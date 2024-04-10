
import logging

logger = logging.getLogger(__name__)

import os
from PIL import Image
from typing import Tuple, List, Union, NoReturn, Callable


def _adjusted_img_size(current_width : int, current_height : int, max_width : int = 900, max_height : int = 900) -> Tuple[int, int]:
   """
   Compute adjusted images size given current size and max size. Does only downscale or keep the current size, never suggests upscaling.
   """
   if current_width > max_width or current_height > max_height:
      if current_width > current_height:
         return max_width, int (max_width * current_height / current_width)
      else:
         return int (max_height * current_width / current_height), max_height
   else:
      return current_width, current_height


def find_images(path : str, extensions_uppercase : List[str] = ['JPG', 'JPEG', 'PNG']) -> List[str]:
    """
    Find image files in path with one of the given file extensions.
    @return the absolute paths to the images. The returned files existed when this function checked for existance. This of course does not imply that they still exist when the function returns.
    """
    images : List[str] = []
    for img in os.listdir(path):
      fullname : str = os.path.join(path, img)
      if os.path.isfile(fullname):
         _, img_ext = os.path.splitext(img)
         if len(img_ext) > 0:
            img_ext = img_ext[1:].upper()
            if img_ext in extensions_uppercase:
                images.append(fullname)
    return images


def scale_images(image_paths : List[str], outdir : str, max_width : int = 900, max_height : int = 900 , overwrite = False) -> NoReturn:


   for img_path in image_paths:
    img_out_path = _get_output_path(img_path, outdir, overwrite)

    image = Image.open(img_path)
    width, height = image.size
    image = image.resize(_adjusted_img_size(width, height, max_width, max_height))
    image.save(img_out_path)


def _get_output_path(img_input_path, outdir : str, overwrite : bool = False) -> str:
    if overwrite and outdir is not None:
      raise ValueError("scale_images: If 'overwrite' is True, outdir must be set to None.")
     if outdir is None and not overwrite:
      raise ValueError("scale_images: If 'overwrite' is False, outdir must not be None.")

    img_filename = os.path.basename(img_input_path)
    img_out_path = img_input_path if overwrite else os.path.join(outdir, img_filename)
    return img_out_path

