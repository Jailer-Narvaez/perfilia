# Arquitectura del proyecto

## 1. Descripción

Bot de Telegram que recibe una oferta laboral mediante un enlace o texto, adapta el CV del usuario utilizando un modelo de lenguaje y genera un PDF optimizado para sistemas ATS.

El sistema tendrá inicialmente un único usuario y funcionará localmente mediante Polling.

## 2. Tecnologías

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.13+ |
| Bot | python-telegram-bot |
| LLM | Gemini mediante freelm |
| CV base | Markdown |
| Base de datos | SQLite |
| PDF | fpdf2 |
| Configuración | Variables de entorno (.env) |

## 3. Funcionamiento

1. El usuario envía una oferta laboral mediante Telegram.
2. El sistema obtiene el contenido de la oferta. Si no puede leer el enlace, solicita el texto directamente.
3. El sistema solicita al usuario el origen o fuente de la oferta y, con esa respuesta, continúa el flujo.
4. Lee el CV base almacenado en `cv_base.md`.
5. Envía el CV y la oferta al LLM para adaptar el contenido.
6. Valida que la información generada corresponda con la experiencia real del usuario, auto-corrigiéndola si es necesario.
7. Evalúa el porcentaje de cumplimiento del CV con respecto a la oferta.
8. Si el cumplimiento es inferior al umbral, consulta al usuario por los conocimientos o experiencia faltantes; con la respuesta en texto libre, el modelo completa el CV en la sección correspondiente (solo agrega, no modifica lo existente).
9. Si el cumplimiento es igual o superior al umbral configurado, genera el PDF.
10. Guarda el resultado en SQLite (`data/history/history.db`) y envía el PDF por Telegram.

**Regla fundamental:** nunca se deben inventar experiencias, habilidades, estudios, certificaciones, cargos, fechas o logros. Si no puede eliminarse la información inventada o no se alcanza el umbral de cumplimiento, no se genera el PDF. La información solo se agrega al CV base con confirmación explícita del usuario.

## 4. Estructura del proyecto

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
├── cv_base.md           # CV original
├── .env                 # Credenciales y configuración
├── .env.example
├── requirements.txt
└── main.py
```

## 5. Reglas de desarrollo

- Mantener el CV original como fuente única de información.
- Utilizar prompts en inglés y generar resultados en español por defecto.
- Permitir cambiar el idioma y proveedor LLM mediante configuración.
- Utilizar un diseño de una columna, sobrio y compatible con ATS.
- Guardar cada adaptación como un registro independiente.
- No generar PDF si la validación de fidelidad falla o no se alcanza el umbral de cumplimiento.
- Mantener separados los módulos para facilitar cambios futuros.

## 6. Configuración

Las credenciales y opciones se administran mediante `.env`:

```env
TELEGRAM_TOKEN=
LLM_API_KEY=
LLM_PROVIDER=gemini
OUTPUT_LANGUAGE=es
MIN_MATCH_SCORE=70
MAX_FIDELITY_ATTEMPTS=3
```

## 7. Alcance futuro

El proyecto debe permitir incorporar posteriormente:
- Nuevos proveedores de modelos de lenguaje.
- Soporte para múltiples usuarios.
- Webhook para despliegue en un VPS.
- Otros formatos de exportación.
- PostgreSQL en reemplazo de SQLite.