
import sys
import subprocess
import os
import get_intersection as inter


def main(config_list,input_path,output):
    
    write_type="w"
    for i in range(0,len(config_list)-1):
        for j in range(i+1,len(config_list)):
            
            f1 = config_list[i].split("\t")
            f2 = config_list[j].split("\t")
            path1 = os.path.join(input_path,f1[1]+"/"+f1[0]+"/"+f1[0]+".fa")
            path2 = os.path.join(input_path,f2[1]+"/"+f2[0]+"/"+f2[0]+".fa")
            print("------")
            print(path1)
            print(path2)
            print("###")
            length_dict = inter.main([path1,path2])
            inter.write_length_dict(length_dict,output,"{} {}:{} {}".format(f1[0],f1[2],f2[0],f2[2]),write_type=write_type)
            write_type="a"


def map_to_genome(config_list,outbase):
    
    # the genome mapped reads to return
    back = []
    for line in config_list:
        
        f = line.split("\t")
        input = "/shared/bak/raw_data/miSRAdb/miRexpress_store/{}/reads/{}.fa.gz".format(f[1],f[0])
        output = os.path.join(outbase,f[1]+"/"+f[0])
        assembly = f[5]
        parameters = "alignType=v mm=0 bedGraph=true"
        str = "java -jar /shared/bak/sRNAtoolboxDB/exec/sRNAbench.jar input={} output={} species={} {}".format(input,output,assembly,parameters)
        all_genome_mapped = os.path.join(output,f[0]+".fa")
        print ("looking for "+all_genome_mapped)
        if not os.path.exists(all_genome_mapped):
            print (str)
            subprocess.run(str, shell=True, check=True)
            
            cat_string = "cat {} {} > {}".format(os.path.join(output,"stat/genomeMappedReads.fa"),os.path.join(output,"stat/genomeMappedReadsHR.fa"),all_genome_mapped)
            subprocess.run(cat_string,shell=True,check=True)
            back.append(all_genome_mapped)
        
        else:
            print(all_genome_mapped+" exists")
            back.append(all_genome_mapped)
    return back

if __name__ == '__main__':


    config_file = sys.argv[1]
    outbase = sys.argv[2]
    outfile = sys.argv[3]
    with open(config_file,"r") as fh:
        config_list = fh.readlines()
    
        
    map_to_genome(config_list,outbase)        
    main(config_list,outbase,outfile)
