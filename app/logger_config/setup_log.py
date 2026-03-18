from pathlib import Path

from loguru import logger

BASE_DIR = Path(__file__).parent
log_path = BASE_DIR / "log_files" / "app.log"


logger.add(log_path, rotation="10 MB")
