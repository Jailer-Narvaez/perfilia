# Perfilia

Bot de Telegram que adapta tu currículum a ofertas laborales y genera un PDF compatible con sistemas ATS, manteniendo siempre la veracidad de tu información profesional.

## Flujo de trabajo

1. Envías una oferta laboral por Telegram (enlace o texto).
2. El bot analiza la oferta y adapta tu CV base.
3. Valida que la información generada corresponda con tu experiencia real.
4. Si la validación es satisfactoria, genera el PDF y lo envía por Telegram.

**Regla fundamental:** nunca se inventa experiencia, habilidades, estudios, certificaciones, cargos, fechas ni logros. Si la validación falla, no se genera el PDF.

## Tecnologías

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.13+ |
| Bot | python-telegram-bot |
| LLM | Gemini mediante freelm |
| CV base | Markdown (`cv_base.md`) |
| Base de datos | SQLite |
| PDF | fpdf2 |
| Configuración | Variables de entorno (`.env`) |

## Requisitos

- Python 3.13 o superior.
- Un bot de Telegram y su token (vía [BotFather](https://t.me/BotFather)).
- Una API key de Gemini (vía [Google AI Studio](https://aistudio.google.com/apikey)).

## Instalación

```bash
git clone <repositorio>
cd perfilia
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # Linux / macOS
python -m pip install -r requirements.txt
```

## Configuración

1. Copia el archivo de ejemplo y rellena los valores:

```bash
cp .env.example .env
```

2. Edita `.env`:

```env
TELEGRAM_TOKEN=<token de tu bot>
ALLOWED_USER_ID=<tu Telegram user ID>
LLM_API_KEY=<tu API key de Gemini>
LLM_PROVIDER=gemini
OUTPUT_LANGUAGE=es
```

3. Crea tu CV base a partir de la plantilla y rellénalo con tu información:

```bash
cp cv_base.example.md cv_base.md
```

`cv_base.md` contiene tus datos personales y no se sube al repositorio (está en `.gitignore`).

| Variable | Descripción |
|---|---|
| `TELEGRAM_TOKEN` | Token del bot creado con BotFather. |
| `ALLOWED_USER_ID` | Tu ID de Telegram. El bot ignora mensajes de otros usuarios. |
| `LLM_API_KEY` | API key del proveedor de lenguaje (Gemini por defecto). |
| `LLM_PROVIDER` | Proveedor LLM. Por defecto `gemini`. |
| `OUTPUT_LANGUAGE` | Idioma del CV generado. Por defecto `es`. |
| `MIN_MATCH_SCORE` | Umbral mínimo de cumplimiento (%) para generar el PDF. Por defecto `70`. |
| `MAX_FIDELITY_ATTEMPTS` | Intentos máximos de auto-corrección de fidelidad. Por defecto `3`. |
| `PDF_FONT_REGULAR` | Ruta a la fuente TTF regular para el PDF. |
| `PDF_FONT_BOLD` | Ruta a la fuente TTF negrita para el PDF. |

### Obtener tu Telegram user ID

Envía `/start` a [@userinfobot](https://t.me/userinfobot) y anota el número que devuelve.

## Ejecución

Con el entorno virtual activo:

```bash
python main.py
```

El bot queda escuchando por *polling* en segundo plano. Deténlo con `Ctrl+C`.

## Estructura del proyecto

```text
perfilia/
├── app/
│   ├── bot/             # Comandos y mensajes de Telegram
│   ├── services/        # Adaptación, validación y extracción
│   ├── llm/             # Comunicación con el modelo de lenguaje
│   ├── pdf/             # Generación del PDF (fpdf2)
│   ├── database/        # Historial de adaptaciones
│   └── config.py        # Configuración
├── data/
│   ├── history/         # Historial
│   └── output/          # PDFs generados
├── prompts/             # Instrucciones para el LLM
├── sdd/                 # Documentación de especificación (constitution, architecture, features, tasks)
├── cv_base.example.md   # Plantilla del CV (cópiala como cv_base.md)
├── cv_base.md           # CV real (fuente única de información; no se sube al repositorio)
├── .env                 # Credenciales y configuración (no subir al repositorio)
├── .env.example
├── agents.md            # Instrucciones para el agente de IA
├── LICENSE
├── requirements.txt
└── main.py
```

## El CV base

`cv_base.md` es la fuente única de tu información profesional. La adaptación solo cambia la redacción y organización, nunca los hechos. Mantenlo actualizado para que las adaptaciones reflejen tu experiencia real.

Para crearlo, copia `cv_base.example.md` y rellénalo con tu información. El archivo real se mantiene fuera del repositorio para no exponer tus datos personales.

## Estado de desarrollo

- [x] Fase 1 — Configuración inicial
- [x] Fase 2 — Bot de Telegram
- [x] Fase 3 — Gestión de ofertas laborales
- [x] Fase 4 — Integración con LLM
- [x] Fase 5 — Validación del CV
- [x] Fase 6 — Generación del PDF
- [x] Fase 7 — Historial
- [ ] Fase 8 — Pruebas y finalización (sin tests automatizados)
