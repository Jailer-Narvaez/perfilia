"""Validacion de fidelidad y evaluacion de cumplimiento del CV."""

import json
from dataclasses import dataclass, field

from app.llm import client, prompts


class ValidationError(Exception):
    pass


@dataclass
class MatchResult:
    score: int
    gaps: list[str] = field(default_factory=list)


async def check_fidelity(base_cv: str, adapted_cv: str) -> list[str]:
    prompt = prompts.render_check_fidelity(base_cv, adapted_cv)
    try:
        raw = await client.generate(
            [{"role": "user", "content": prompt}], json_mode=True
        )
    except client.LLMError as exc:
        raise ValidationError("No se pudo validar el contenido") from exc

    data = _parse_json(raw)
    issues = data.get("issues", [])
    if not isinstance(issues, list):
        issues = [issues]
    return [str(item) for item in issues]


async def correct_cv(base_cv: str, adapted_cv: str, issues: list[str]) -> str:
    prompt = prompts.render_correct_cv(base_cv, adapted_cv, _format_issues(issues))
    try:
        return await client.generate([{"role": "user", "content": prompt}])
    except client.LLMError as exc:
        raise ValidationError("No se pudo corregir el CV") from exc


async def refine_adapted_cv(
    base_cv: str, adapted_cv: str, max_attempts: int
) -> tuple[str, list[str]]:
    current = adapted_cv
    issues = await check_fidelity(base_cv, current)
    for _ in range(max_attempts):
        if not issues:
            break
        current = await correct_cv(base_cv, current, issues)
        issues = await check_fidelity(base_cv, current)
    return current, issues


async def evaluate_match(base_cv: str, offer_text: str) -> MatchResult:
    prompt = prompts.render_evaluate_match(base_cv, offer_text)
    try:
        raw = await client.generate(
            [{"role": "user", "content": prompt}], json_mode=True
        )
    except client.LLMError as exc:
        raise ValidationError("No se pudo evaluar el cumplimiento") from exc

    data = _parse_json(raw)
    score = _parse_score(data.get("score"))
    gaps = data.get("gaps", [])
    if not isinstance(gaps, list):
        gaps = [gaps]
    return MatchResult(score=score, gaps=[str(item) for item in gaps])


def _parse_score(value) -> int:
    try:
        score = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError("El porcentaje de cumplimiento no es valido") from exc
    return max(0, min(100, score))


def _format_issues(issues: list[str]) -> str:
    return "\n".join(f"- {item}" for item in issues)


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
        raise ValidationError("La respuesta de validacion no es JSON valido") from exc
    if not isinstance(data, dict):
        raise ValidationError("La respuesta de validacion no tiene el formato esperado")
    return data
