import subprocess
import os

def run_preprocessing():
    testdir = os.path.dirname(os.path.realpath(__file__))
    input_file = os.path.join(testdir, 'test_data', '1_read.fastq.gz')
    script_path = os.path.join(testdir, '..', 'dwuir', 'DWUIR_preprocessing.py')
    return subprocess.Popen(['python', script_path, input_file], stdout=subprocess.PIPE).stdout

def test_umi_placement():
    for line in run_preprocessing():
        assert line.split(b':')[7].split(b' ')[0] == b'CATGACGAC'
        # Test only header line, so break here
        break

def test_index_header_placement():
    for line in run_preprocessing():
        assert line.split(b':')[-1] == b"CACCCGTT+GCTATCCT"

def test_read_sequence_R1():
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

if __name__ == '__main__':
    pass
