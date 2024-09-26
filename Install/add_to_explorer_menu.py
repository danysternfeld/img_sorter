import winreg as wrg 
import sys  
import os

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None

def find_img_sorter():
    name = "img_sorter.py"
    our_location = os.path.dirname(os.path.abspath(__file__))
    places = [r"c:\program_files",fr"{our_location}\.."]
    for p in places:
        if(find(name,p)):
            return os.path.abspath(rf"{p}\{name}")
    return None    


# Store location of HKEY_CURRENT_USER 
pyPath = sys.executable
location = wrg.HKEY_CURRENT_USER 
img_sorter_path = find_img_sorter()
if(not img_sorter_path):
    print("Could not find image sorter")
    sys.exit()
command = f"{pyPath} {img_sorter_path}  \"%V\""  
# Store path in soft 
shellKey = wrg.OpenKeyEx(location, r"Software\Classes\Directory\Background\shell\\") 
img_sort_key = wrg.CreateKey(shellKey, "Img Sorter")
cmdKey = wrg.CreateKey(img_sort_key, "Command") 
wrg.SetValueEx(cmdKey,None,0,wrg.REG_SZ,command)
wrg.SetValueEx(img_sort_key,"Icon",0,wrg.REG_SZ,pyPath)

