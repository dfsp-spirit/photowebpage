# photowebpage
A simple Python script to generate a static HTML page that displays all images in a directory. Intended for my personal use only. Ignore this.


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


## Usage

```shell
photogallery --outdir ./testdata/out --thumbnails  ./testdata/input/chile
```
