"""Lectura y actualizacion del CV base."""

from app import config


class CVNotFoundError(Exception):
    pass


def read_cv() -> str:
    if not config.CV_BASE_PATH.exists():
        raise CVNotFoundError(f"No se encontro el CV base en {config.CV_BASE_PATH}")
    return config.CV_BASE_PATH.read_text(encoding="utf-8")


def write_cv(text: str) -> None:
    if not text or not text.strip():
        raise CVNotFoundError("El CV actualizado esta vacio")
    config.CV_BASE_PATH.write_text(text, encoding="utf-8")
