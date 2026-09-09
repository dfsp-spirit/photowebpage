"""
Integration tests for the gallery generation pipeline (photowebpage.cli.generate_gallery).

These tests exercise the full pipeline on real image files. One of them writes a
sample gallery for the Chile test images into the gitignored directory
'testdata/out' so it can be opened and inspected in a browser.
"""

import os
import shutil

from PIL import Image

from photowebpage.cli import generate_gallery
from photowebpage.common import (
    outhtml_filename,
    outdir_subdir_img,
    outdir_subdir_thumbnails,
)

# Repository root (the parent of the 'tests' directory).
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _write_test_image(img_path, width, height):
    """Create a small solid-color test image at img_path."""
    image = Image.new("RGB", (width, height), color=(200, 30, 30))
    image.save(img_path)


def _clean_generated_output(outdir):
    """Remove previously generated gallery output from outdir (keeps other files, e.g. README)."""
    index_html = os.path.join(outdir, outhtml_filename)
    if os.path.exists(index_html):
        os.unlink(index_html)
    for subdir in (outdir_subdir_img, outdir_subdir_thumbnails):
        sub_outdir = os.path.join(outdir, subdir)
        if os.path.isdir(sub_outdir):
            shutil.rmtree(sub_outdir)


def test_generate_gallery_with_thumbnails(tmp_path):
    """A small gallery in a temp dir: thumbnails must be shown, linking to the full-size images."""
    indir = tmp_path / "input"
    outdir = tmp_path / "out"
    indir.mkdir()
    outdir.mkdir()
    _write_test_image(indir / "a_portrait.jpg", 30, 50)
    _write_test_image(indir / "b_landscape.jpg", 60, 40)
    _write_test_image(indir / "c_square.jpg", 40, 40)

    html_path = generate_gallery(str(indir), str(outdir), use_thumbnails=True)

    assert html_path == str(outdir / outhtml_filename)
    assert os.path.isfile(html_path)

    img_dir = outdir / outdir_subdir_img
    thumb_dir = outdir / outdir_subdir_thumbnails
    assert len(os.listdir(img_dir)) == 3
    assert len(os.listdir(thumb_dir)) == 3

    with open(html_path) as html_file:
        html = html_file.read()
    assert html.count("<a href='img/") == 3
    assert html.count("<img src='thumbnails/") == 3

    # Written files must be readable images.
    for img_path in list(img_dir.iterdir()) + list(thumb_dir.iterdir()):
        with Image.open(img_path) as image:
            image.verify()


def test_generate_gallery_without_thumbnails(tmp_path):
    """Without thumbnails, the full-size images must be shown directly."""
    indir = tmp_path / "input"
    outdir = tmp_path / "out"
    indir.mkdir()
    outdir.mkdir()
    _write_test_image(indir / "a.jpg", 30, 50)
    _write_test_image(indir / "b.jpg", 60, 40)

    html_path = generate_gallery(str(indir), str(outdir), use_thumbnails=False)

    assert os.path.isfile(html_path)

    img_dir = outdir / outdir_subdir_img
    assert len(os.listdir(img_dir)) == 2
    assert not (outdir / outdir_subdir_thumbnails).exists()

    with open(html_path) as html_file:
        html = html_file.read()
    assert html.count("<img src='img/") == 2
    assert "<a href=" not in html


def test_generate_chile_sample_gallery_in_testdata_out():
    """
    Write a sample gallery for the Chile test images into 'testdata/out'.

    This test doubles as a demo generator: run pytest and then open the file at
    '<repo>/testdata/out/index.html' in a browser to inspect the result.
    """
    indir = os.path.join(REPO_ROOT, "testdata", "input", "chile")
    outdir = os.path.join(REPO_ROOT, "testdata", "out")

    if not os.path.isdir(indir):
        raise AssertionError(f"Input test images not found at '{indir}'.")
    os.makedirs(outdir, exist_ok=True)

    _clean_generated_output(outdir)

    html_path = generate_gallery(indir, outdir, use_thumbnails=True)

    assert html_path == os.path.join(outdir, outhtml_filename)
    assert os.path.isfile(html_path)

    with open(html_path) as html_file:
        html = html_file.read()

    img_dir = os.path.join(outdir, outdir_subdir_img)
    thumb_dir = os.path.join(outdir, outdir_subdir_thumbnails)
    n_img_files = len(os.listdir(img_dir))
    n_thumb_files = len(os.listdir(thumb_dir))

    expected = len(
        [f for f in os.listdir(indir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    )
    assert expected > 0
    assert n_img_files == expected
    assert n_thumb_files == expected
    # The gallery must show thumbnails that link to the full-size images.
    assert html.count("<a href='img/") == expected
    assert html.count("<img src='thumbnails/") == expected

    print(f"\nSample gallery written to: {html_path}")
