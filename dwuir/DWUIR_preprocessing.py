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
    # I didn't get string formatting to work, so I made a quick + + instead.
    index_umi_re = re.compile(' ([1,2]:[N,Y]:[0-9]*):([A-Z]*)([A-Z]{' + str(args.UMI_length) + '})\+([A-Z]*)$')
    sub_pattern = re.compile('\3 \1:\2+\4')

    step_len = 4
    if args.paired:
        step_len = 8

    with dnaio.open(args.input_fastq, interleaved=args.paired) as ifh, \
         dnaio.open(sys.stdout.buffer, fileformat='fastq', mode='w') as ofh:
        for record in ifh:
            if args.paired:
                r1, r2 = record
            else:
                r1 = record

            _, index1, umi, index2 = re.search(index_umi_re, r1.name).groups()
            r1.name = re.sub(index_umi_re, r':\3 \1:\2+\4', r1.name)
            r1.sequence = index1 + r1.sequence
            r1.qualities = ':'*len(index1) + r1.qualities
            ofh.write(r1)

            # Start printing R2:
            r2_name = r1.name.replace('{} 1:'.format(umi), '{} 2:'.format(umi))

            if args.paired:
                r2.name = r2_name
                r2.sequence = index2 + r2.sequence
                r2.qualities = ':'*len(index2) + r2.qualities
                ofh.write(r2)
            else:
                # r1 is fake read 2
                r1.name = r2_name
                r1.sequence = index2
                r1.qualities = ':'*len(index2)
                ofh.write(r1)



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
