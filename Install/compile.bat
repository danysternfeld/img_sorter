cd ..
pyinstaller -F img_sorter.py
::pyinstaller -F install\add_EXE_to_explorer_menu.py
::pyinstaller -F install\remove_from_explorer_menu.py
copy dist\*.exe install\
cd install
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" ./installerScript.iss
del *.exe



