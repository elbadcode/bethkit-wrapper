import os
import sys
import re

name = str(sys.argv[1])
outpath = os.path.abspath(str(sys.argv[2]).split('"')[1])
noext = os.path.splitext(name)[0]
regex = r"<EDID>(.+)<"
out_name = str(name).split('.')[0]+"edids.txt"
out_f = os.path.join(outpath, out_name)

def main():
	with open(out_f, "w") as log:
		xmlf = os.path.join(os.getcwd(), name)
		try:
			with open(xmlf,"r+", encoding='utf-8') as f:
				text = f.read()
				all_lines = re.findall(regex, text, re.MULTILINE)
				print(all_lines)
				for line in all_lines:
					print(f"{line}",file=log)
		except UnicodeDecodeError:
			try:
				with open(xmlf, "r+", encoding='cp1252') as f:
					text = f.read()
					all_lines = re.findall(regex, text, re.MULTILINE)
					print(all_lines)
					for line in all_lines:
						print(f"{line}", file=log)
			except UnicodeDecodeError:
				print("too many errors", file=log)





main()