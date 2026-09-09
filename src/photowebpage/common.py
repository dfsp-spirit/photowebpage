"""
photowebpage.common
~~~~~~~~~~~~~~~~~~~

Shared settings (output folder and file names as well as the maximum image
dimensions) used by the other modules of the photowebpage package.
"""

# ----- Settings -----

# Output paths and filenames
outdir_subdir_html: str = "html"
outdir_subdir_img: str = "img"
outdir_subdir_thumbnails: str = "thumbnails"
outhtml_filename: str = "index.html"

# Output Image dimensions in pixels
img_height_max: int = 1000
img_width_max: int = 1000
thumbnail_img_height_max: int = 400
thumbnail_img_width_max: int = 400
