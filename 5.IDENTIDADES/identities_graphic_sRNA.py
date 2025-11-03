
import os
import pandas as pd
import plotly.express as px
import argparse

def get_file_source(root_dir):
    '''
    Look for files in dirs
    '''
    
    files = []

    for root, dirs, file in os.walk(root_dir):
        dirs.sort()
        if os.path.basename(root) == "stat":
            archivo_r = os.path.join(root, "mapping_stat_all.tsv")
            if os.path.exists(archivo_r):
                files.append(archivo_r)

    return files

def give_args():
    '''
    Ask for input and output files to generate dataframe and graphic
    '''
    
    parser = argparse.ArgumentParser(description="Script that requires at least 2 parameters, an input file and an output file.")
    parser.add_argument("-rootdir", required=True, help="Input file")
    parser.add_argument("-output_df", required=True, help="Output dataframe file")
    parser.add_argument("-output_graphic", required=True, help="Output graphic")

    args = parser.parse_args()

    return args.rootdir, args.output_df, args.output_graphic

def main(list_of_files):
    '''
    Read each file
    Return dictionary ---> {Category: [Percentages of UR in each file; if that category does not exist, add 0]}
    '''
    
    dic = {}
    
    for file in list_of_files:
        with open(file, "r") as fh:
            next(fh)
            for line in fh:
                    f = line.strip().split("\t")
                    if f[0] not in dic:
                            dic[f[0]] = []

    for file in list_of_files:
        lines = []
        with open(file, "r") as fh:
            next(fh)
            for line in fh:
                f = line.strip().split("\t")
                lines.append(f)
        
        for key in dic:
            present = False
            for i in lines:    
                if i[0] == key:
                    dic[key].append(float(i[2]))
                    present=True    
            if not present:
                dic[key].append(0)
    
    if all(len(v) == 6 for v in dic.values()):
        print("----")
        print("All categories have exactly 6 elements")
    else:
        print("----")
        print("ERROR: There are any list(s) without 6 elements")

    return dic

def classify_categories(identities_dict):

    #Classifying some important categories for our study and adding to a new dict with the sum of its values
    keys_repetitiveDNA = {"LINE_+", "LINE_-", "SINE_+", "SINE_-", "Satellite_+", "Satellite_-", "LTR_+", "LTR_-", "Retroposon_+", "Retroposon_-"}
    sum_repetitiveDNA = [sum(values) for values in zip(*(identities_dict[k] for k in keys_repetitiveDNA))]

    keys_rRNA = {"rRNA_+", "rRNA_-"}
    sum_rRNA = [sum(values) for values in zip(*(identities_dict[k] for k in keys_rRNA))]

    keys_mRNA = {"mRNA_+", "mRNA_-"}
    sum_mRNA = [sum(values) for values in zip(*(identities_dict[k] for k in keys_mRNA))]

    keys_TSS = {"TSS_+", "TSS_-"}
    sum_TSS = [sum(values) for values in zip(*(identities_dict[k] for k in keys_TSS))]

    keys_TES = {"TES_+", "TES_-"}
    sum_TES = [sum(values) for values in zip(*(identities_dict[k] for k in keys_TES))]

    keys_pseudogene = {"pseudogene_-", "pseudogene_+"}
    sum_pseudogene = [sum(values) for values in zip(*(identities_dict[k] for k in keys_pseudogene))]

    new_identities_dict = {k: v for k, v in identities_dict.items() if (k not in keys_repetitiveDNA and k not in keys_rRNA and k not in keys_mRNA and k not in keys_TSS and k not in keys_TES and k not in keys_pseudogene)}
    new_identities_dict["Repetitive_DNA"] = sum_repetitiveDNA
    new_identities_dict["rRNA"] = sum_rRNA
    new_identities_dict["mRNA"] = sum_mRNA
    new_identities_dict["TSS"] = sum_TSS
    new_identities_dict["TES"] = sum_TES
    new_identities_dict["Pseudogene"] = sum_pseudogene

    #Grouping the less abundant categories into one
    keys_other_RNA = set()
    for key, values in new_identities_dict.items():
        if key == "ath-miRBase_+":
            continue
        count = sum(x > 1.5 for x in values)
        if count < 3:
            keys_other_RNA.add(key)
    
    sum_other_RNA = [sum(values) for values in zip(*(new_identities_dict[k] for k in keys_other_RNA))]
    definitive_dict = {k: v for k, v in new_identities_dict.items() if k not in keys_other_RNA}
    definitive_dict["Other_RNA"] = sum_other_RNA
    
    print(definitive_dict)
    return definitive_dict

def get_plot_bar(definitive_dict):
    
    #DATAFRAME
    variables = [["21nt", "High"], ["21nt", "Low"], ["21nt", "Medium"], ["24nt", "High"], ["24nt", "Low"], ["24nt", "Medium"]]
    data = []
    
    for key, values in definitive_dict.items():
        for [length, reproducibility], value in zip(variables, values):
            data.append([key, length, reproducibility, value]) #Row for dataframe: [Categories, Length, Reproducibility, Percentage UR]

    df = pd.DataFrame(data, columns=["Category", "Length", "Reproducibility", "Percentage_UR"])

    #Grouping categories Length and Reproducibility / Ordering them
    df["Length_Reproducibility"] = df["Length"] + "-" + df["Reproducibility"]
    order = ["21nt-High", "24nt-High", "21nt-Medium", "24nt-Medium", "21nt-Low", "24nt-Low"]
    df["Length_Reproducibility"] = pd.Categorical(df["Length_Reproducibility"], categories=order, ordered=True)


    #PLOT BAR
    colors = {"ath-miRBase_+": "saddlebrown", "rRNA": "brown", "mRNA": "tomato", "TSS": "khaki", "TES": "deepskyblue", "Pseudogene": "springgreen", "Repetitive_DNA": "blueviolet", "Other_RNA": "hotpink", "unassigned": "grey"}

    plot_identities = px.bar(df, x="Length_Reproducibility", y="Percentage_UR", color="Category", color_discrete_map=colors, category_orders={"Length_Reproducibility": order}, barmode="stack")
    plot_identities.update_layout(xaxis_title="sRNA type (with Length and Reproducibility)", yaxis_title="Percentage UR", legend_title="Categories", template="plotly_white")
  
    return df, plot_identities

if __name__ == '__main__':
    root_dir, output_df, output_graphic= give_args()
    list_of_files = get_file_source(root_dir)
    identities_dict = main (list_of_files)
    definitive_dict = classify_categories(identities_dict)
    df_identities, identities_graphic = get_plot_bar(definitive_dict)

    df_identities.to_csv(output_df, sep="\t", index=False)
    identities_graphic.write_html(output_graphic)

