"""Carga y renderizado de los prompts del LLM."""

from app import config


def _load(name: str) -> str:
    path = config.PROMPTS_DIR / name
    return path.read_text(encoding="utf-8")


def render_analyze_offer(offer_text: str) -> str:
    template = _load("analyze_offer.txt")
    return template.replace("{{offer}}", offer_text)


def render_adapt_cv(cv_text: str, offer_analysis: str) -> str:
    template = _load("adapt_cv.txt")
    return (
        template.replace("{{cv}}", cv_text)
        .replace("{{offer}}", offer_analysis)
        .replace("{{language}}", config.OUTPUT_LANGUAGE)
    )


def render_check_fidelity(cv_text: str, adapted_cv: str) -> str:
    template = _load("validate_cv.txt")
    return (
        template.replace("{{cv}}", cv_text)
        .replace("{{adapted}}", adapted_cv)
        .replace("{{language}}", config.OUTPUT_LANGUAGE)
    )


def render_correct_cv(cv_text: str, adapted_cv: str, issues: str) -> str:
    template = _load("correct_cv.txt")
    return (
        template.replace("{{cv}}", cv_text)
        .replace("{{adapted}}", adapted_cv)
        .replace("{{issues}}", issues)
        .replace("{{language}}", config.OUTPUT_LANGUAGE)
    )


def render_evaluate_match(cv_text: str, offer_text: str) -> str:
    template = _load("evaluate_match.txt")
    return (
        template.replace("{{cv}}", cv_text)
        .replace("{{offer}}", offer_text)
        .replace("{{language}}", config.OUTPUT_LANGUAGE)
    )


def render_apply_gaps(cv_text: str, gaps: list[str], response: str) -> str:
    template = _load("apply_gaps.txt")
    formatted_gaps = "\n".join(f"{i}. {gap}" for i, gap in enumerate(gaps, start=1))
    return (
        template.replace("{{cv}}", cv_text)
        .replace("{{gaps}}", formatted_gaps)
        .replace("{{response}}", response)
        .replace("{{language}}", config.OUTPUT_LANGUAGE)
    )
