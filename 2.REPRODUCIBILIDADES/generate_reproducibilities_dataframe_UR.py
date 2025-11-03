
import argparse
import numpy as np
import pandas as pd

def main (input):
    '''
    Read tsv file with number of samples in which reads are present
    Return dictionary: Read lenght <---> List with reproducibility percentages
    '''
    with open(input, "r") as fh:
        dic = {}
        for line in fh:
            if line.startswith("#"):
                total = line.replace(" ", "").split(":")
                denominator = int(total[1])
            else:
                f = line.strip().split("\t")
                length = len(f[0])
                if length >= 16 and length <= 26:
                    if length in dic:
                        dic[length].append(float((int(f[1])/denominator)*100))
                    else:
                        dic[length]=[float((int(f[1])/denominator)*100)]
    dic = dict(sorted(dic.items()))
    
    return dic


def get_data_frame(dict_reproducibility):
    '''
    Dataframe with reproducibility percentiles (1-100) for each list
    '''
    
    data_higher = []
    
    for key, list in dict_reproducibility.items():    
        for q in range(0, 101):
            percentiles_higher = np.percentile(list, q, method = 'higher')
            data_higher.append([key, q, float(percentiles_higher)]) #Row for dataframe: [key, P{q}, value]
  
    dfN_higher = pd.DataFrame(data_higher, columns = ["Length", "Percentile", "Value"])
    
    return dfN_higher



def give_args ():
    '''
    Ask for input and output files
    '''
    
    parser = argparse.ArgumentParser(description="Script that requires at least 5 parameters.")
    parser.add_argument("-input", required=True, help="Input file")
    parser.add_argument("-output", required=True, help="Output file")
    
    args = parser.parse_args()

    return args.input, args.output

if __name__ == '__main__':
    input, output_higher = give_args()
    dict_reproducibility = main(input)
    
    dfN_higher = get_data_frame(dict_reproducibility)

    dfN_higher.to_csv(output_higher, sep="\t", index=False)

