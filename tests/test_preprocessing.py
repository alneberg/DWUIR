def run_preprocessing():
    return "dummy"

def test_umi_placement():
    for line in run_preprocessing():
        print(line)
        assert line.split(':')[7].split(' ')[0] == 'CATGACGAC'
        # Test only header line, so break here
        break

def test_index_header_placement():
    for line in run_preprocessing():
        assert line.split(':')[-1] == "CACCCGTT+GCTATCCT"


if __name__ == '__main__':
    test_umi_placement()
    test_index_header_placement()
