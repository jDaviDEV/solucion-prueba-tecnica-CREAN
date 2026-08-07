from pathlib import Path
from datetime import datetime
import logging


class Logger:

    def __init__(self):

        # Raíz del proyecto
        root = Path(__file__).resolve().parents[2]

        # Carpeta de logs
        log_dir = root / "logs"
        log_dir.mkdir(exist_ok=True)

        # Nombre del archivo
        log_file = log_dir / f"{datetime.now():%Y%m%d_%H%M%S}.log"

        # Logger principal
        self.logger = logging.getLogger("solucion")
        self.logger.setLevel(logging.INFO)

        # Evita agregar handlers duplicados si se importa varias veces
        if self.logger.handlers:
            return

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Archivo
        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        # Consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger