"""
photowebpage: generate a static HTML page with an image gallery from all images in a folder.

This module is the package entry point. It also configures the package-wide
logger that is used by all other modules of the package.
"""

import sys
import logging

# ----- Package-wide logger configuration ------
logger = logging.getLogger(__name__)
logger.setLevel(
    logging.DEBUG
)  # configure the default log level here. logging.INFO or logging.DEBUG should do it.
# logger.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
fmt_interactive = logging.Formatter(
    "%(asctime)s - %(levelname)s: %(message)s", "%H:%M:%S"
)
sh.setFormatter(fmt_interactive)
logger.addHandler(sh)
