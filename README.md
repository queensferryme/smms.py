# smms.py

## Introduction

Python package `smms.py` is a command line toolkit for managing images at [https://sm.ms](https://sm.ms). It provides simple and quick utilities for you to upload, delete and search personal images.

## Usage

### install

Simply install with one line command `pip install smms.py`.

### delete

Deleting images from [https://sm.ms](https://sm.ms) are sort of frustrating. But thanks to the official API, we have access to remove images from the server.

```bash
smms delete --help
# Usage: smms d [OPTIONS] [FILENAMES]...
#   delete images from remote server & clean local history
# Options:
#   -c, --comment TEXT  wildcard statement for matching commentations
#   -d, --date TEXT     one or more date strings like "yyyy-mm-dd" to specify
#                       search scope
#   -y, --yes           delete without confirmation
#   --help              Show this message and exit.
smms delete "*t*" -d 2001-01-01
# Delete all images with a letter "t" in filename uploaded on 2001-01-01
```

You can use `filename`, `comment` & `date` to narrow down the scope. You will also be required to confirm deletion out of security consideration.

### upload

Uploading images to [https://sm.ms](https://sm.ms) is pretty simple when using `smms.py`. For instance:

```bash
smms upload --help
# Usage: smms upload [OPTIONS] FILENAME
#   upload images & insert new records into local history
# Options:
#   -c, --comment TEXT  commentation string for images
#   --help              Show this message and exit.
smms upload $HOME/images/*.jpg -c 'example upload'
# upload all jpg-format images in ~/images/ and comment them
```

### search

Command `search` enables you to search and view your local history. Yet another example:

```bash
smms search --help
# Usage: smms s [OPTIONS] [FILENAMES]...
#   search for matched records in local history
# Options:
#   -c, --comment TEXT  wildcard statement for matching commentations
#   -d, --date TEXT     one or more date strings like "yyyy-mm-dd" to specify
#                       search scope
#   --help              Show this message and exit.
smms search "*.jpg" -c "*backup*"
# Search for all jpg-format images commented with 'backup'
```

### migrate

```bash
smms migrate --help
# Usage: smms migrate [OPTIONS]
#   migrate local history from version 0.0.2 to 1.0.0
# Options:
#   --help  Show this message and exit.
```

Help to migrate your old version local history.

## Change Log

- version `1.0.0`  
    Project refactoring, Default comment string has change from `'--- NO COMMENT ---'` to `''`
- version `0.0.1`  
    Fix color issue under windows platform
- version `0.0.0`  
    initial version

## About

If you have any suggestions, please email me at *queensferry.me@gmail.com*. Pull & Request is also welcome.
