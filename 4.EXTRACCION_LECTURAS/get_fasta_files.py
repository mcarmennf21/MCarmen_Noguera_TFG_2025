
import argparse

def get_reads_frecuency(input, min_len, max_len, min_percentage, max_percentage):
    '''
    Read the file and extract reads within specific ranges of length and reproducibility
    '''
    
    with open(input, "r") as fh:
        rna_parametric = []
        
        for line in fh:
            if line.startswith("#"):
                total = line.replace(" ", "").split(":")
                denominator = int(total[1])
            else:
                f = line.strip().split("\t")
                if int(len(f[0])) >= min_len and int(len(f[0])) <= max_len:
                    if float((int(f[1])/denominator)*100) >= min_percentage and float((int(f[1])/denominator)*100) <= max_percentage:
                        rna_parametric.append([f[1], f[0]]) 

    return rna_parametric


def give_args ():
    '''
    Ask for input and output files, and for the parameters of length and reproducibility
    '''
    
    parser = argparse.ArgumentParser(description="Script that requires at least 5 parameters.")
    parser.add_argument("-input", required=True, help="Input file")
    parser.add_argument("-output", required=True, help="Output file")
    parser.add_argument("-minlen", type=float, required=True, help="Minimum length")
    parser.add_argument("-maxlen", type=float, required=True, help="Maximum length")
    parser.add_argument("-minpercentage", type=float, required=True, help="Minimum percentage")
    parser.add_argument("-maxpercentage", type=float, required=True, help="Maximum percentage")
    
    args = parser.parse_args()
    #if len(args.params) < 4:
        #parser.error("You need to provide at least 4 positional parameters!!")

    return args.input, args.output, args.minlen, args.maxlen, args.minpercentage, args.maxpercentage 

def write_fasta_file(list_with_reproducibilities, output, write_type="w"):
    '''
    Write fasta file with this specific format: 
        >ID(number)#(number of samples)
        (SEQUENCE)
    '''
    
    with open (output, write_type) as out:
        for count, sequence in enumerate(list_with_reproducibilities, start=1):
            out.write(f">ID{count}#{sequence[0]}\n")
            out.write(f"{sequence[1]}\n")


if __name__ == '__main__':
    
    input, output, min_len, max_len, min_percentage, max_percentage = give_args()
    list_with_reproducibilities = get_reads_frecuency(input, min_len, max_len, min_percentage, max_percentage)
    #outfile_name = r"reads_frecuency_{}-{}, {}-{}.fasta".format(min_len, max_len, min_percentage, max_percentage)
    #out_path = r"C:\Users\nogfe\Desktop\TFG\e xperiments_and_results\reads_getted\{}".format(outfile_name)
    write_fasta_file(list_with_reproducibilities, output)
