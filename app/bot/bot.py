"""Construccion y configuracion del bot de Telegram."""

import logging

from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

from app import config
from app.bot import handlers

logger = logging.getLogger(__name__)


def _user_filter():
    if config.ALLOWED_USER_ID is not None:
        return filters.User(user_id=config.ALLOWED_USER_ID)
    logger.warning("ALLOWED_USER_ID no configurado: el bot aceptara mensajes de cualquier usuario.")
    return filters.ALL


def create_application() -> Application:
    if not config.TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN no esta configurado en .env")

    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    allowed = _user_filter()

    application.add_handler(CommandHandler("start", handlers.start, filters=allowed))
    application.add_handler(
        CommandHandler("comandos", handlers.comandos, filters=allowed)
    )
    application.add_handler(
        CommandHandler("historial", handlers.historial, filters=allowed)
    )
    application.add_handler(
        CommandHandler("eliminar", handlers.eliminar, filters=allowed)
    )
    application.add_handler(
        MessageHandler(allowed & filters.TEXT & ~filters.COMMAND, handlers.handle_message)
    )
    application.add_handler(
        MessageHandler(allowed & ~filters.TEXT, handlers.handle_unsupported)
    )

    return application
