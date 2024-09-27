import time
import winreg as wrg 
import sys  
import os

# def find(name, path):
#     for root, dirs, files in os.walk(path):
#         if name in files:
#             return os.path.join(root, name)
#     return None

# def find_img_sorter():
#     name = "img_sorter.exe"  
#     appdata = os.environ["APPDATA"]  
#     localappdata = appdata = os.environ["APPDATA"]
#     our_location = os.path.dirname(os.path.abspath(__file__))
#     places = [our_location,localappdata,appdata,r"C:\Program Files (x86)", r"c:\program files",fr"{our_location}\.."]
#     for p in places:
#         path = find(name,p)
#         if(path):
#             return os.path.abspath(rf"{path}")
#     return None    


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

