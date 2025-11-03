
from typing import List,Dict
from sys import argv
from os import path,walk
import json

result_dict = {}


def write_json(file:str,out_dict:dict,*args,**kwargs):
    """Write a dictionary to a json file

    Parameters
    ----------
    file : str
        The output file.
    out_dict : dict
        The dictionary that will be written out.
    """    
    with open(file,"w") as fh:
        fh.write(json.dumps(out_dict,*args,**kwargs))

def get_files_recursive(directory:str,extension: str|None = None)->List[str]:
    """Get back all files recursively that have a certain extension

    Parameters
    ----------
    directory : str
        The directory path
    extension : _type_, optional
        The extension (tested with file.endswith()), by default None

    Returns
    -------
    List[str]
        The file names with path
    """    

    list = []
    for root, dirs, files in walk(directory):
        for file in files:
#            print(os.path.join(root, file))
            if extension:
                if file.endswith(extension):
                    list.append(path.join(root,file))
            else:
                list.append(path.join(root,file))
    return list

def read_fasta(file:str, min_length=0,to_upper=True, u_to_t=False) ->Dict[str,str]:
    """Read a fasta file into a mp

    Parameters
    ----------
    file : str
        The fasta file
    min_length : int, optional
        All sequences shorter than this threshold will be omitted, by default 0
    to_upper : bool, optional
        Convert sequences to upper case letters, by default True
    u_to_t : bool, optional
        Convert U to T (for RNA sequences), by default False
       Returns
    -------
    Dict[int,str]
        The reads map, read ID --> read sequence
    """
    back = {}
    sequence = ""
    id = ""
    with open(file,"r") as fh:
        for line in fh:
            if line.startswith(">"):
                ## an id was read before
                if len(id)> 0 and len(sequence) > min_length:
                    if to_upper:
                        sequence = sequence.upper()
                    if u_to_t:
                        sequence = sequence.replace("U","T")

                    back[id] = sequence
                    sequence = ""
                    id = line.strip().split()[0].replace(">","")
                else:
                    id = line.strip().split()[0].replace(">","")
            else:
                sequence = sequence + line.strip()

        if len(sequence) > 0:
            if to_upper:
                sequence = sequence.upper()
            if u_to_t:
                sequence = sequence.replace("U","T")
#                sequence = sequence.replace("U","T")
            back[id] = sequence
    return back

def add_to_dict(fasta_map: dict, sample: str):

    for k in fasta_map:
        v = fasta_map[k]
        rc = int(k.split("#")[1])
        if v in result_dict:
            result_dict[v][sample] = rc
        else:
            result_dict[v] = {sample:rc}


files = get_files_recursive(argv[1],"genomeMappedReads.fa")

for file in files:
#    print (file)
    f = file.split(path.sep)
#    print (f[len(f)-3])
    sample = f[len(f) -3]
    fm = read_fasta(file)
    print (f"LR\t{sample}\t{len(fm)}")
    add_to_dict(fm,sample)
    hr = file.replace("genomeMappedReads.fa","genomeMappedReadsHR.fa")
    fm = read_fasta(hr)
    add_to_dict(fm,sample)
    print (f"HR\t{sample}\t{len(fm)}")
#    print (hr)

#            cat_string = "cat {} {} > {}".format(os.path.join(output,"stat/genomeMappedReads.fa"),os.path.join(output,"stat/genomeMappedReadsHR.fa"),all_genome_mapped)

write_json(path.join(argv[1],"matrix.json"),result_dict)