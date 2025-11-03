
import os
import pandas as pd
import argparse

def get_file_source(root_dir):
    '''
    Look for files in dirs
    '''

    files = []
    for root, dirs, file in os.walk(root_dir):
        if os.path.basename(root) == "stat":
            archivo_r = os.path.join(root, "readLengthAnalysis.txt")
            if os.path.exists(archivo_r):
                files.append(archivo_r)

    return files


def main(list_of_files):
    '''
    Dictionary ---> {Length of read: [Sample, Percentage of RC, Percentage of UR]}
    '''
    
    dic ={}
    for file in list_of_files:
        sample_name = os.path.basename(os.path.dirname(os.path.dirname(file))) #Storing the sample name
        with open(file, "r") as fh:
            for line in fh:
                if not line[0].isdigit():
                    continue
                else:
                    f = line.strip().split("\t")
                    length = int(f[0])
                    if length >= 16 and length <= 26:
                        if length in dic:
                            dic[length].append([sample_name, f[4], f[2]])
                        else:
                            dic[length]=[[sample_name, f[4], f[2]]]
    dic = dict(sorted(dic.items()))
    
    return dic


def get_data_frame(dict_with_frecuencies):
    data_both_frecuency = []

    for key, list in dict_with_frecuencies.items():
        for sublist in list:
            data_both_frecuency.append([key, sublist[0], sublist[1], sublist[2]]) #Row for dataframe: [Length, Samplename, PercentageRC, PercentageUR]

    dfN_frecuency = pd.DataFrame(data_both_frecuency, columns=["Length", "Samplename", "PercentageRC", "PercentageUR"])

    return dfN_frecuency


def give_args():
    '''
    Ask for input and output files
    '''
    
    parser = argparse.ArgumentParser(description="Script that requires at least 2 parameters, an input file and an output file.")
    parser.add_argument("-rootdir", required=True, help="Input file")
    parser.add_argument("-output", required=True, help="Output file")
    
    args = parser.parse_args()

    return args.rootdir, args.output


if __name__ == '__main__':
    root_dir, output_dataframe_frecuency = give_args()
    list_of_files = get_file_source(root_dir)
    dict_with_frecuencies = main (list_of_files)
    df_frecuency = get_data_frame(dict_with_frecuencies)

    df_frecuency.to_csv(output_dataframe_frecuency, sep="\t", index=False)

