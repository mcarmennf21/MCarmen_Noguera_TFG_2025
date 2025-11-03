
from sys import argv
from os import path
import json

def read_json(file:str,*args,**kwargs):
    """Read a json file and give back a dictionary

    Parameters
    ----------
    file : str
        The input file in json format

    Returns
    -------
    dict
        The corresponding dictionary
    """
    if not path.exists(file):
        return {}
    
    with open(file, 'r',encoding="utf-8") as fh:
        return json.load(fh,*args,**kwargs)
    

def sort_list (a):
    return a[1]

d = read_json(argv[1])
c = set()
count_d = {}
for read in d: # outer key

    c= c.union(d[read].keys())

    count_d[read] = len(d[read])

tosort = []
for k in count_d:
    tosort.append([k,count_d[k]])

tosort.sort(key=sort_list,reverse=True)

with open (f"{argv[1]}_mat.tsv","w") as fh:
    fh.write(f"#total: {len(c)}\n")
    for  sorted in tosort:
        fh.write(f"{sorted[0]}\t{sorted[1]}\n")

