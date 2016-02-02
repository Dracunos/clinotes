import argparse
import os
import re
import sys

if getattr(sys, 'frozen', False):
    path = os.path.dirname(sys.executable)
else:
    path = os.path.dirname(os.path.realpath(__file__))
notes_filepath = os.path.join(path, "clinote.txt")

parser = argparse.ArgumentParser()
action = parser.add_mutually_exclusive_group(required=True)
action.add_argument("--addnote",
                    help=("Add a note in quotes. Add at least one tag in "
                          "brackets (no spaces). Example: [note] This "
                          "is a note tagged 'note'."))
action.add_argument("--get",
                    help="Input a note tag or tags to find in quotes.")
action.add_argument("--getall",
                    help="Gets all notes.",
                    action='store_true')
action.add_argument("--getids",
                    help="Input tags, results include ids needed for deletion.")
action.add_argument("--getallids",
                    help="Gets all notes and includes ids.",
                    action='store_true')
action.add_argument("--delnote",
                    help="Input a note id for deletion.")
action.add_argument("--openfile",
                    help="Opens clinote.txt file with default editor.",
                    action='store_true')
args = parser.parse_args()


def find_tags(string):
    tags = re.findall(u"\[([a-zA-Z0-9\-_+=/\\'\"\:\;\.]+)\]", string)
    return [tag.lower() for tag in tags]

def get_notes(tag_list, note_obj):
    lines = note_obj.readlines()
    note_list = []
    for line in lines:
        split_line = line.split("-=-")
        try:
            note_num, text = split_line
        except ValueError:  # if split finds too many '-=-'s in the note
            note_num = split_line[0]
            text = "-=-".join(split_line[1:])
        tags = find_tags(text)
        tag_found = False
        for tag in tags:
            if tag in tag_list:
                tag_found = True
                break
        if tag_found:
            note_list.append((note_num, text))
    return note_list

def get_all_notes(note_obj):
    lines = note_obj.readlines()
    note_list = []
    for line in lines:
        split_line = line.split("-=-")
        try:
            note_num, text = split_line
        except ValueError:  # if split finds too many '-=-'s in the note
            note_num = split_line[0]
            text = "-=-".join(split_line[1:])
        note_list.append((note_num, text))
    return note_list

def print_notes(note_list, include_id):
    for note in note_list:
        if include_id:
            print "ID: {}".format(note[0])
        print note[1]
    if not note_list:
        print "No notes found."

if args.addnote:
    tags = find_tags(args.addnote)
    if not tags:
        print "You must add at least one tag inside equal-brackets (no spaces). Example: [note] This is a note tagged 'note'."
    else:
        with open(notes_filepath, 'a+') as notefile:
            try:
                last_note = get_all_notes(notefile)[-1]
                nl = '\n'
                if last_note[1][-1:] == "\n":
                    nl = ""
                last_note_id = int(last_note[0])
            except IndexError:
                nl = ""
                last_note_id = 0
            notefile.write(nl + str(last_note_id + 1) + "-=-" + args.addnote + "\n")
        print "Note successfully written."

elif args.get or args.getids:
    include_id = False
    get_tags = args.get
    if args.getids:
        include_id = True
        get_tags = args.getids
    splitter = " "
    if "," in get_tags:
        splitter = ", "
    tag_list = get_tags.split(splitter)
    try:
        with open(notes_filepath) as notefile:
            note_list = get_notes(tag_list, notefile)
    except IOError:
        note_list = []
    print_notes(note_list, include_id)

elif args.getall or args.getallids:
    include_id = False
    if args.getallids:
        include_id = True
    try:
        with open(notes_filepath) as notefile:
            note_list = get_all_notes(notefile)
    except IOError:
        note_list = []
    print_notes(note_list, include_id)

elif args.delnote:
    note = args.delnote
    note_deleted = False
    try:
        with open(notes_filepath) as notefile:
            lines = notefile.readlines()
    except IOError:
        lines = []
    with open(notes_filepath, "w+") as notefile:
        new_lines = []
        for line in lines:
            if line.split("-=-")[0] == note:
                note_deleted = True
            else:
                new_lines.append(line)
        notefile.writelines(new_lines)
    if note_deleted:
        print "Note successfully deleted."
    else:
        print "Note not found."

elif args.openfile:
    os.startfile(notes_filepath)