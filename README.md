# Copyright 2023 by Dany Sternfeld.
# All rights reserved.
#
# This script does two things:
# 1) uses a csv file to sort images in a folder into their own folders,
# to ease the upload process of images to TotalPrint
# Here's a sample csv:
# תמונות , כיתה  
# 1,	1236 1235
# 2,	2345
# 3,	456 458
#
# first column is the class number and the second column is either one image number or
# a range of image numbers.
#
#
# 2) In the upload staging area in the FTP dir, it uses info.txt to move files from class dirs
# numbered 1,2,3,4 to coded dirs, e.g 3901 etc..
# place sorted dirs from the previos step in the FTP dir and drag it to the script.
#
# 1 and 2 can be combined - place info,txt and csv file in image directory and
# the final directories will be created.
#
# usage: chdir to image directory with a cvs file or FTP directory. Run without arguments
# OR: drag a folder onto this script
#
# to enable drag and drop in windows, make sure .py files are
# associated with python and add this reg key:
# [HKEY_CLASSES_ROOT\Python.File\shellex\DropHandler]
# @="{60254CA5-953B-11CF-8C96-00AA00B8708C}"
#
# When drag and drop is used, a log file is written to the dropped folder.
