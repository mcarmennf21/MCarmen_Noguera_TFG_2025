import sys
import gzip

def read_sRNAbench_fasta(file):
    """ 
    Read a fasta file
    Return: dictionary ID <---> Sequence
    """
    back = {}

    if file.endswith('.gz'):
        import gzip
        my_open = gzip.open
    else:
        my_open = open

    with my_open(file, 'rt') as fh:

        for line in fh:
            if line.startswith(">"):
                seq = fh.readline().strip()
                f = line.split("#")
                back[seq] = int(f[1].strip())
                
    return back

def main(args):
    """
    Arguments: the microRNA file, the prediction
    """
    ### read the fasta files
    counts_1 = read_sRNAbench_fasta(args[0])
    counts_2 = read_sRNAbench_fasta(args[1])
    
    max_len = 0
    intersect = {}
    ## iterate first dictionary
    for read in counts_1:
        #check if read exists in other 
        ## intersection - read is in both
        if read in counts_2:    
            intersect[read]=[counts_1[read],counts_2[read]]
        ## read is only in first file --> assign 0 to second
        else:
            intersect[read]=[counts_1[read],0]
    
        if len(read) > max_len:
            max_len = len(read)
    ## interate the second dictionary
    for read in counts_2:
        ## read is only in second --> assign 0 to first
        if not read in intersect:
            intersect[read] = [0,counts_2[read]]
        
        if len(read) > max_len:
            max_len = len(read)

    
    ### the length dictionary
    length_dic = {}
    
    ## generate the data structure for the intersection/unique counts as a function of read length
    for i in range(max_len+1):
        length_dic[i] = [0,0,0,0,0,0,0,0]
        # description of indexes of the length_dic
        # 0: amount of intersecting reads in first file, 1: amount of intersecting reads in second file; 
        # 2: amount of unique reads in first file; 3: amount of unique reads in second file
        # index 4-7 are the same but counting UNIQUE reads instead of READ COUNT
    for read in intersect:
#        print("read: {} {}-{}".format(read,intersect[read][0],intersect[read][1]))
        length = len(read)
        ## check if read exists in both samples
        if intersect[read][0] > 0 and intersect[read][1] > 0:
            length_dic[length][0] = length_dic[length][0] + intersect[read][0]
            length_dic[length][1] = length_dic[length][1] + intersect[read][1]
            length_dic[length][4] = length_dic[length][4] + 1
            length_dic[length][5] = length_dic[length][5] + 1
        elif intersect[read][0] > 0 :
            length_dic[length][2] = length_dic[length][2] + intersect[read][0]
            length_dic[length][6] = length_dic[length][6] + 1
        elif intersect[read][1] > 0 :
            length_dic[length][3] = length_dic[length][3] + intersect[read][1]
            length_dic[length][7] = length_dic[length][7] + 1
        else:
            print("ERROR - The program should never go here!!!!!")
    return length_dic
#    for i in length_dic:
#        print(" len {} {}".format(i,length_dic[i]))


def write_length_dict(length_dict, outfile,annotation, write_type="w"):
    with open (outfile,write_type) as out:
        out.write("#{}\n".format(annotation))
        for length in length_dict:
            out.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(length,length_dict[length][0],length_dict[length][1],length_dict[length][2],length_dict[length][3],length_dict[length][4],length_dict[length][5],length_dict[length][6],length_dict[length][7])) 
              
if __name__ == '__main__':

    ## call main function with list of provided command lines (all less the first one which is the name of the python program itself)
    arg = [r"F:\docencia\TFG_2425\SRP263048\SRX8384368.fa.gz",r"F:\docencia\TFG_2425\SRP263048\SRX8384367.fa.gz"]
    length_dict = main(arg)
    write_length_dict(length_dict,r"F:\docencia\TFG_2425\out.tsv","file1-file2")
#    main(sys.argv[1:])