"""Punto de entrada de Perfilia."""

import asyncio
import logging

from app.bot.bot import create_application
from app.database import history


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)


def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Perfilia iniciando...")
    history.init_db()
    application = create_application()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        application.run_polling(close_loop=False)
    finally:
        loop.close()


if __name__ == "__main__":
    main()
