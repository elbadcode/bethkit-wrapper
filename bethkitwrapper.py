import os, sys, re, subprocess, shutil
import json
from lxml import etree as ET
from pathlib import Path
import tkinter as tk
from tkinter import filedialog


os.environ['bethkit'] = "C:\\Games\\Bethkit\\bethkit.exe"


#globals
def set_globals():
    validate_path()
    global script_path
    script_path = sys.argv[0]
    global file_path
    file_path = "\\."
    try:
        file_path = sys.argv[1]
        print(file_path)
    except Exception as e:
        print(e)

    global parent_path
    global file
    parent_path, file = str(file_path).rsplit('\\', 1)
    global name
    global ext
    name, ext = str(file).split('.')
    global temp_file
    temp_file = name + '.esx'
    global out_file
    out_file = name + '.xml'
    global summary
    summary = name + '-summary.txt'
    global summary2
    summary2 = name + '-regex.txt'

def ext_change(file_path, ext):
    try:
        return os.path.splitext(file_path)[0] + ext
    except TypeError:
        p = str(file_path).rsplit('.')[0] + ext
    return p


def validate_path():
    try:
        global bethkit
        bethkit = os.environ.get('bethkit', 'Not Set')
        if os.path.exists(bethkit):
            print('found bethkit')
            return True
        else:
            script_parent = os.path.dirname(sys.argv[0])
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
                subprocess.run(f'start "" "{out_file}"')
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

#parsed xml version

def parse_and_summarize():
    with open (summary, "a") as f:
        parse_vars = []
        try:
            with open(os.path.join(os.path.dirname(script_path), "parser_cfg.json"), "r") as conf:
                conf_json = json.load(conf)
                for var in conf_json["parsevars"]:
                    parse_vars.append(var)
        except Exception as e:
            print(e)
        edid_list = []
        mast_list = []
        var_list = []
        tree = ET.parse(out_file)
        root = tree.getroot()
        elems = tree.xpath('//MAST/text()')
        for master in elems:
            print(f"Master files:{master}")
            print(f"Master files:{master}", file=f)
        if len(parse_vars) >= 1:
            for parse_var in parse_vars:
                #sorry
                #reg = f"r'^(<{parse_var}(>(\\s|.+)?<| (.+))>)|(<{parse_var}>(.+)<)$'"
                reg = f"(<{parse_var}(>(\s|.+)?<| (.+))>)|(<{parse_var}>(.+)<)"
                reg = 'r\"' + reg + '\"'
                print(str(reg))
                get_edids(search_regex=str(reg))
                vars = root.iter(f'{parse_var}')
                for var_entry in vars:
                    var = var_entry.tag
                    text = var_entry.text
                    if text:
                        print(var)
                        print(f"{text}")
                        print(f"{text}", file=f)
        elif len(parse_vars) == 0 or parse_vars is null:
            print(f"EDIDs:")
            edids = root.iter('EDID')
            for edid_entry in edids:
                edid = edid_entry.values()
                if edid:
                    edid_list.append(edid)
                    print(edid)
                    print(edid, file=f)



#Regex version reads raw text without needing to interact with xml structure



def get_edids(search_regex):
    with open(summary2, "a") as log:
        xmlf = os.path.join(os.getcwd(), out_file)
        try:
            with open(xmlf,"r+", encoding='utf-8') as f:
                text = f.read()
                matches = re.finditer(search_regex, text, re.MULTILINE | re.IGNORECASE)
                for matchNum, match in enumerate(matches, start=1):
                    print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum,
                                                                                        start=match.start(),
                                                                                        end=match.end(),
                                                                                        match=match.group()),
                          file=log)
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1

                        print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                                        start=match.start(groupNum),
                                                                                        end=match.end(groupNum),
                                                                                        group=match.group(groupNum)),
                              file=log)
        except UnicodeDecodeError:
            try:
                with open(xmlf, "r+", encoding='cp1252') as f:
                    text = f.read()
                    matches = re.finditer(search_regex, text, re.MULTILINE | re.IGNORECASE)
                    for matchNum, match in enumerate(matches, start=1):
                        print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum,
                                                                                            start=match.start(),
                                                                                            end=match.end(),
                                                                                            match=match.group()),file=summary2)
                        for groupNum in range(0, len(match.groups())):
                            groupNum = groupNum + 1

                            print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                                            start=match.start(groupNum),
                                                                                            end=match.end(groupNum),
                                                                                            group=match.group(groupNum)), file=summary2)
            except UnicodeDecodeError:
                print("too many errors")
                print("too many errors", file=log)

def convert_xml_to_esx(path):
    parent_path = os.path.dirname(path)
    os.chdir(parent_path)
    esx = ext_change(path, '.esx')
    print(esx)
    return esx


def convert_to_esp(path):
    if path.endswith('.xml'):
        path = convert_xml_to_esx(path)
    p = Path(path)
    if p.exists():
        os.chdir(p.parent_path)
        os.makedir('output')
        out = ext_change(p, '.esp')
        out_path = os.path.join('output')
        out_file = os.path.join(out_path, out)
        subprocess.run("{bethkit} {path} {out_file}")

def draw_dnd_box():
    root = TkinterDnD.Tk()

    lb = tk.Listbox(root)
    lb.insert(1, "drag files to here")

    # register the listbox as a drop target
    lb.drop_target_register(DND_FILES)
    lb.dnd_bind('<<Drop>>', lambda e: lb.insert(tk.END, e.data))

    lb.pack()
    root.mainloop()


def main():
    if sys.argv:
        if len(sys.argv) == 1:
            try:
                arg = tk.filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=(('esp files', '*.esp'), ('esm files', '*.esm'), ('esl files', '*.esl'),('esx files', '*.esx'),('xml files', '*.xml')))
                if arg.endswith(('xml', 'esx')):
                    set_globals()
                    convert_to_esp(arg)
                elif arg.endswith(('esp', 'esl', 'esm')):
                    set_globals()
                    convert_to_xml()
                    parse_and_summarize()
            except Exception as e:
                print(e)
        else:
            try:
                for arg in sys.argv:
                    if arg.endswith(('xml','esx')):
                        set_globals()
                        convert_to_esp(arg)
                        break
                    elif arg.endswith(('esp','esl','esm')):
                        set_globals()
                        convert_to_xml()
                        parse_and_summarize()
                        break
            except Exception as e:
                print (e)


main()