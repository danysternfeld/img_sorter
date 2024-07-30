import winreg
import os
import sys
import win32com.client

    # find the desktop
with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as key:
    # Extracted string may contain unexpanded environment variables, such as "%USERPROFILE%\Desktop"
    desktop_dir, _ = winreg.QueryValueEx(key, "Desktop")
    # To expand the environment variable in the above string, use this form
    desktop_dir = os.path.expandvars(winreg.QueryValueEx(key, "Desktop")[0])
    print("User desktop located in ",desktop_dir)

    #  Create shortcut
    target = os.getcwd() + r"\img_sorter.py"
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(desktop_dir + "/Sort Photos.lnk")
    shortcut.Targetpath = target
    shortcut.save()
    
  
    
  