
from sys import settrace
from anki.collection import Collection
from anki.notes import Note
def get_capital_alphabet(pinyin: str):
        cap=pinyin[0]
        e={ 'è','ē','ě', 'é'}
        a={'à', 'ǎ', 'á', 'ā',}
        o={  'ǒ','ō','ò'}
        if cap in a:
            cap='a'
        elif cap in o:
            cap='o'
        elif cap in e:
            cap='e'
        if not cap.isascii():
            print(cap)
            raise f'capital is non ascii'
        return cap
class ChineseIdiom(object):
    '成语大全'
    def __init__(self,items: dict):
      self.py=items[0]
      self.entry=items[1]
      self.category=items[3]
      self.synonym=items[4]
      self.antonym=items[5]
      self.source=items[6]
      self.trans=items[7]
    
    def tags(self)->str:
        capital_py=get_capital_alphabet(self.py)
        if self.category!='':
        # only fisrt 2 seg in cate
            segs=self.category.split('-')[:2]
            cat='_'.join(segs)
            return f'{capital_py} {cat}'
        else:
            return f'{capital_py }'
class GuHanYu(object):
    '古汉语词典'
    def __init__(self,items: dict[str]):
        'multi tone/pinyin'
        self.items=items
        self.py1=items[1]
        self.py2=items[3]
        self.py3=items[5]
        self.py4=items[7]
        self.py5=items[9]
        self.pys=[items[1],items[3],items[5],items[7],items[9]]
    def fix_filed_mismatch(self,keys: list[str],nt:Note):
        # record py field key 
        py_keys=keys
        err_py_keys=[]
        cont=''
        # accum field content from 【】py field
        for item in py_keys:
            py_ctt=nt[item]
            if '【' in py_ctt and '】' in py_ctt:
                err_py_keys.append(item)
                cont+=py_ctt
        return (err_py_keys,cont)
    def ret_py_keys(self,keys: list[str]):
        'return py keys'
        k=[]
        n=0
        for item in keys[:10]:
            n+=1
            if n%2==0:
                k.append(item)
        return k
    def tags(self)->str:
        capitals=[]
        pys=[]
        print(self.pys)
        for item in self.pys:
            if '㈠' in item:
                item=item[1:]
            if '㈡' in item:
                item=item[1:]
            pys.append(item)
        for i in pys:
            if i!='':
                cap=get_capital_alphabet(i)
                capitals.append(cap)
        # remove duplicate capital
        capitals_set=set(capitals)
        tags=' '.join(capitals_set)
        return tags

        


