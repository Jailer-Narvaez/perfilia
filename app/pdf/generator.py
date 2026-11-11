"""Generacion del PDF del CV adaptado con fpdf2."""

from datetime import datetime
from pathlib import Path

from fpdf import FPDF

from app import config

FONT_FAMILY = "Cv"
BODY_SIZE = 10
LINE_HEIGHT = 5


class PDFGenerationError(Exception):
    pass


def generate_pdf(markdown_text: str) -> Path:
    pdf = _build_document()
    pdf.add_page()

    for line in markdown_text.split("\n"):
        _render_line(pdf, line)

    filename = f"cv_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.pdf"
    output_path = config.OUTPUT_DIR / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))
    return output_path


def _build_document() -> FPDF:
    if not config.PDF_FONT_REGULAR.exists():
        raise PDFGenerationError(
            f"No se encontro la fuente: {config.PDF_FONT_REGULAR}"
        )

    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_font(FONT_FAMILY, "", str(config.PDF_FONT_REGULAR))
    bold_path = config.PDF_FONT_BOLD if config.PDF_FONT_BOLD.exists() else config.PDF_FONT_REGULAR
    pdf.add_font(FONT_FAMILY, "B", str(bold_path))

    return pdf


def _render_line(pdf: FPDF, line: str) -> None:
    text = line.rstrip()
    if not text.strip():
        pdf.ln(2)
        return

    if text.startswith("### "):
        pdf.set_font(FONT_FAMILY, "B", 11)
        pdf.multi_cell(0, LINE_HEIGHT + 1, text[4:].strip())
    elif text.startswith("## "):
        pdf.ln(3)
        pdf.set_font(FONT_FAMILY, "B", 13)
        pdf.multi_cell(0, 6, text[3:].strip().upper())
        y = pdf.get_y()
        pdf.set_draw_color(80, 80, 80)
        pdf.set_line_width(0.4)
        pdf.line(pdf.l_margin, y + 0.5, pdf.w - pdf.r_margin, y + 0.5)
        pdf.ln(2)
    elif text.startswith("# "):
        pdf.set_font(FONT_FAMILY, "B", 18)
        pdf.multi_cell(0, 8, text[2:].strip(), align="C")
    elif text.startswith("- "):
        _write_inline(pdf, "\u2022 " + text[2:].strip())
        pdf.ln()
    else:
        _write_inline(pdf, text.strip())
        pdf.ln()


def _write_inline(pdf: FPDF, text: str, size: int = BODY_SIZE) -> None:
    for index, segment in enumerate(text.split("**")):
        if not segment:
            continue
        pdf.set_font(FONT_FAMILY, "B" if index % 2 == 1 else "", size)
        pdf.write(LINE_HEIGHT, segment)
