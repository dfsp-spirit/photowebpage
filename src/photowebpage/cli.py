#!/usr/bin/env python

import os
import logging
import argparse
from typing import List

from photowebpage.image_selection import find_images, handled_image_extensions

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Generate a static web page with an image gallery from a directory of images.')
    # Optional positional argument
    parser.add_argument('imgdir', type=str, default=os.getcwd(),
                    help='Directory containing input images. Defaults to current working directory if omitted.')
    parser.add_argument('--outdir', type=str, default=os.getcwd(),
                    help='An existing, writeable output directory. In this folder, both the HTML and the web-ready images and thumbnails will be placed. Defaults to current working directory if omitted.')
    args = parser.parse_args()

    indir : str = os.path.abspath(args.imgdir)
    outdir : str = os.path.abspath(args.outdir)

    if not os.path.isdir(indir):
        parser.error(f"Input image directory '{indir}' does not exist or is not accessible. Please check.")

    if not os.path.isdir(outdir):
        parser.error(f"Output directory '{outdir}' does not exist or is not accessible. Please check.")
    if not os.access(outdir, os.W_OK | os.X_OK):
        logger.warning(f"Output directory '{outdir}' may not be writeable.")

    logger.info(f"Using input dir '{indir}' and output dir '{outdir}'.")

    outdir_html : str = os.path.join(outdir, "html")
    outdir_img : str = os.path.join(outdir, "img")

    if not os.path.isdir(outdir_html):
        os.mkdir(outdir_html)
    else:
        logger.info(f"Output HTML directory '{outdir_html}' already exists.")

    if not os.path.isdir(outdir_img):
        os.mkdir(outdir_img)
    else:
        logger.info(f"Output image directory '{outdir_img}' already exists.")


    image_filenames : List[str] = find_images([indir])
    logger.info(f"Found {len(image_filenames)} image files in directory '{indir}' with uppercased extensions '{handled_image_extensions}'.")


if __name__ == "__main__":
    main()