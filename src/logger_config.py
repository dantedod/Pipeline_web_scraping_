# src/logger_config.py
import logging
import os


def setup_logger(name: str, log_dir: str = "logs/pipeline") -> logging.Logger:

    os.makedirs(log_dir, exist_ok=True)

    from datetime import datetime

    data_atual = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    log_file = os.path.join(log_dir, f"{name}_{data_atual}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", "%d-%m-%y %H:%M:%S"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger, log_file
