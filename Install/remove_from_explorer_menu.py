import winreg as wrg 
import sys  
import os


def remove_recursive(key,Key2delete,deleteName):
    while True:
        try:
            # get kids
            subKeyName = wrg.EnumKey(Key2delete,0)
        except OSError:
            # no kids - safe to delete
            wrg.CloseKey(Key2delete)
            wrg.DeleteKey(key,deleteName)
            return  
        # recurse on kids      
        subKeyH = wrg.OpenKey(Key2delete,subKeyName)
        remove_recursive(Key2delete,subKeyH,subKeyName)

pyPath = sys.executable
location = wrg.HKEY_CURRENT_USER 
shellKey = wrg.OpenKeyEx(location, r"Software\Classes\Directory\Background\shell\\") 
keyName = "Img Sorter"
img_sort_key = wrg.CreateKey(shellKey, keyName)
remove_recursive(shellKey,img_sort_key,keyName)
