import time
import winreg as wrg 
import sys  
import os

location = wrg.HKEY_CURRENT_USER 
#img_sorter_path = find_img_sorter()
mypath = sys.argv[1] + r"\img_sorter.exe"
print(f"MYPATH = {mypath}")
if(not os.path.exists(mypath)):
    print("Could not find image sorter")
    time.sleep(2)
    #input("----->")
    sys.exit()
fullpath = os.path.abspath(mypath)    
command = f"{fullpath}  \"%V\""  

BGKey = wrg.OpenKeyEx(location, r"Software\Classes\Directory\Background\\") 
shellKey = wrg.CreateKey(BGKey, "Shell")
img_sort_key = wrg.CreateKey(shellKey, "Img Sorter")
cmdKey = wrg.CreateKey(img_sort_key, "Command") 
wrg.SetValueEx(cmdKey,None,0,wrg.REG_SZ,command)
wrg.SetValueEx(img_sort_key,"Icon",0,wrg.REG_SZ,fullpath)

