"""
photowebpage.image_selection
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Functions to find image files in a directory, sort them, and create scaled
copies (e.g., web-ready images or thumbnails) in an output directory.
"""

import logging
import os
import math
from typing import Tuple, List, Union, Dict
from PIL import Image
from photowebpage.common import img_height_max, img_width_max

logger = logging.getLogger(__name__)

handled_image_extensions: List[str] = ["JPG", "JPEG", "PNG"]


def _adjusted_img_size(
    current_width: int, current_height: int, max_width: int = 900, max_height: int = 900
) -> Tuple[int, int]:
    """
    Compute adjusted images size given current size and max size. Does only downscale or keep the current size, never suggests upscaling.
    """
    if current_width > max_width or current_height > max_height:
        if current_width > current_height:
            return max_width, int(max_width * current_height / current_width)
        else:
            return int(max_height * current_width / current_height), max_height
    else:
        return current_width, current_height


def find_images(
    paths: List[str], image_extensions_uppercase: List[str] = handled_image_extensions
) -> List[str]:
    """
    Find image files in path with one of the given file extensions.
    @param paths List of one or more directories to search for images. The search is not recursive.
    @param image_extensions_uppercase List of uppercase image file extensions to include. Typically something like ```['JPG', 'JPEG', 'PNG']```.
    @return list of the absolute paths to the detected images. The returned files existed when this function checked for existence. This of course does not imply that they still exist when the function returns.
    """
    images: List[str] = []

    for path in paths:
        path = os.path.abspath(path)
        for img in os.listdir(path):
            fullname: str = os.path.join(path, img)
            if os.path.isfile(fullname):
                _, img_ext = os.path.splitext(img)
                if len(img_ext) > 0:
                    img_ext = img_ext[1:].upper()
                    if img_ext in image_extensions_uppercase:
                        images.append(fullname)

    return images


def _calculate_aspect(width: int, height: int) -> Tuple[int, int]:
    """
    Calculate aspect ration of an image with the given width and height. E.g., 1920x1080 => (16, 9).
    """
    r = math.gcd(width, height)
    x: int = int(width / r)
    y: int = int(height / r)
    return x, y


def sort_filenames_by_aspect_ratio(image_paths: List[str]) -> List[str]:
    """
    Sort image filenames by aspect ratio of the image. Useful for the gallery because it looks bad if there is a random order of portrait format and landscape format images in the gallery. It looks much better if all portrait format images are followed by all landscape format images, or vice versa.
    @param image_paths: list of input image filenames. The images will be opened to check for dimensions and compute their aspect ratio, so the filenames must be valid image files.
    @return list of image filenames, containing the filenames from image_paths, but (potentially) in a different order.
    """
    images: List[Dict[str, Union[str, int, Tuple[int, int]]]] = []

    for img_path in image_paths:
        with Image.open(img_path) as image:
            width, height = image.size
        aspect_ratio: Tuple[int, int] = _calculate_aspect(width, height)
        images.append(
            {
                "img_path": img_path,
                "aspect_ratio": aspect_ratio,
                "width": width,
                "height": height,
            }
        )

    images.sort(key=lambda x: x["aspect_ratio"][0])  # Sort by width
    images.sort(
        key=lambda x: x["aspect_ratio"][1]
    )  # Sort by height within width order, works due to stable sort

    if logger.isEnabledFor(logging.INFO):
        aspect_ratios = [i["aspect_ratio"] for i in images]
        unique_aspect_rations = list(set(aspect_ratios))
        logger.info(
            f"The {len(image_paths)} images have {len(unique_aspect_rations)} different aspect ratios: {unique_aspect_rations}."
        )

    if logger.isEnabledFor(logging.DEBUG):
        for img in images:
            logger.debug(
                f"Image '{img.get('img_path')}' has dimension ({img.get('width')}, {img.get('height')}) and aspect ratio {img.get('aspect_ratio')[0]}:{img.get('aspect_ratio')[1]}."
            )

    return [i["img_path"] for i in images]


def scale_images(
    image_paths: List[str],
    image_output_paths: List[str],
    max_width: int = img_width_max,
    max_height: int = img_height_max,
) -> None:
    """
    Create a scaled copy of the input images and save them in the output paths.
    @param image_paths: list of str, paths to the input images.
    @param image_output_paths: list of str, paths where to write the output images. Length must match that of image_paths. You can construct them using the ```get_output_paths``` function.
    @param max_width: maximal width of scaled image, in pixels
    @param max_height: maximal height of scaled image, in pixels
    """
    if len(image_paths) != len(image_output_paths):
        raise ValueError(
            f"Length of image_paths does not match length of image_output_paths."
        )

    for idx, img_path in enumerate(image_paths):
        with Image.open(img_path) as image:
            width, height = image.size
            w, h = _adjusted_img_size(width, height, max_width, max_height)
            resized_image = image.resize((w, h))
        resized_image.save(image_output_paths[idx])


def get_output_paths(
    img_input_paths: List[str],
    outdir: Union[str, None],
    overwrite: bool = False,
    suffix: Union[str, None] = None,
    prefix: Union[str, None] = None,
) -> List[str]:
    """
    Determine the output paths for the given input images, based on outdir, prefix, suffix and overwrite.

    @param img_input_paths: Paths to input images.
    @param outdir: Output directory. If None, the output images will be written next to their respective input images, which only makes sense if 'overwrite' is False and 'suffix' and/or 'prefix' is given (otherwise input and output paths would be identical).
    @param overwrite: Whether to overwrite the input file, i.e., simply return the img_input_path.
    @param suffix: A suffix to add to the filename, before the file extension, to make the output file different from the input file, if they both go into the same directory but you do not want to overwrite them. E.g., "_thumb" will turn the output for input "my_image.jpg" to "my_image_thumb.jpg".
    @param prefix: A prefix to add to the filename, to make the output file different from the input file, if they both go into the same directory but you do not want to overwrite them. E.g., "thumb_" will turn the output for input "my_image.jpg" to "thumb_my_image.jpg".
    @return list of output paths, one per input path, in the same order as in ```img_input_paths```.
    """
    if overwrite and (outdir is not None or suffix is not None or prefix is not None):
        raise ValueError(
            "get_output_paths: If 'overwrite' is True, outdir, prefix and suffix must be set to None."
        )

    if outdir is None and suffix is None and prefix is None and not overwrite:
        raise ValueError(
            "get_output_paths: If 'overwrite' is False, one of outdir, prefix or suffix must not be None."
        )

    out_paths = []

    for img_input_path in img_input_paths:

        img_filename = os.path.basename(img_input_path)

        if suffix:
            img_name, img_ext = os.path.splitext(img_filename)
            img_filename = img_name + suffix + img_ext

        if prefix:
            img_filename = prefix + img_filename

        if overwrite:
            img_out_path = img_input_path
        elif outdir is not None:
            img_out_path = os.path.join(outdir, img_filename)
        else:
            # No outdir given: write the output next to the input image so that
            # the prefix/suffix can still produce a distinct filename.
            img_out_path = os.path.join(os.path.dirname(img_input_path), img_filename)
        out_paths.append(img_out_path)

    return out_paths
