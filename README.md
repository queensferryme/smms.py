# smms.py

[TOC]

## Introduction

Python package `smms.py` is a command line toolkit for managing images at [https://sm.ms](https://sm.ms). It provides simple and quick utilities for you to upload, delete and query personal images.

## Usage

### install

The installation procedure could easily be done with `pip`. For exmaple: `pip install smms.py`.

### upload

Uploading images to [https://sm.ms](https://sm.ms) is pretty simple when using command `smms`. For instance:

```bash
smms upload --help
# Usage: smms upload [OPTIONS] [IMAGES]...
# Upload images and record commits, shell-style wildcards supported
# Options:
# -c, --comment TEXT  commentation strings, making comments for images
# --help              Show this message and exit.
smms upload $HOME/images/*.jpg -c 'example upload'
# upload all jpg-format images in ~/images/ and comment them
```

### delete

Deleting images on [https://sm.ms](https://sm.ms) directly on browsers are sort of complicated. But thanks to the official API, we have access to remove images from the server.

```bash
smms delete --help
# Usage: smms delete [OPTIONS]
# Remove specific images from server
# Options:
# -A, --All           ALL flag, indicating deleting all images
# -d, --dates TEXT    ISO date strings, specifying dates to delete
# -p, --pattern TEXT  Search pattern, like <property>:<shell-style wildcards>
# --yes               Confirm delete events
# --help              Show this message and exit.
smms delete -d 2001-01-01 -d 2018-06-26 -A
# Delete all images uploaded on 2001-01-01 or 2018-06-26
smms remove -A -p 'filename:bak_*.jpg'
# Delete all backup jpg-format images
```

It works pretty well. For match patterns, you have four properties to choose from on hand: `filename`, `url`, `delete ` and `comment`. You may view `~/.sm.ms.history` for clearer comprehension.

### query

Command `query` enables you to filter and view your local history. Yet another example:

```bash
smms query --help
#Usage: smms query [OPTIONS]
# Query records from local history
# Options:
# -d, --dates TEXT    ISO date strings, specifying dates to query
# -p, --pattern TEXT  Search pattern, like <property>:<shell-style wildcards>
# --help              Show this message and exit.
smms query -d 2018-06-26 -d 2018-06-27 -p 'comment:backup*'
# Query all images uploaded in dates above commented with 'backup'
```



## About

If you have any suggestions, please email me at *queensferry.me@gmail.com*.
