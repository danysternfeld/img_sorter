# Copyright 2023 by Dany Sternfeld.
# All rights reserved.
#
# This script uses a csv file to sort images in a folder into their own folders,
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
# usage: chdir to image directory. Place csv file there. run without arguments
# OR: drag a folder onto this script
#
# to enable drag and drop in windows, make sure .py files are
# associated with python and add this reg key:
# [HKEY_CLASSES_ROOT\Python.File\shellex\DropHandler]
# @="{60254CA5-953B-11CF-8C96-00AA00B8708C}"
#
# When drag and drop is used, a log file is written to the dropped folder.

import os
import sys
import glob
import csv
import re
import shutil
import traceback

def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c
    return glob.glob(''.join(map(either, pattern)))


def keepOpenIfNotDND():
    if(not isDND):
        input("Press Enter to continue...")

try:
    # this supports dropping a folder onto this script
    isDND = False
    if(len(sys.argv) > 1):
        os.chdir(sys.argv[1])
        # write a log file to the working dir
        sys.stdout =  open('img_sorter_out.txt', 'w')
        isDND = True
        
    

    rootdir = os.getcwd()
    infile =  glob.glob('*.csv')
    if(len(infile) > 1):
        raise Exception("more than one csv file in dir ". rootdir)
    elif(len(infile) == 0):
        raise Exception("No input csv file in directory " + rootdir )
    csvfile =  open(infile[0])
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if( not row[0].isnumeric()): continue
        print(row)
        classnum = row[0]
        images = row[1].split()
        min = 0
        max = 9999
        if(len(images) > 1):
            if(images[0] > images[1]):
                min = images[1]
                max = images[0]
            else:
                min = images[0]
                max = images[1]
        else:
            min = images[0]
            max = min
        destdir = ".\\" + classnum
        if(not os.path.exists(destdir)):
            os.makedirs(destdir)
        imgfiles = insensitive_glob("img*")
        # if no 'img* files found, try jpg's
        if(len(imgfiles) == 0):
            imgfiles = insensitive_glob("*.jpg")
        for imgfile in imgfiles:
            matchObj = re.search("\d+",imgfile)
            if(not matchObj == None):
                filenum = matchObj.group()
                if(int(filenum) >= int(min) and int(filenum) <= int(max)):
                    destfile = destdir+"\\"+imgfile
                    print("Moving " + imgfile + " to "+  destfile)
                    shutil.move(imgfile,destfile)
                    keepOpenIfNotDND()
except Exception as err:
    print(f"Unexpected ERROR:\n {err=}, {type(err)=}")
    print("error is: "+ traceback.format_exc())
    keepOpenIfNotDND()

                





