import logging
import pathlib

# Create log directory
pathlib.Path("./assets/cache/debug").mkdir(parents=True, exist_ok=True)

# Configure logger
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s][%(filename)s][L%(lineno)d][%(funcName)s] | %(message)s",
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("./assets/cache/debug/mlw-getto.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)