#!/usr/bin/env python

import os
import logging
import argparse
from typing import List, Dict

from photowebpage.image_selection import find_images, handled_image_extensions, get_output_paths, scale_images
from photowebpage.html_generator import gen_full_webpage
from photowebpage.common import outhtml_filename, outdir_subdir_html, outdir_subdir_img, outdir_subdir_thumbnails

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Generate a static web page with an image gallery from a directory of images.')
    # Optional positional argument
    parser.add_argument('imgdir', type=str, default=os.getcwd(),
                    help='Directory containing input images. Defaults to current working directory if omitted.')
    parser.add_argument('--outdir', type=str, default=os.getcwd(),
                    help='An existing, writeable output directory. In this folder, both the HTML and the web-ready images and thumbnails will be placed. Defaults to current working directory if omitted.')
    parser.add_argument('--thumbnails', action='store_true',
                    help='Whether to generate and use thumbnails for the images.')

    args = parser.parse_args()

    indir : str = os.path.abspath(args.imgdir)
    outdir : str = os.path.abspath(args.outdir)
    use_thumbnails : bool = args.thumbnails

    if not os.path.isdir(indir):
        parser.error(f"Input image directory '{indir}' does not exist or is not accessible. Please check.")

    if not os.path.isdir(outdir):
        parser.error(f"Output directory '{outdir}' does not exist or is not accessible. Please check.")
    if not os.access(outdir, os.W_OK | os.X_OK):
        logger.warning(f"Output directory '{outdir}' may not be writeable.")

    logger.info(f"Using input dir '{indir}' and output dir '{outdir}'.")

    outsubdirs : Dict[str, str] = { 'images' : os.path.join(outdir, outdir_subdir_img) }

    if use_thumbnails:
        outsubdirs['thumbnails'] = os.path.join(outdir, outdir_subdir_thumbnails)

    for subdirname in outsubdirs.keys():
        sub_outdir = outsubdirs.get(subdirname)
        if not os.path.isdir(sub_outdir):
            os.mkdir(sub_outdir)
        else:
            logger.info(f"Output {subdirname} directory '{sub_outdir}' already exists.")

    image_filenames : List[str] = find_images([indir])
    logger.info(f"Found {len(image_filenames)} image files in directory '{indir}' with uppercased extensions '{handled_image_extensions}'.")

    if not len(image_filenames) > 0:
        logger.warning("No images found, please check the input directory setting.")

    web_image_filenames : List[str] = get_output_paths(image_filenames, outdir=outsubdirs["images"])
    scale_images(image_filenames, web_image_filenames, max_width=900, max_height=900)

    if use_thumbnails:
        web_thumbnail_filenames : List[str] = get_output_paths(image_filenames, outdir=outsubdirs["images"], prefix="thumbnail_")
        scale_images(image_filenames, web_thumbnail_filenames, max_width=900, max_height=900)

    webpage : str = gen_full_webpage(image_filenames)
    output_html_file = os.path.join(outdir, outhtml_filename)
    with open(output_html_file, "w") as text_file:
        text_file.write(webpage)
    logger.info(f"Web gallery page for {len(image_filenames)} images written to file '{output_html_file}'")

if __name__ == "__main__":
    main()