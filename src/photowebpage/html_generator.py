"""
photowebpage.html_generator
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Functions to generate the static HTML code of the gallery web page from a list
of web-ready image file names. A full HTML page template with placeholders for
title and body is provided; the placeholders ```___TITLE___``` and
```___BODY___``` are filled in via simple text replacement.
"""

from typing import List, Union
import os
import logging
from photowebpage.common import outdir_subdir_img, outdir_subdir_thumbnails

logger = logging.getLogger(__name__)

# Full HTML page template. Title and body are inserted by replacing the
# placeholders ___TITLE___ and ___BODY___, respectively.
template = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html
     PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>___TITLE___</title>
  </head>
  <body>
    ___BODY___
  </body>
</html>"""


def get_html_page(title: str, body: str, template=template) -> str:
    """
    Return a full HTML page from the template, the title and the body.
    @param title: The HTML page title in the header section, displayed in the browser.
    @param body: The formatted HTML string forming the page body.
    @param template: The HTML page template.
    """
    page: str = template.replace("___TITLE___", title)
    page = page.replace("___BODY___", body)
    return page


def gen_gallery_html(
    images: List[str],
    thumbnails: Union[List[str], None] = None,
    image_subdir: str = outdir_subdir_img,
    thumbnail_subdir: str = outdir_subdir_thumbnails,
) -> str:
    """
    Generate the HTML code of the image gallery.

    Each image is embedded via an <img> tag. If thumbnails are provided, the
    thumbnail is shown wrapped in a link to the corresponding full-size image;
    otherwise the full-size image is shown directly.

    @param images: List of file names of the full-size (web-ready) images. Note that only the basename is used, so you can pass full or relative paths, but the path part will be ignored, because the images are assumed to be stored directly in ```image_subdir```. The images should be ready for the web, i.e., scaled and converted to a format that the browser can display, ideally at a suitable compression level.
    @param thumbnails: List of thumbnail file names, one per image, or None to not use thumbnails. If given, its length must match that of ```images```. As for ```images```, only the basename of each entry is used and the thumbnails are assumed to live in ```thumbnail_subdir```.
    @param image_subdir: Name of the directory (relative to the generated HTML file) that contains the full-size images.
    @param thumbnail_subdir: Name of the directory (relative to the generated HTML file) that contains the thumbnail images.
    @return the HTML code of the image gallery, as a string.
    """
    if thumbnails is not None:
        if len(thumbnails) != len(images):
            raise ValueError(
                f"Length of images and thumbnails must match. Pass None for thumbnails list if you do not have any."
            )
    outstr = ""
    for idx, img in enumerate(images):
        img_path_rel = os.path.join(
            image_subdir, os.path.basename(img)
        )  # Image path relative to location of generated HTML file.
        if thumbnails:
            thumb_path = os.path.join(
                thumbnail_subdir, os.path.basename(thumbnails[idx])
            )
            outstr += (
                "<a href='" + img_path_rel + "'>" + _img_tag(thumb_path) + "</a>" + "\n"
            )
        else:
            outstr += _img_tag(img_path_rel) + "\n"
    return outstr


def _img_tag(imgpath: str) -> str:
    """
    Generate an HTML <img> tag for the given image path.
    @param imgpath: The path to the image, e.g., relative to the generated HTML file.
    @return the HTML code of the <img> tag, as a string.
    """
    return "<img src='" + imgpath + "'></img>"


def gen_full_webpage(
    images: List[str],
    thumbnails: Union[List[str], None] = None,
    image_subdir: str = outdir_subdir_img,
    title: str = "Web Gallery",
) -> str:
    """
    Generate a complete, standalone HTML page showing the given images as a gallery.
    @param images: List of file names of the full-size (web-ready) images.
    @param thumbnails: List of thumbnail file names, one per image, or None to not use thumbnails. If given, the thumbnails will be shown and link to the full-size images.
    @param image_subdir: Name of the directory (relative to the HTML file) that contains the full-size images.
    @param title: The title of the HTML page, as shown in the browser title bar.
    @return the complete HTML code of the page, as a string.
    """
    gallery_html: str = gen_gallery_html(images, thumbnails, image_subdir=image_subdir)
    return get_html_page(title, body=gallery_html, template=template)
