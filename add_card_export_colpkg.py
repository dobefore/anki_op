
from typing import Collection
from deserial import ChineseIdiom, GuHanYu
import tempfile,os,shutil
from pathlib import Path
from anki.collection import Collection as aopen
from anki.exporting import AnkiPackageExporter
def export_deck(col:Collection):
    e = AnkiPackageExporter(col)
    # write to Temp dir
    fd, newname = tempfile.mkstemp(prefix="ankitest", suffix=".apkg")
    newname = str(newname)
    print(newname)
    os.close(fd)
    os.unlink(newname)
    e.exportInto(newname)

    # cp file to desktop
    fname=Path(newname).parts[-1]
    shutil.copyfile(newname,Path(r'C:\Users\Admin\Desktop').joinpath(fname))
def add_cards_export_deck():
    nam=r'C:\Users\Admin\AppData\Roaming\Anki2\swjz\collection.anki2'
    col = aopen(nam)
    # create a new deck
    newId = col.decks.id("new_deck")
    # first must create a new note tyoe on anki,
    # then model name can be accessed
    m = col.models.by_name('Basic-0cc42')
    # choose deck for model by did
    m["did"] =newId
    col.models.save(m, updateReqs=False)
    # print deck id and name
    # print(col.decks.all_names_and_ids())
    note = col.new_note(m)
    # card field
    note["entry"] = "1"
    note["comment"] = '<img align="baseline" height="100" src="Images/image27372.jpeg" width="100"/>'
    col.addNote(note)
    
    export_deck(col)
def read_notes_from_sql(note_type: str,col_path: str):
    '''return note fields read from anki db limit
     to a certain note type'''
    col = aopen(col_path)
    m = col.models.by_name(note_type)
    mid=m.get("id")
    ids=col.db.all("select id from notes where mid=?",mid)
    n=0
    for i in ids:
        n+=1
        nt=col.getNote(i[0])
        fields=nt.values()
        fld_keys=nt.keys()
        
        # if n==50:
        #     break
        ci=GuHanYu(fields)
        tag=ci.tags()  
        print(tag)
        nt.add_tag(tag)
        nt.flush()
    export_deck(col)
    


nam=r'C:\Users\Admin\AppData\Roaming\Anki2\puyuan\collection.anki2'
read_notes_from_sql('基础-古汉语词典',nam)
