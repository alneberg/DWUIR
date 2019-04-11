import subprocess
import os

def run_preprocessing():
    testdir = os.path.dirname(os.path.realpath(__file__))
    input_file = os.path.join(testdir, 'test_data', '1_read.fastq.gz')
    script_path = os.path.join(testdir, '..', 'dwuir', 'DWUIR_preprocessing.py')
    return subprocess.Popen(['python', script_path, input_file], stdout=subprocess.PIPE).stdout

def test_umi_placement():
    """Correct UMI in R1"""
    for line in run_preprocessing():
        assert line.split(b':')[7].split(b' ')[0] == b'CATGACGAC'
        # Test only header line, so break here
        break

def test_index_header_placement():
    """Correct index in header of R1"""
    for line in run_preprocessing():
        assert line.split(b':')[-1] == b"CACCCGTT+GCTATCCT"

def test_read_sequence_R1():
    """First index placed in R1"""
    first = True
    second = False
    for line in run_preprocessing():
        if first:
            first = False
        else: # Only test the second line
            assert line.startswith(b'CACCGTT')
            second = True
            break
    assert second # Make sure the else case is executed

def test_interleaved():
    """Exactly 2 interleaved reads"""
    output = run_preprocessing().readlines()
    assert len(output) == 8

def test_r1r2_header():
    """Identical header except R1/R2 denotion"""
    output = run_preprocessing().readlines()
    assert output[4].replace(b' 2:N', b' 1:N') == output[0]

def test_r2_index():
    """Test insertion of index in R2"""
    output = run_preprocessing().readlines()
    assert output[5].startswith('GCTATCCT')

if __name__ == '__main__':
    pass
