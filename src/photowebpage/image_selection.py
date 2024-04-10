
import logging

logger = logging.getLogger(__name__)

import os
from PIL import Image
from typing import Tuple, List, Union

handled_image_extensions : List[str] = ['JPG', 'JPEG', 'PNG']


def adjusted_size(current_width : int, current_height : int, max_width : int = 900, max_height : int = 900) -> Tuple[int, int]:
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


def find_images(paths : Union[List[str], str], image_extensions_uppercase : List[str] = handled_image_extensions) -> List[str]:
    """
    Find image files in path with one of the given file extensions.
    @param paths List of one or more directories to search for images. The search is not recursive.
    @param image_extensions_uppercase List of uppercase image file extensions to include. Typically something like ```['JPG', 'JPEG', 'PNG']```.
    @return the absolute paths to the detected images. The returned files existed when this function checked for existance. This of course does not imply that they still exist when the function returns.
    """
    images : List[str] = []

    if type(paths) is not list:
       paths = [paths]

    for path in paths:
      path = os.path.abspath(path)
      for img in os.listdir(path):
         fullname : str = os.path.join(path, img)
         if os.path.isfile(fullname):
            _, img_ext = os.path.splitext(img)
            if len(img_ext) > 0:
               img_ext = img_ext[1:].upper()
               if img_ext in image_extensions_uppercase:
                  images.append(fullname)

    return images

