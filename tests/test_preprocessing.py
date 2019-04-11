import subprocess
import os

def run_preprocessing_1read():
    testdir = os.path.dirname(os.path.realpath(__file__))
    input_file = os.path.join(testdir, 'test_data', '1_read.fastq.gz')
    script_path = os.path.join(testdir, '..', 'dwuir', 'DWUIR_preprocessing.py')
    return subprocess.Popen(['python', script_path, input_file], stdout=subprocess.PIPE).stdout

def run_preprocessing_250_reads():
    testdir = os.path.dirname(os.path.realpath(__file__))
    input_file = os.path.join(testdir, 'test_data', '250_reads.fastq.gz')
    script_path = os.path.join(testdir, '..', 'dwuir', 'DWUIR_preprocessing.py')
    return subprocess.Popen(['python', script_path, input_file], stdout=subprocess.PIPE).stdout

def run_preprocessing_1read_paired():
    testdir = os.path.dirname(os.path.realpath(__file__))
    input_file = os.path.join(testdir, 'test_data', '1_read.interleaved.fastq.gz')
    script_path = os.path.join(testdir, '..', 'dwuir', 'DWUIR_preprocessing.py')
    return subprocess.Popen(['python',  script_path, '--paired', input_file], stdout=subprocess.PIPE).stdout
    

def test_umi_placement():
    """Correct UMI in R1"""
    for line in run_preprocessing_1read():
        assert line.split(b':')[7].split(b' ')[0] == b'CATGACGAC'
        # Test only header line, so break here
        break

def test_index_header_placement():
    """Correct index in header of R1"""
    for line in run_preprocessing_1read():
        assert line.split(b':')[-1] == b"CACCCGTT+GCTATCCT\n"
        break

def test_read_sequence_R1():
    """First index placed in R1"""
    first = True
    second = False
    for line in run_preprocessing_1read():
        if first:
            first = False
        else: # Only test the second line
            assert line.startswith(b'CACCCGTT')
            second = True
            break
    assert second # Make sure the else case is executed

    with gzip.open('1_read.fastq.gz', 'rb') as ifh:
        original = ifh.readlines()
    assert output[1] == 'CACCCGTT' + original[1]

def test_interleaved():
    """Exactly 2 interleaved reads"""
    output = run_preprocessing_1read().readlines()
    assert len(output) == 8

def test_r1r2_header():
    """Identical header except R1/R2 denotion"""
    output = run_preprocessing_1read().readlines()
    assert output[4].replace(b' 2:N', b' 1:N') == output[0]

def test_r2_index():
    """Test insertion of index in R2"""
    output = run_preprocessing_1read().readlines()
    assert output[5].startswith(b'GCTATCCT')

def test_nr_reads():
    """Test nr of reads have doubled"""
    output = run_preprocessing_250_reads()
    assert len(output.readlines()) == 2000

def test_paired_umi_placement():
    """Check UMI placement for both reads"""
    output = run_preprocessing_1read_paired().readlines()
    for line in output[0,4]:
        assert line.split(b':')[7].split(b' ')[0] == b'CATGACGAC'

def test_paired_index_header_placement():
    """Check index placement for both reads"""
    output = run_preprocessing_1read_paired().readlines()
    for line in output[0,4]:
        assert line.split(b':')[-1] == b"CACCCGTT+GCTATCCT\n"

def test_paired_read_sequences():
    """Check read sequence for both reads"""
    output = run_preprocessing_1read_paired().readlines()
    assert output[1].startswith(b'CACCCGTT')
    assert output[5].startswith(b'GCTATCCT')

def test_paired_read_sequences():
    """Check read sequence for both reads"""
    output = run_preprocessing_1read_paired().readlines()
    assert output[1].startswith(b'CACCCGTT')
    assert output[5].startswith(b'GCTATCCT')

    with gzip.open('1_read.interleaved.fastq.gz', 'rb') as ifh:
        original = ifh.readlines()
    assert output[1] == 'CACCCGTT' + original[1]
    assert output[5] == 'GCTATCCT' + original[5]

def test_length_read_index_paired():
    """Length of read and qualities should match"""
    output = run_preprocessing_1read_paired().readlines()
    assert len(output[1]) == len(output[3])
    assert len(output[5]) == len(output[7])

def test_paired_r1r2_header():
    """Identical header except R1/R2 denotion for paired"""
    output = run_preprocessing_1read_paired().readlines()
    assert output[4].replace(b' 2:N', b' 1:N') == output[0]

if __name__ == '__main__':
    pass
