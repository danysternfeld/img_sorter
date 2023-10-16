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

def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c
    return glob.glob(''.join(map(either, pattern)))


def keepOpenIfNotDND(isDND):
    if(not isDND ):
        input("Press Enter to continue...")

def ParseCSVAndMoveFiles(infile):
    csvfile =  open(infile)
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
                    print("Moving " + imgfile + " to " +  destfile)
                    shutil.move(imgfile,destfile)


##########################################################
def ParseInfoTxt():
    info = open("info.txt",encoding="utf-8")
    lines = info.readlines()
    matches = 0
    pattern = re.compile(r'(\d+).*(\d+)')
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
        folderDict[matchobj.group(2)] = matchobj.group(1)
    return folderDict




def ParseInfotxtAndMove():
    folderDict = ParseInfoTxt()
    for classFolder in folderDict:
        if os.path.exists(classFolder):
            codeFolder = folderDict[classFolder]
            if os.path.exists(codeFolder) :
                images = os.listdir(classFolder)
                for image in images :
                    dstdir = codeFolder + "/Group/"
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
        #dir = 'C:\\Users\\danys\\OneDrive\\Documents\\scripts\\img_sorter\\Pictures\\staging\\FTP'
        dir = sys.argv[1]
        os.chdir(sys.argv[1])
        os.chdir(dir)
        isDND = True
        # write a log file to the working dir
        sys.stdout =  open('img_sorter_out.txt', 'w', encoding='utf-8')
    return isDND
    
def ChooseModeAndRun():
    rootdir = os.getcwd()
    infile =  glob.glob('*.csv')
    if(len(infile) > 1):
        raise Exception("more than one csv file in dir ". rootdir)
    elif(len(infile) == 1):
        ParseCSVAndMoveFiles(infile[0])
    else:
        infile =  glob.glob('info.txt')
        if(len(infile) == 0):
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

                





