# bethkit-wrapper
open bethesda game plugins directly in your default xml handler from win explorer for quick summary info and editing if you're really wild
Must run setup as admin. If the main script doesn't work and spits out a permission error you need to either grant folder and file permissions for the mod folder or run the script as admin. Disable UAC if you're a power user and want everything to run as admin if you are an admin account

version 1.0: 
nexus upload of initial version with registry tweaks delivered by setup tool, batch script wrapper, python script to dump edids to text. Only works in admin mode

version 2.0 (now):
rewrite in python and compile to exe. Added more parsers 

v2.5 maybe:
support data load from esp.json, support more parsing

version 3.0 planned:
remove bethkit.exe dependency. Replace using esper/esp.json repos by matortheeternal to write my own deserializer 

version 4.0 final:
implement custom structured text viewer/editor that I will hopefully have already made for other project by then
