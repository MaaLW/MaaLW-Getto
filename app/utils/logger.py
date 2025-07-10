import logging
import pathlib
from logging.handlers import TimedRotatingFileHandler

# Create log directory
pathlib.Path("./assets/getto/log").mkdir(parents=True, exist_ok=True)

# Configure logger
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s][%(filename)s][L%(lineno)d][%(funcName)s] | %(message)s",
    level=logging.DEBUG,
    handlers=[
        TimedRotatingFileHandler("./assets/getto/log/getto.log", when="midnight", interval=1, backupCount=7, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)