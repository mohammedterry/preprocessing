import os

class Tokeniser:
    filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'    
 
    def __init__(self, path = 'small_vocab', hash_function = False):  
        self.load(path = path)     
        self.tokenise(hash_function = hash_function)

    def load(self, path):
        input_file = os.path.join(path)
        with open(input_file, "r") as f:
            data = f.read()
        self.sentences = data.split('\n')
        self.max_length = max([len(sentence.strip(self.filters).split()) for sentence in self.sentences])
        self.words = [word for sentence in self.sentences for word in sentence.split() if word not in self.filters]
        self.vocab = [word.lower().strip(self.filters) for word in set(self.words)]

    def tokenise(self, hash_function):
        if hash_function:
            self.ids = {(hash(w) % (len(self.vocab) - 1) + 1) : w for w in self.vocab}
        else:
            self.ids = {i:w for i,w in zip(range(1,len(self.vocab) + 1), self.vocab)}

    def display(self, n = 1):
        for i in range(n):
            print('Line {}:  {}'.format(i + 1, self.sentences[i]))
        print('{} words.'.format(len(self.words)))
        print('{} unique words.'.format(len(self.vocab)))
        print('{} words is the length of the longest sentence.'.format(self.max_length))


T = Tokeniser().display()