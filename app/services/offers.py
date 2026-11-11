"""Extraccion y preparacion del contenido de ofertas laborales."""

import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

MAX_DOWNLOAD_BYTES = 5 * 1024 * 1024
MAX_TEXT_CHARS = 8000
REQUEST_TIMEOUT = 15
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

TAGS_TO_SKIP = {"script", "style", "nav", "header", "footer", "aside", "form", "noscript"}


class OfferExtractionError(Exception):
    pass


def validate_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def extract_from_url(url: str) -> str:
    if not validate_url(url):
        raise OfferExtractionError("URL no valida")

    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": USER_AGENT},
            stream=True,
        )
    except requests.RequestException as exc:
        raise OfferExtractionError("No se pudo descargar la pagina") from exc

    if response.status_code != 200:
        raise OfferExtractionError(f"La pagina respondio con estado {response.status_code}")

    content = b""
    for chunk in response.iter_content(chunk_size=8192):
        content += chunk
        if len(content) > MAX_DOWNLOAD_BYTES:
            raise OfferExtractionError("La pagina excede el tamano maximo permitido")

    text = _extract_main_text(content)
    if not text:
        raise OfferExtractionError("No se encontro contenido en la pagina")
    return text


def _extract_main_text(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")
    for tag in soup(TAGS_TO_SKIP):
        tag.decompose()
    for tag in soup.find_all(["a", "img", "button"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    return _normalize_whitespace(text)


def prepare_offer_text(text: str) -> str:
    cleaned = _normalize_whitespace(text)
    if len(cleaned) > MAX_TEXT_CHARS:
        cleaned = cleaned[:MAX_TEXT_CHARS].rstrip()
    return cleaned


def _normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    lines = [line for line in lines if line]
    return "\n".join(lines)
