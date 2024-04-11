
import logging

logger = logging.getLogger(__name__)

import os
import PIL
from PIL import Image
from typing import Tuple, List, Union, NoReturn, Callable
from photowebpage.common import img_height_max, img_width_max

handled_image_extensions : List[str] = ['JPG', 'JPEG', 'PNG']


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


def find_images(paths : List[str], image_extensions_uppercase : List[str] = handled_image_extensions) -> List[str]:
    """
    Find image files in path with one of the given file extensions.
    @param paths List of one or more directories to search for images. The search is not recursive.
    @param image_extensions_uppercase List of uppercase image file extensions to include. Typically something like ```['JPG', 'JPEG', 'PNG']```.
    @return list of the absolute paths to the detected images. The returned files existed when this function checked for existance. This of course does not imply that they still exist when the function returns.
    """
    images : List[str] = []

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


def sort_filenames_by_image_dims(image_paths : List[str]):
   image_paths_sorted : List[str] = []

   for img_path in image_paths:
      image = Image.open(img_path)
      width, height = image.size

   return image_paths_sorted


def scale_images(image_paths : List[str], image_output_paths : List[str], max_width : int = img_width_max, max_height : int = img_height_max) -> None:
   """
   Create a scaled copy of the input images and save them in the output paths.
   @param image_paths: list of str, paths to the input images.
   @param image_output_paths: list of str, paths where to write the output images. Length must match that of image_paths. You can construct them using the ```get_output_paths``` function.
   @param max_width: maximal width of scaled image, in pixels
   @param max_height: maximal height of scaled image, in pixels
   """
   if len(image_paths) != len(image_output_paths):
      raise ValueError(f"Length of image_paths does not match length of image_output_paths.")

   for idx, img_path in enumerate(image_paths):
      image = Image.open(img_path)
      width, height = image.size
      w, h = _adjusted_img_size(width, height, max_width, max_height)
      image = image.resize((w, h))
      image.save(image_output_paths[idx])


def get_output_paths(img_input_paths : List[str], outdir : Union[str, None], overwrite : bool = False, suffix : Union[str, None] = None, prefix : Union[str, None] = None) -> str:
   """
   Determine output path for image, given input image and outdir or suffix.
   @param img_input_path: Paths to input images
   @param outdir: Output directory
   @param overwrite: Whether to overwrite the input file, i.e., simply return the img_input_path.
   @param suffix: A suffix to add to the filename, before the file extension, to make the output file different from the input file, if they both go into the same directory but you do not want to overwrite them. E.g., "_thumb" will turn the output for input "my_image.jpg" to "my_image_thumb.jpg".
   @param prefix: A prefix to add to the filename, to make the output file different from the input file, if they both go into the same directory but you do not want to overwrite them. E.g., "thumb_" will turn the output for input "my_image.jpg" to "thumb_my_image.jpg".
   @return list of output paths
   """
   if overwrite and (outdir is not None or suffix is not None or prefix is not None):
      raise ValueError("scale_images: If 'overwrite' is True, outdir, prefix and suffix must be set to None.")

   if outdir is None and suffix is None and prefix is None and not overwrite:
      raise ValueError("scale_images: If 'overwrite' is False, one of outdir, prefix or suffix must not be None.")

   out_paths = []

   for img_input_path in img_input_paths:

      img_filename = os.path.basename(img_input_path)

      if suffix:
         img_name, img_ext = os.path.splitext(img_filename)
         img_filename = img_name + suffix + img_ext

      if prefix:
         img_filename = prefix + img_filename

      img_out_path = img_input_path if overwrite else os.path.join(outdir, img_filename)
      out_paths.append(img_out_path)

   return out_paths

