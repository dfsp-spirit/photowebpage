#!/usr/bin/env python

"""
photowebpage.cli
~~~~~~~~~~~~~~~~

Command line interface of the photowebpage package.

This module implements the ```photogallery``` command (```main```) and exposes
the underlying ```generate_gallery``` function, which scans a directory for
images and generates a static HTML gallery page from them.
"""

import os
import logging
import argparse
from typing import List, Dict, Union

from photowebpage.image_selection import (
    find_images,
    handled_image_extensions,
    get_output_paths,
    scale_images,
    sort_filenames_by_aspect_ratio,
)
from photowebpage.html_generator import gen_full_webpage
from photowebpage.common import (
    outhtml_filename,
    outdir_subdir_img,
    outdir_subdir_thumbnails,
    img_height_max,
    img_width_max,
    thumbnail_img_width_max,
    thumbnail_img_height_max,
)

logger = logging.getLogger(__name__)


def main():
    """
    Run the photogallery command line application.

    Parses the command line arguments and delegates the actual gallery
    generation to ```generate_gallery```.
    """
    parser = argparse.ArgumentParser(
        description="Generate a static web page with an image gallery from a directory of images."
    )
    # Optional positional argument
    parser.add_argument(
        "imgdir",
        type=str,
        default=os.getcwd(),
        help="Directory containing input images. Defaults to current working directory if omitted.",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default=os.getcwd(),
        help="An existing, writeable output directory. In this folder, both the HTML and the web-ready images and thumbnails will be placed. Defaults to current working directory if omitted.",
    )
    parser.add_argument(
        "--thumbnails",
        action="store_true",
        help="Whether to generate and use thumbnails for the images.",
    )

    args = parser.parse_args()

    try:
        generate_gallery(
            indir=args.imgdir,
            outdir=args.outdir,
            use_thumbnails=args.thumbnails,
        )
    except ValueError as err:
        parser.error(str(err))


def generate_gallery(
    indir: str,
    outdir: str,
    use_thumbnails: bool = True,
    do_sort_by_aspect_ratio: bool = True,
) -> str:
    """
    Generate a static HTML gallery page from all images in the input directory and write it to the output directory.

    The images are copied (and scaled down, if necessary) into subdirectories of the output directory so that they are ready for the web. If ```use_thumbnails``` is True, smaller thumbnail copies are created as well and shown in the gallery, linking to the full-size web images.

    @param indir: Directory containing the input images.
    @param outdir: An existing, writeable output directory. The HTML page and the web-ready images and thumbnails will be placed in this folder.
    @param use_thumbnails: Whether to generate and use thumbnails. If True, the gallery shows thumbnails that link to the full-size web images; if False, the full-size web images are shown directly.
    @param do_sort_by_aspect_ratio: Whether to sort the images by aspect ratio in the gallery (all portrait images first, then landscape images).
    @return absolute path to the generated HTML file.
    @raise ValueError if the input or the output directory does not exist.
    """
    indir = os.path.abspath(indir)
    outdir = os.path.abspath(outdir)

    if not os.path.isdir(indir):
        raise ValueError(
            f"Input image directory '{indir}' does not exist or is not accessible. Please check."
        )

    if not os.path.isdir(outdir):
        raise ValueError(
            f"Output directory '{outdir}' does not exist or is not accessible. Please check."
        )
    if not os.access(outdir, os.W_OK | os.X_OK):
        logger.warning(f"Output directory '{outdir}' may not be writeable.")

    logger.info(f"Using input dir '{indir}' and output dir '{outdir}'.")

    outsubdirs: Dict[str, str] = {"images": os.path.join(outdir, outdir_subdir_img)}

    logger.info(
        f"Using full images for the web with dimension ({img_width_max}, {img_height_max})."
    )

    thumbnail_width_max = thumbnail_img_width_max
    thumbnail_height_max = thumbnail_img_height_max

    if use_thumbnails:
        outsubdirs["thumbnails"] = os.path.join(outdir, outdir_subdir_thumbnails)
        logger.info(
            f"Using thumbnails with dimension ({thumbnail_width_max}, {thumbnail_height_max})."
        )
    else:
        logger.info("Not using thumbnails.")

    for subdirname in outsubdirs.keys():
        sub_outdir = outsubdirs.get(subdirname)
        if not os.path.isdir(sub_outdir):
            os.mkdir(sub_outdir)
        else:
            logger.info(f"Output {subdirname} directory '{sub_outdir}' already exists.")

    image_filenames: List[str] = find_images([indir])
    logger.info(
        f"Found {len(image_filenames)} image files in directory '{indir}' with uppercased extensions '{handled_image_extensions}'."
    )

    if do_sort_by_aspect_ratio:
        logger.info("Sorting the images by aspect ratio.")
        image_filenames = sort_filenames_by_aspect_ratio(image_filenames)

    if len(image_filenames) == 0:
        logger.warning("No images found, please check the input directory setting.")

    web_image_filenames: List[str] = get_output_paths(
        image_filenames, outdir=outsubdirs["images"]
    )
    scale_images(
        image_filenames,
        web_image_filenames,
        max_width=img_width_max,
        max_height=img_height_max,
    )

    web_thumbnail_filenames: Union[List[str], None] = None
    if use_thumbnails:
        web_thumbnail_filenames = get_output_paths(
            image_filenames, outdir=outsubdirs["thumbnails"]
        )
        scale_images(
            image_filenames,
            web_thumbnail_filenames,
            max_width=thumbnail_width_max,
            max_height=thumbnail_height_max,
        )

    webpage: str = gen_full_webpage(image_filenames, thumbnails=web_thumbnail_filenames)
    output_html_file = os.path.join(outdir, outhtml_filename)
    with open(output_html_file, "w") as text_file:
        text_file.write(webpage)
    logger.info(
        f"Web gallery page for {len(image_filenames)} images written to file '{output_html_file}'"
    )

    return output_html_file


if __name__ == "__main__":
    main()
