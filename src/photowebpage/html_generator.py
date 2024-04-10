
from typing import List, Union
import os
import logging
from photowebpage.common import outdir_subdir_img, outdir_subdir_html

logger = logging.getLogger(__name__)

"""Template for the full HTML file. The title and body can be manipulated by using text replacement on the placeholders ```___TITLE___``` and ```___BODY___```, respectively."""
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


def get_html_page(title : str, body : str, template=template) -> str:
    """
    Return a full HTML page from the template, the title and the body.
    @param title: The HTML page title in the header section, displayed in the browser.
    @param body: The formatted HTML string forming the page body.
    @param template: The HTML page template.
    """
    page : str = template.replace("___TITLE___", title)
    page = page.replace("___BODY___", body)
    return page


def gen_gallery_html(images : List[str], thumbnails : Union[List[str], None] = None, image_subdir : str = outdir_subdir_img) -> str:
    """
    Generate the HTML for the gallery from the list of webready images.
    @param images: List of image file names. The images should be ready for the web, i.e., scaled and converted to a suitable format that browser can display. A suitable compression level, if supported by the format, may also come in handy.
    """
    if thumbnails is not None:
        if len(thumbnails) != len(images):
            raise ValueError(f"Length of images and thumbnails must match. Pass None for thumbnails list if you do not have any.")
    outstr = ""
    for idx, img in enumerate(images):
        img_path = os.path.join(image_subdir, img)
        if thumbnails:
            thumb_path = os.path.join(image_subdir, thumbnails[idx])
            outstr += "<a href='" + img_path + "'>" + _img_tag(thumb_path) + "</a>" + "\n"
        else:
            outstr += _img_tag(img_path) + "\n"
    return outstr

def _img_tag(imgpath : str) -> str:
    return "<img src='" + imgpath + "'></img>"

def gen_full_webpage(images : List[str], thumbnails : Union[List[str], None] = None, image_subdir : str = outdir_subdir_img, title : str = "Web Gallery") -> str:
    gallery_html : str = gen_gallery_html(images, thumbnails, image_subdir=image_subdir)
    return get_html_page(title, body=gallery_html, template=template)
