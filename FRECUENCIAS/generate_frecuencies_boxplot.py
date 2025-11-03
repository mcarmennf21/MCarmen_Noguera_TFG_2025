
import pandas as pd
import plotly.express as px
import argparse

def give_args ():
    '''
    Ask for input and output files to generate graphics
    '''
    
    parser = argparse.ArgumentParser(description="Script that requires at least 3 parameters.")
    parser.add_argument("-input", required=True, help="Input file")
    parser.add_argument("-output", nargs="+", required=True, help="Output files")

    args = parser.parse_args()
    if len(args.output) < 2:
        parser.error("You need to provide at least 2 output files")

    return args.input, args.output[0], args.output[1]

if __name__ == '__main__':

    input, output_RC, output_UR = give_args()
    df_frecuency = pd.read_csv(input, sep="\t")

    fig_RC = px.box(df_frecuency, x="Length", y="PercentageRC", labels={"Length":"Length", "PercentageRC":"Frecuency Rc"}, points="all", hover_name="Samplename")
    fig_UR = px.box(df_frecuency, x="Length", y="PercentageUR", labels={"Length":"Length", "PercentageUR":"Frecuency UR"}, points="all", hover_name="Samplename")
    fig_UR.update_traces(marker=dict(color="firebrick"), line=dict(color="firebrick"))

    fig_RC.write_html(output_RC)
    fig_UR.write_html(output_UR)
