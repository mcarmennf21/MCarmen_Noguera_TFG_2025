
import argparse
import pandas as pd
import plotly.express as px

def give_args ():
    '''
    Ask for input and output files to generate graphics
    '''
    
    parser = argparse.ArgumentParser(description="Script that requires at least 5 parameters.")
    parser.add_argument("-input", required=True, help="Input file")
    parser.add_argument("-output", required=True, help="Output file")
    
    args = parser.parse_args()
    
    return args.input, args.output

if __name__ == '__main__':

    input, output = give_args()
   
    df_higher = pd.read_csv(input, sep="\t")
    fig_higher = px.box(df_higher, x="Length", y="Value", labels={"Length":"Length (nt)", "Value":"Reproducibility percentage among UR"}, log_y=True)
   
    fig_higher.write_html(output)

