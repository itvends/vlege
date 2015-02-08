#!/usr/bin/env python3
# vlege/vlege.py
# EugeneKay/vlege
#
# Vlege
#
# Vlege is a Very Low-Effort Gallery Engine, powering HTML image galleries
# based upon a native filesystem structure. Complicated server-side scripting
# languages and databases are eschewed in favor of basic HTML and JavaScript
# generated using a simple Python script and some helpful libraries.
#
# Copyright(c) 2014 Vlege Authors, including Eugene E. Kashpureff Jr.
# Licensed under GNU GPLv3+. See included README for more information
#


## Dependencies
# Basics
import os, sys
# Logging
import logging
# CLI friendliness
import argparse
# Image-handling
from PIL import Image
# Output templating
import jinja2

## Function definitions

def vlege(path=None, thumb=200, medium=1000):
    """Vlege-ize a path

    Keyword arguments:
    path -- path to be Vlege-ized
    thumb -- max pixel dimension of thumbnails
    medium -- max pixel dimension of mediums
    """

    ## Sanitize variables
    # Existance of path
    if not os.path.isdir(path):
        raise MyError("Invalid album path specified. Must be a directory.")

    # Size of thumb & mediums
    size={}
    size["thumb"]=(thumb,thumb)
    size["medium"]=(medium,medium)

    ## Processing loop
    # Walk filesystem hierarchy
    for root, dirs, files in os.walk(path):
        # Current directory
        logging.info("Directory: %s" % root)
        # Walk through subdirectories
        for subdir in dirs:
            logging.info("Subdir: %s" % subdir)

        # Walk through files listing
        for filename in files:
            # Full path to file
            filepath=root+"/"
            # Pull apart filename
            filesplit=os.path.splitext(filename)
            # Basic name of file
            filebase=filepath+filesplit[0]
            # Echo
            logging.info("File: "+filepath+filename)
            # Skip non-images
            if filesplit[1].lower() != ".jpg":
                logging.info("Skipped, not a jpg")
                continue
            # Skip already-processed
            if os.path.isfile(filebase+"-thumb.jpg"):
                logging.info("Skipped, thumb found")
                continue
            # Only process originals
            if "-medium" in filesplit[0] or "-thumb" in filesplit[0]:
                logging.info("Skipped, is a thumb/med")
                continue
            # Load file
            try:
                img = Image.open(filepath+filename)
            except IOError:
                logging.error("Could not open file")
                continue
            # Create+save a Thumbnail
            thumb = img.copy()
            try:
                thumb.thumbnail(size["thumb"])
                thumb.save(filebase+"-thumb.jpg")
            except IOError:
                logging.error("Could not create thumb")
            # Do we need a Medium?
            if img.size > size["medium"]:
                # Create+save a Medium
                try:
                    medium = img.copy()
                    medium.thumbnail(size["medium"])
                    medium.save(filebase+"-medium.jpg")
                except IOError:
                    logging.error("Could not create medium")

def main():
    ## Argument parsing
    # Initialize
    parser = argparse.ArgumentParser("vlege")

    # Enumerate args
    parser.add_argument("-v", "--verbose", action="store_true",
                            help="Increase output verbosity")
    parser.add_argument("album", help="Path to an album to be processed")

    # Annnd... parse!
    args = parser.parse_args()

    ## Output & Logging
    if args.verbose:
        # Verbose logging
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
        logging.info("Verbose output.")
    else:
        # Standard logging
        logging.basicConfig(format="%(levelname)s: %(message)s")

    vlege(path=args.album)

if __name__ == "__main__":
    sys.exit(main())
