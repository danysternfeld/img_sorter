import os
import sys
import glob
import csv
import re
import shutil
# usage: chdir to image directory. Place csv file there. run without arguments
# OR: drag a folder onto this script

def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c
    return glob.glob(''.join(map(either, pattern)))

# this supports dropping a folder onto this script
if(len(sys.argv) > 1):
    os.chdir(sys.argv[1])
    # write a log file to the working dir
    sys.stdout =  open('img_sorter_out.txt', 'w')
    
 

rootdir = os.getcwd()
infile =  glob.glob('*.csv')
if(len(infile) > 1):
    raise Exception("more than one csv file in dir ". rootdir)
with open(infile[0]) as csvfile:
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
        for imgfile in imgfiles:
            matchObj = re.search("\d+",imgfile)
            if(not matchObj == None):
                filenum = matchObj.group()
                print("filenum="+filenum)
                if(int(filenum) >= int(min) and int(filenum) <= int(max)):
                    destfile = destdir+"\\"+imgfile
                    print("Moving " + imgfile + " to "+  destfile)
                    shutil.move(imgfile,destfile)


            





