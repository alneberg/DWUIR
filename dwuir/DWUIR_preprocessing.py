"""The preprocessing step of DWUIR: A script to transform fastq files with UMIs and indices in 
the header so that it can be demultiplexed by cutadapt.

Input can be in formats fastq and fastq.gz, output is printed 
uncompressed to stdout, intended to be piped to cutadapt.
"""
import argparse
import gzip
import sys

def open_file(fp, mode):
    if fp.endswith('.gz'):
        return gzip.open(fp, mode)
    else:
        return open(fp, mode)

def main(args):
    with open_file(args.input_fastq, 'rt') as ifh:
        for line in ifh:
            sys.stdout.write(line)
         

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
