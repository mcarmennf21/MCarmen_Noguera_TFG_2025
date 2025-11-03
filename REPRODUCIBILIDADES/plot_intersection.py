import pandas as pd
import plotly.express as px
import plotly.io as io
import plotly.graph_objects as go

def get_data_frame_read_count(input, min_len = 16, max_len=26): 
    '''
    Dataframe of RC intersections (calculated using Jaccard index)
    '''

    data=[]
    name1 ="NA"
    name2="NA"
    cond = "Intra"
    color = "blue"
    with open(input,"r") as fh:
        for line in fh:
            if line.startswith("#"):
                names=line.replace("#","").strip().split(":")
                name1 = names[0]+names[1].split(" ")[0]
                name2 = names[1]+names[0].split(" ")[0]
                if names[0].split()[1] == names[1].split()[1]:
                    cond="Intra"
                    color="blue"
                else:
                    cond="Inter"
                    color="red"
            else:
                f = line.split("\t")
                if int(f[0]) >= min_len and int(f[0]) <= max_len:
                    if float(f[1]) + float(f[3]) > 0 and float(f[2]) + float(f[4]) > 0:
                        fraction1 = float(f[1])/(float(f[1])+float(f[3]))
                        fraction2 = float(f[2])/(float(f[2])+float(f[4]))
                        data.append([f[0],fraction1,name1,cond,color])
                        data.append([f[0],fraction2,name2,cond,color])
                    
    dfN = pd.DataFrame(data, columns=['Length', "Fraction","Comparison","Condition","Color"])    
    return dfN
def get_data_frame_unique_reads(input, min_len = 16, max_len=26): 
    '''
    Dataframe of UR intersections (calculated using Jaccard index)
    '''

    data=[]
    name1 ="NA"
    name2="NA"

    cond = "Intra"
    color="blue"
    with open(input,"r") as fh:
        for line in fh:
            if line.startswith("#"):
                names=line.replace("#","").strip().split(":")
                name1 = names[0]+names[1].split()[0]
                name2 = names[1]+names[0].split()[0]
                if names[0].split()[1] == names[1].split()[1]:
                    cond="Intra"
                    color="blue"
                else:
                    cond="Inter"
                    color="red"
                
            else:
                f = line.split("\t")
                if int(f[0]) >= min_len and int(f[0]) <= max_len:
                    if float(f[1]) + float(f[3]) > 0 and float(f[2]) + float(f[4]) > 0:
                        fraction1 = float(f[5])/(float(f[5])+float(f[7]))
                        fraction2 = float(f[6])/(float(f[6])+float(f[8]))
                        data.append([f[0],fraction1,name1,cond,color])
                        data.append([f[0],fraction2,name2,cond,color])
                    
    dfN = pd.DataFrame(data, columns=['Length', "Fraction","Comparison","Condition","Color"])    
    return dfN

if __name__ == '__main__':


    input = r"C:\Users\nogfe\Desktop\TFG\experiments_and_results\tsv_files\different_tissues\seeds_flowers_SRP098796_SRP194124.tsv"
    output = input.replace(".tsv", ".html")
    
    df = get_data_frame_read_count(input)
    df_u = get_data_frame_unique_reads(input)
    labels={"Fraction":"Read Count Intersection","Length":"Length (nt)"}
    
    fig = px.box(df, y="Fraction",x="Length",labels=labels,points="all",color="Condition",hover_name="Comparison")
    fig_u = px.box(df_u, y="Fraction",x="Length",labels=labels,points="all",hover_name="Comparison")
    
    fig_alt = go.Figure()
    fig_alt.add_trace(go.Scatter(x=df["Length"],y=df["Fraction"],mode="markers",text=df['Comparison'],marker=dict(color=df['Color'])))
    fig_alt.update_layout(xaxis_title="Length (nt)", yaxis_title="Reproducibility (Read Count Intersection)")

    if output.endswith("html"):
        fig.write_html(output)
        fig_alt.write_html(output.replace("html","_scatter.html"))
        fig_u.write_html(output.replace("html","_unique.html"))
    else:
        io.write_image(fig,output)
