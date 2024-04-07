#!/usr/bin/env python

import os
import logging

from image_selection import find_images

logger = logging.getLogger(__name__)


def main():
    logger.warning("Running main.")
    directory : str = os.getcwd()  # path = os.path.abspath(".")
    image_filenames : list = find_images(directory)
    logger.info(f"Found {len(image_filenames)} files.")


if __name__ == "__main__":
    main()