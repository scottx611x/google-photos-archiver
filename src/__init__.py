import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

__version__ = os.getenv("CIRCLE_TAG", "0.0.0")
