# photowebpage
A simple Python script and command line application to generate a static HTML gallery page that displays all images in a directory in a web gallery. Intended for my personal use only. Ignore this.

## Features

* Implemented as a command line application
* Can scan a directory for suitable images, and one can apply some basic filters to use only a subset of the images in the target directory, e.g., filter by file formats or require a minimum size.
* Can generate thumbnails if requested, and show these thumbnails in the gallery (as links to the full-size images)
* Some simple convenience features, like sorting the images by aspect ratio in the output gallery (e.g., first all portrait orientation images, then all landscape orientation images)


## Installation

This is not on pip, so for now your only option is the developer installation. It requires Python, git and a shell (typically bash under Linux):

Clone this repo and change into your local copy:

```shell
git clone https://github.com/dfsp-spirit/photowebpage
cd photowebpage/
```

Then create a new virtual environment to isolate the installation from your system Python and install into it:

```shell
python -m venv .
source bin/activate
pip install -e .
```

You now have the ```photogallery``` command available. See the next section for information on how to use it.

## Usage

Type ```photogallery``` to see basic usage information.

An example command to search for images in the directory ```/testdata/input/chile```and write the output gallery to the directory ```./testdata/out``` would be:

```shell
photogallery --outdir ./testdata/out --thumbnails  ./testdata/input/chile
```

If you do not want thumbnails in the gallery, but want the full sized images in there directly, omit the ```--thumbnails```part of the command.

