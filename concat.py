import splitter #to format the content

def concat(input_paths, output_path = 'concat.txt'):
    '''
    concatonates several files into one efficiently
    '''
    with open(output_path, "w") as output_file: 
        for path in input_paths:
            with open(path) as input_file:
                output_file.write(splitter.split_sentences(input_file.read()))
                output_file.write('\n++++++++++\n')
    print('done')

#TESTING
filenames = '''
    2_3.txt 2_7.txt
    '''.split()
concat(filenames, '00000.txt')
