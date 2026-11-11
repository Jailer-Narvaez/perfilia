"""Handlers de mensajes del bot de Perfilia."""

import asyncio
import logging
from pathlib import Path

from telegram import Message, Update
from telegram.ext import ContextTypes

from app import config
from app.database import history
from app.pdf import generator as pdf_generator
from app.services import adaptation, cv as cv_service, offers, validation

logger = logging.getLogger(__name__)

WELCOME_TEXT = (
    "Hola, soy Perfilia.\n\n"
    "Envíame una oferta laboral como enlace o como texto y adaptaré tu CV "
    "generando un PDF compatible con sistemas ATS."
)

COMMANDS_TEXT = (
    "Comandos disponibles:\n\n"
    "/start — Mensaje de bienvenida e instrucciones.\n"
    "/comandos — Muestra este listado de comandos.\n"
    "/historial — Lista las últimas adaptaciones registradas.\n"
    "/eliminar <id> — Elimina un registro del historial y su PDF."
)


def extract_url(message: Message) -> str | None:
    if not message.text or not message.entities:
        return None
    for entity in message.entities:
        if entity.type == "url":
            return message.text[entity.offset : entity.offset + entity.length]
        if entity.type == "text_link":
            return entity.url
    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_TEXT)


async def comandos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(COMMANDS_TEXT)


async def historial(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        records = await asyncio.to_thread(history.list_adaptations)
    except Exception:
        logger.exception("No se pudo consultar el historial")
        await update.message.reply_text("No pude consultar el historial.")
        return

    if not records:
        await update.message.reply_text("No hay adaptaciones registradas.")
        return

    lines = []
    for record in records:
        snippet = record["offer_text"].split("\n")[0][:60]
        source = record.get("source") or ""
        if len(source) > 40:
            source = source[:40] + "..."
        lines.append(
            f"{record['id']}. {record['created_at']} — {record['match_score']}% — "
            f"[{source}] {snippet}"
        )
    await update.message.reply_text(
        "Últimas adaptaciones:\n\n" + "\n".join(lines)
    )


async def eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("Uso: /eliminar <id>")
        return
    if not args[0].isdigit():
        await update.message.reply_text("El ID debe ser un número entero.")
        return

    adaptation_id = int(args[0])
    try:
        pdf_path = await asyncio.to_thread(history.delete_adaptation, adaptation_id)
    except Exception:
        logger.exception("No se pudo eliminar el registro del historial")
        await update.message.reply_text("No pude eliminar el registro.")
        return

    if pdf_path is None:
        await update.message.reply_text(
            f"No existe un registro con el ID {adaptation_id}."
        )
        return

    if pdf_path:
        try:
            path = Path(pdf_path)
            if path.exists():
                path.unlink()
        except OSError:
            logger.exception("No se pudo eliminar el PDF del disco")

    await update.message.reply_text(f"Registro {adaptation_id} eliminado.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get("pending_gaps"):
        await _handle_gap_reply(update, context)
        return

    if context.user_data.get("pending_source"):
        await _handle_source_reply(update, context)
        return

    url = extract_url(update.message)
    if url:
        offer_text = await _offer_from_url(update, url)
        if offer_text is None:
            return
    else:
        offer_text = update.message.text

    context.user_data["pending_source"] = {"offer_text": offer_text}
    await update.message.reply_text(
        "¿De dónde proviene esta oferta? Envíame la fuente "
        "(por ejemplo la URL, LinkedIn, Computrabajo, etc.)."
    )


async def _handle_source_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    source = update.message.text
    if not source or not source.strip():
        await update.message.reply_text(
            "Envía la fuente de la oferta (URL, portal, etc.) para continuar."
        )
        return

    pending = context.user_data.pop("pending_source", None)
    await _adapt_and_reply(update, context, pending["offer_text"], source=source.strip())


async def _offer_from_url(update: Update, url: str) -> str | None:
    try:
        return await asyncio.to_thread(offers.extract_from_url, url)
    except offers.OfferExtractionError as exc:
        await update.message.reply_text(
            f"No pude extraer el contenido de la oferta ({exc}). "
            "Envíame el texto de la oferta directamente."
        )
        return None


async def _adapt_and_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    offer_text: str,
    allow_gap_question: bool = True,
    source: str = "texto",
) -> None:
    await update.message.reply_text("Adaptando tu CV a la oferta...")
    try:
        result = await adaptation.adapt_cv(offer_text)
    except adaptation.AdaptationError as exc:
        await update.message.reply_text(f"No pude adaptar el CV: {exc}")
        return

    await update.message.reply_text("Validando la fidelidad del contenido...")
    try:
        adapted_cv, remaining_issues = await validation.refine_adapted_cv(
            result.base_cv, result.adapted_cv, config.MAX_FIDELITY_ATTEMPTS
        )
    except validation.ValidationError as exc:
        await update.message.reply_text(
            f"No se pudo validar el contenido ({exc}). No se generará el documento."
        )
        return

    if remaining_issues:
        issues = "\n".join(f"- {item}" for item in remaining_issues)
        await update.message.reply_text(
            "La validación de fidelidad falló. No se generará el documento.\n\n"
            + issues
        )
        return

    await update.message.reply_text("Evaluando el cumplimiento con la oferta...")
    try:
        match = await validation.evaluate_match(result.base_cv, result.offer_text)
    except validation.ValidationError as exc:
        await update.message.reply_text(
            f"No se pudo evaluar el cumplimiento ({exc}). No se generará el documento."
        )
        return

    if match.score < config.MIN_MATCH_SCORE:
        if allow_gap_question and match.gaps:
            context.user_data["pending_gaps"] = {
                "offer_text": result.offer_text,
                "gaps": match.gaps,
                "source": source,
            }
            numbered = _format_gaps_numbered(match.gaps)
            await update.message.reply_text(
                f"Tu perfil cumple {match.score}% de la oferta, por debajo del "
                f"{config.MIN_MATCH_SCORE}% requerido.\n\n"
                f"Brechas detectadas:\n{numbered}\n\n"
                "Respóndeme con texto libre por cada brecha: si cuentas con ese "
                "conocimiento o experiencia descríbelo; si no, responde 'no'."
            )
            return

        gaps = "\n".join(f"- {item}" for item in match.gaps)
        await update.message.reply_text(
            f"Tu perfil cumple {match.score}% de la oferta, por debajo del "
            f"{config.MIN_MATCH_SCORE}% requerido. No se generará el documento.\n\n"
            f"Brechas principales:\n{gaps}"
        )
        return

    try:
        pdf_path = pdf_generator.generate_pdf(adapted_cv)
    except pdf_generator.PDFGenerationError as exc:
        await update.message.reply_text(f"No pude generar el PDF: {exc}")
        return

    try:
        history.save_adaptation(
            result.offer_text, adapted_cv, str(pdf_path), match.score, source
        )
    except Exception:
        logger.exception("No se pudo guardar la adaptacion en el historial")

    await send_pdf(update.effective_chat.id, pdf_path, context)
    await update.message.reply_text(
        f"Aquí tienes tu CV adaptado en PDF. Tu perfil cumple {match.score}% de la oferta."
    )


async def _handle_gap_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pending = context.user_data["pending_gaps"]
    gaps = pending["gaps"]
    offer_text = pending["offer_text"]
    source = pending.get("source", "texto")
    response = update.message.text

    if not response or not response.strip():
        await update.message.reply_text(
            "No entendí tu respuesta. Cuéntame por cada brecha si cuentas con ese "
            "conocimiento o experiencia, o responde 'no'."
        )
        return

    context.user_data.pop("pending_gaps", None)

    try:
        base_cv = cv_service.read_cv()
        result = await adaptation.apply_gap_responses(base_cv, gaps, response)
    except cv_service.CVNotFoundError as exc:
        await update.message.reply_text(f"No se pudo actualizar el CV: {exc}")
        return
    except adaptation.AdaptationError as exc:
        await update.message.reply_text(f"No se pudo actualizar el CV: {exc}")
        return

    if not result.added:
        await update.message.reply_text(
            "Entendido. No se agregó información, por lo que no se generará el documento."
        )
        return

    cv_service.write_cv(result.cv)
    await update.message.reply_text("Actualicé tu CV con la información confirmada.")

    await _adapt_and_reply(
        update, context, offer_text, allow_gap_question=False, source=source
    )


def _format_gaps_numbered(gaps: list[str]) -> str:
    return "\n".join(f"{index}. {gap}" for index, gap in enumerate(gaps, start=1))


async def handle_unsupported(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Solo acepto ofertas laborales como texto o enlaces.")


async def send_pdf(chat_id: int, path: Path, context: ContextTypes.DEFAULT_TYPE) -> None:
    with path.open("rb") as pdf_file:
        await context.bot.send_document(
            chat_id=chat_id, document=pdf_file, filename=path.name
        )
