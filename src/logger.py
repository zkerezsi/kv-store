import sys
import logging

logger = logging.getLogger("main")
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
