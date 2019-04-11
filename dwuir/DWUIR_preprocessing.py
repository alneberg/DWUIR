"""The preprocessing step of DWUIR: A script to transform fastq files with UMIs and indices in 
the header so that it can be demultiplexed by cutadapt.

Input can be in formats fastq and fastq.gz, output is printed 
uncompressed to stdout, intended to be piped to cutadapt.
"""
import argparse
import gzip
import sys
from itertools import islice
import re
import dnaio

def open_file(fp, mode):
    if fp.endswith('.gz'):
        return gzip.open(fp, mode)
    else:
        return open(fp, mode)

def main(args):
    # Regex matching the end of a fastq header:
    # [1,2] = Read 1 or 2
    # [N,Y] = Is Filtered Tag
    # [0-9]* = Control Number
    # ([A-Z]*) = Index1
    # ([A-Z]{N}) = UMI with exactly N bases
    # \+([A-Z]*) = Plus sign and Index2
    index_umi_re = re.compile(' ([1,2]:[N,Y]:[0-9]*):([A-Z]*)([A-Z]{{}})\+([A-Z]*)$'.format(args.UMI_length))
    sub_pattern = re.compile('\3 \1:\2+\4')

    step_len = 4
    if args.paired:
        step_len = 8
    with dnaio.open(args.input_fastq) as ifh:
        for record in ifh[:step_len]:
            _, index1, umi, index2 = re.search(index_umi_re, lines[0])
            header_line1 = re.sub(index_umi_re, sub_pattern, lines[0])
            sys.stdout.write(header_line1)
            sys.stdout.write(index1 + lines[1])
            sys.stdout.write(lines[2])
            sys.stdout.write(':'*len(index1) + lines[3])
            
            # Start printing R2:
            sys.stdout.write(header_line1.replace('{} 1:'.format(umi), '{} 2:'.format(umi)))

            if args.paired:
                sys.stdout.write(index2 + lines[5])
                sys.stdout.write(lines[6])
                sys.stdout.write(':'*len(index2) + lines[7])
            else:
                # Fake read 2
                sys.stdout.write(index2 + '\n')
                sys.stdout.write(lines[2])
                sys.stdout.write(':'*len(index2)+'\n')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_fastq", help=("Input fastq. If a paired-end sequencing setup "
                                            "has been used, the pairs should be interleaved "
                                            "in this input file and the appropriate --paired "
                                            "flag needs to be used."))
    parser.add_argument("--UMI_length", help=("Length of the UMI that will be removed from the "
                                              "end of the first index. Default value is 9"), 
                                              default=9)
    parser.add_argument("--paired", action="store_true", help=("Use this flag to indicate that "
                                            "the input fastq have interleaved pairs"))
    args = parser.parse_args()

    main(args)
