"""Adaptacion del CV a una oferta laboral."""

import json
from dataclasses import dataclass

from app.llm import client, prompts
from app.services import cv as cv_service, offers


class AdaptationError(Exception):
    pass


@dataclass
class AdaptationResult:
    adapted_cv: str
    base_cv: str
    offer_text: str


@dataclass
class GapUpdate:
    added: bool
    cv: str


async def adapt_cv(offer_text: str) -> AdaptationResult:
    offer_text = offers.prepare_offer_text(offer_text)

    try:
        base_cv = cv_service.read_cv()
    except cv_service.CVNotFoundError as exc:
        raise AdaptationError("No se pudo leer el CV base") from exc

    analyze_prompt = prompts.render_analyze_offer(offer_text)
    try:
        offer_analysis = await client.generate(
            [{"role": "user", "content": analyze_prompt}]
        )
    except client.LLMError as exc:
        raise AdaptationError("No se pudo analizar la oferta") from exc

    adapt_prompt = prompts.render_adapt_cv(base_cv, offer_analysis)
    try:
        adapted_cv = await client.generate([{"role": "user", "content": adapt_prompt}])
    except client.LLMError as exc:
        raise AdaptationError("No se pudo adaptar el CV") from exc

    return AdaptationResult(adapted_cv=adapted_cv, base_cv=base_cv, offer_text=offer_text)


async def apply_gap_responses(base_cv: str, gaps: list[str], response: str) -> GapUpdate:
    prompt = prompts.render_apply_gaps(base_cv, gaps, response)
    try:
        raw = await client.generate(
            [{"role": "user", "content": prompt}], json_mode=True
        )
    except client.LLMError as exc:
        raise AdaptationError("No se pudo actualizar el CV") from exc

    data = _parse_json(raw)
    added = bool(data.get("added", False))
    cv_text = data.get("cv", "")
    if not isinstance(cv_text, str):
        cv_text = str(cv_text)
    return GapUpdate(added=added, cv=cv_text)


def _parse_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise AdaptationError("No se pudo procesar tu respuesta") from exc
    if not isinstance(data, dict):
        raise AdaptationError("No se pudo procesar tu respuesta")
    return data
