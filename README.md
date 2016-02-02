# clinotes
Simple cli notetaking app

    usage: clinotes.exe [-h]
                        (--addnote ADDNOTE | --get GET | --getall | --getids GETIDS | --getallids | --delnote DELNOTE | --openfile)
  
    optional arguments:
      -h, --help         show this help message and exit
      --addnote ADDNOTE  Add a note in quotes. Add at least one tag in brackets
                         (no spaces). Example: [note] This is a note tagged
                         'note'.
      --get GET          Input a note tag or tags to find in quotes.
      --getall           Gets all notes.
      --getids GETIDS    Input tags, results include ids needed for deletion.
      --getallids        Gets all notes and includes ids.
      --delnote DELNOTE  Input a note id for deletion.
      --openfile         Opens clinote.txt file with default editor.
    

This is my simple little tag-based notetaking command line app. Just stick the exe in a path folder for easy command line access.

It creates a clinote.txt file wherever you put it (once you start using it). I used python and cx_freeze. Only tested on Windows.
