# logging_config.py
import logging
from colorlog import ColoredFormatter
import os

# Zorg dat de logmap bestaat
os.makedirs("logs", exist_ok=True)

# Formatter zonder kleur voor logbestanden
# ANSI kleurcodes
# Formatter zonder kleur voor logbestanden
file_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

# Formatter met kleur voor console
console_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    log_colors={
        "DEBUG": "white",
        "INFO": "blue",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red"
    }
)

# File handler voor logbestanden
file_handler = logging.FileHandler("logs/app.log")
file_handler.setLevel(logging.DEBUG)  # Log alles vanaf DEBUG in het bestand
file_handler.setFormatter(file_formatter)

# Console handler voor gekleurde output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Toon alles vanaf DEBUG in de console
console_handler.setFormatter(console_formatter)

# Logger instellen
logger = logging.getLogger("file_and_console_logger")
logger.setLevel(logging.DEBUG)  # Vang alles vanaf DEBUG
logger.addHandler(file_handler)
logger.addHandler(console_handler)