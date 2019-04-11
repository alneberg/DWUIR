# DWUIR - Demultiplexing With UMIs in the Index Read
Currently `bcl2fastq2` does not support UMI sequences which are located in the index read.
It is however possible to get the UMI sequences into the read name of the fastq with the caveat that the demultiplexing
then is broken.
This repo contains some scripts to transform the input and perform the demultiplexing using cutadapt.

## Supported Use cases
### Unique dual indices, single end sequencing, UMI in the end of the first adapter
### Unique dual indices, paired end sequencing, UMI in the end of the first adapter

## Use cases not supported
### Dual non-unique indices
This requires running cutadapt twice, demultiplexing based on one index at a time.

### UMI in template read
This is supported by `bcl2fastq2` and therefore, this hack is not necessary.

## Input
Fastq file(s) with the indices and UMIs located in the read name, like so:
```
@D00450:681:HTMCVBCX2:1:1108:1183:1896 1:N:0:CACCCGTTCATGACGAC+GCTATCCT
NCCGTGTTATCCTTGAGTAAAGGTGAGTATTAGGTGTGAGAGCGTTTTGAA
+
#<<GGGGGG.<<<AGG.GG.<AA<G.<GGG.<AGGG.<GGGGG.<GAG.G<
@D00450:681:HTMCVBCX2:1:1108:1180:1951 1:N:0:CTTACTCGATCTCGAAT+CCTATCCT
GGCCAAGCGTTCATAGCGACGTCGCTTTTTTATCCTTCGATGTCGGCTCTT
+
AGGAA.<AGGGA.<GGAAGIAGGGAA.GG..<.<.<GAGGG.G..AGGIGA
@D00450:681:HTMCVBCX2:1:1108:1499:1856 1:N:0:CCTTGATCGAATCCTAA+ACTCCATC
NGTAGATCTGTGGCGATATGAGAGGGCTGCAGTGCCTTTCCCCATTCATTC
+
#<<AGAAGIGIAGGAGGGII..GGGG<<G.<G<<.GAGGG..<A<AGAGGG
```

## Output
Demultiplexed fastq files with the UMIs seperated from the indices:
```
@D00450:681:HTMCVBCX2:1:1108:1183:1896:CATGACGAC 1:N:0:CACCCGTT+GCTATCCT
NCCGTGTTATCCTTGAGTAAAGGTGAGTATTAGGTGTGAGAGCGTTTTGAA
+
#<<AGAAGIGIAGGAGGGII..GGGG<<G.<G<<.GAGGG..<A<AGAGGG
```
