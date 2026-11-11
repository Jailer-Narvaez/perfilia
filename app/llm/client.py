"""Comunicacion con el modelo de lenguaje mediante freelm."""

import logging

from freelm import AsyncFreeLLM, GoogleAIStudio

from app import config

logger = logging.getLogger(__name__)

PROVIDERS = {"gemini": GoogleAIStudio}


class LLMError(Exception):
    pass


_client = None


def _build_client() -> AsyncFreeLLM:
    if not config.LLM_API_KEY:
        raise LLMError("LLM_API_KEY no esta configurado en .env")

    provider_cls = PROVIDERS.get(config.LLM_PROVIDER.lower())
    if provider_cls is None:
        raise LLMError(f"Proveedor LLM no soportado: {config.LLM_PROVIDER}")

    return AsyncFreeLLM([provider_cls(config.LLM_API_KEY)])


def get_client() -> AsyncFreeLLM:
    global _client
    if _client is None:
        _client = _build_client()
    return _client


async def generate(messages: list[dict], json_mode: bool = False) -> str:
    client = get_client()
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    try:
        response = await client.chat(messages, **kwargs)
    except Exception as exc:
        logger.exception("Error al llamar al proveedor LLM")
        raise LLMError("El proveedor LLM fallo al responder") from exc

    text = (response.text or "").strip()
    if not text:
        raise LLMError("El proveedor LLM devolvio una respuesta vacia")
    return text
