import os, sys, re, subprocess
import ctypes
from lxml import etree as ET


#globals
script_path = sys.argv[0]
#note if you add bethkit to path properly you should be able to call 'bethkit' from anywhere
file_path = sys.argv[1]
print(file_path)
parent_path, file = str(file_path).rsplit('\\', 1)
name, ext = str(file).split('.')
temp_file = name + '.esx'
out_file = name + '.xml'
summary = name + '-summary.txt'


def validate_path():
    try:
        global bethkit
        bethkit = "C:\\Games\\Bethkit\\bethkit.exe"
        if os.path.exists(bethkit):
            print('found bethkit')
            return True
        else:
            script_parent = os.path.dirname(sys.argv[1])
            bethkit = os.path.join(script_parent, "bethkit.exe")
    except FileNotFoundError:
        print('did not find bethkit, reinstall')
        return False


def is_elevated():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def convert_to_xml():
    if validate_path():
        if os.path.exists(out_file):
            os.system(f"start {out_file}")
            return
        os.chdir(parent_path)
        subprocess.run(f'{bethkit} convert "{file}" "{name}.esx"')
        try:
            os.rename(temp_file, out_file)
            try:
                print("Done conversion")
                subprocess.run(f'start "{out_file}"')
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

#parsed xml version

def parse_and_summarize():
    with open (summary, "w") as f:
        edid_list = []
        mast_list = []
        tree = ET.parse(out_file)
        root = tree.getroot()
        elems = tree.xpath('//MAST/text()')
        for master in elems:
            print(f"Master files:{master}")
            print(f"Master files:{master}", file=f)
        params = tree.xpath(f'//GRUP')
        print(f"EDIDs:")
        for param in params:
            edids = param.findall('.//EDID')
            for edid_entry in edids:
                edid = edid_entry.values()
                if edid:
                    edid_list.append(edid)
                    print(edid)
                    print(edid, file=f)



#Regex version reads raw text without needing to interact with xml structure

edid_regex = r"<EDID>(.+)<"

def get_edids():
    with open(summary, "a") as log:
        xmlf = os.path.join(os.getcwd(), out_file)
        try:
            with open(xmlf,"r+", encoding='utf-8') as f:
                text = f.read()
                all_lines = re.findall(edid_regex, text, re.MULTILINE)
                print(all_lines)
                for line in all_lines:
                    print(f"{line}",file=log)
        except UnicodeDecodeError:
            try:
                with open(xmlf, "r+", encoding='cp1252') as f:
                    text = f.read()
                    all_lines = re.findall(edid_regex, text, re.MULTILINE)
                    print(all_lines)
                    for line in all_lines:
                        print(f"{line}", file=log)
            except UnicodeDecodeError:
                print("too many errors")
                print("too many errors", file=log)





def main():
    convert_to_xml()
    parse_and_summarize()
    get_edids()


#   if is_elevated():
#       convert_to_xml()
#      parse_and_summarize()
#      get_edids()

# else:
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

main()