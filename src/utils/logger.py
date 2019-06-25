import logging

logger = logging.getLogger("esim")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

FORMAT = "[%(asctime)s][%(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
DTFMT = "%H:%M:%S"
fromatter = logging.Formatter(fmt=FORMAT, datefmt=DTFMT)

ch.setFormatter(fromatter)

logger.addHandler(ch)
