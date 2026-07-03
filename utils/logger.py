import logging
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]

log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)

log_file = log_dir / "pipeline.log"

logger = logging.getLogger("AeroStream")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers if imported multiple times
if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)