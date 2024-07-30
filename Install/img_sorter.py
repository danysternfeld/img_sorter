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
import os
import sys
import glob
import csv
import re
import shutil
import traceback

from cv2 import SUBDIV2D_PTLOC_OUTSIDE_RECT

def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c
    return glob.glob(''.join(map(either, pattern)))


def keepOpenIfNotDND(isDND):
    if(not isDND ):
        input("Press Enter to continue...")


def checkOverlap(min1,max1,min2,max2):
    if(
        (min2 >= min1 and min2<= max1) or
        (max2 >= min1 and max2 <= max1) or
        (min1 >= min2 and min1 <= max2) or
        (max1 >= min2 and max1 <= max2)
    ):
        return True
    else:
        return False

def parseCsv(infile):
    ranges = []
    csvfile =  open(infile, encoding="utf8")
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        for row in csvreader:
            if( not row[0].isnumeric()): continue
            classnum = int(row[0])
            split_images = row[1].split()
            images = []
            for img in split_images:
                images.append(int(img))
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
            # try to catch img counter reset    
            if(9999 - max < 100 and min < 100  ):
                new_ranges = splitRange(min,max)
                for r in new_ranges:
                    r.append(classnum)
                    ranges.append(r)
            # Try to catch typos such as 4452 454 ( ommision of a digit)
            elif(max - min > 1000):
                print(f"WARNING: Suspicios range {min}-{max}  - IGNORED")
            else:
                ranges.append([min,max,classnum])
    for range1 in ranges:
        for range2 in ranges:
            if(range1[0] == range2[0] and range1[1] == range2[1]): 
                continue
            if(checkOverlap(range1[0],range1[1],range2[0],range2[1])):
                raise Exception(f"Overlapping ranges in csv: range {range1[0]}-{range1[1]} overlapps {range2[0]}-{range2[1]}")
    return ranges         

# when a range crosses the 9999 boundary split it to two ranges
# For example:
# 9980-10 will become:
# 9980-9999
# 0-10
def splitRange(min,max):
    # swap min max
    min,max = max,min
    new_ranges = [[min,9999],[0,max]]
    print(f"Splitting range {min}-{max} to {min}-9999 and 0-{max}")
    return new_ranges
                  



def ParseCSVAndMoveFiles(infile):
    ranges = parseCsv(infile)
    for range in ranges:
        min = range[0]
        max = range[1]
        classnum = range[2]
        destdir = ".\\" + str(classnum)
        if(not os.path.exists(destdir)):
            os.makedirs(destdir)
        imgfiles = insensitive_glob("*.jpg")
        for imgfile in imgfiles:
            matchObj = re.search(r"\d+.jpg",imgfile)
            if(not matchObj == None):
                filenum = 0
                numOnlyMatch = re.search(r"\d+",matchObj.group())
                if(numOnlyMatch != None):
                    filenum = numOnlyMatch.group()
                if(int(filenum) >= int(min) and int(filenum) <= int(max)):
                    destfile = destdir+"\\"+imgfile
                    print("Moving " + imgfile + " to " +  destfile+ f" - range is {min}..{max}")
                    shutil.move(imgfile,destfile)


##########################################################
def ParseInfoTxt():
    info = open("info.txt",encoding="utf8")
    lines = info.readlines()
    matches = 0
    pattern = re.compile(r'(\d+)\D*(\d+)')
    folderDict  = dict()
    for line in lines:
        # קוד הפרק: 32899 - שם הפרק: פתיחה 1
        print(line,end = "")
        matchobj = pattern.search(line)
        if matchobj == None:
            continue
        matches += 1
        # skip the first match
        if matches == 1 :
            continue
        # class -> folder code
        if(not matchobj.group(2) in folderDict.keys()):
            folderDict[matchobj.group(2)] = matchobj.group(1)
    return folderDict




def ParseInfotxtAndMove():
    if(not os.path.exists("info.txt")):
        return
    folderDict = ParseInfoTxt()
    for classFolder in folderDict:
        if os.path.exists(classFolder):
            codeFolder = folderDict[classFolder]
            images = os.listdir(classFolder)
            for image in images :
                dstdir = codeFolder + "/Group/"
                if(not os.path.exists(dstdir)):
                    os.makedirs(dstdir)
                dstfile = dstdir + image
                srcFile = classFolder + "/" + image
                if os.path.exists(dstfile):
                    os.remove(dstfile)
                print("Moving " + srcFile + " to " + dstdir )
                shutil.move( srcFile, dstdir)
            print("Removing empty dir " + classFolder)    
            os.rmdir(classFolder)
            



def doDND():
    # this supports dropping a folder onto this script
    isDND = False    
    if(len(sys.argv) > 1 ):
        dir = sys.argv[1]
        os.chdir(dir)
        isDND = True
        # write a log file to the working dir
        sys.stdout =  open('img_sorter_out.txt', 'w', encoding='utf-8')
    return isDND
    
def ChooseModeAndRun():
    rootdir = os.getcwd()
    inputs = 0
    infile =  glob.glob('*.csv')    
    if(len(infile) > 1):
        raise Exception("more than one csv file in dir " + rootdir)
    if(len(infile) == 1):
        inputs += 1
        ParseCSVAndMoveFiles(infile[0])
    infile =  glob.glob('info.txt')
    if(len(infile) == 0) and inputs == 0 :
        raise Exception("No input csv or info.txt file in directory " + rootdir )
    ParseInfotxtAndMove()   


###############
#########  main
###############
try:
    isDND = doDND()
    ChooseModeAndRun()
    keepOpenIfNotDND(isDND)
except Exception as err:
    print(f"Unexpected ERROR:\n {err=}, {type(err)=}")
    print("error is: "+ traceback.format_exc())
    keepOpenIfNotDND(isDND)

                





