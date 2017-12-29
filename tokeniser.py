import os
import collections

class Tokeniser:
    filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'    
 
    def __init__(self, path = 'small_vocab', ordered = True, hashing = False, padding = True):  
        self.load(path = path, ordered = ordered)     
        self.tokenise(hashing = hashing)
        self.sequences = [self.sequence(sentence, padding = padding) for sentence in self.sentences]

    def load(self, path, ordered):
        input_file = os.path.join(path)
        with open(input_file, "r") as f:
            data = f.read()
        self.sentences = [sentence.strip(self.filters) for sentence in data.split('\n')]
        self.max_length = max([len(sentence.split()) for sentence in self.sentences])
        words = [word.lower().strip(self.filters) for sentence in self.sentences for word in sentence.split() if word not in self.filters]
        self.word_count = len(words)
        word_freq = collections.Counter(words)
        if ordered:
            self.vocab = [word for word, _ in word_freq.most_common()]            
        else:
            self.vocab = [word for word in set(words)]

    def tokenise(self, hashing):
        if hashing: #some vocab gets lost due to hashing problem
            self.id2word = {(hash(w) % (len(self.vocab) - 1) + 1) : w for w in self.vocab}
        else: #number off according to frequency - e.g. 1 is most frequent word in vocab
            self.id2word = {i:w for i,w in zip(range(1,len(self.vocab) + 1), self.vocab)}
        self.word2id = {d[1]: d[0] for d in self.id2word.items()}

    def sequence(self, sentence, padding = True):
        pad = [] 
        if padding: pad = [0]*(self.max_length - len(sentence.split())) 
        return pad + [self.word2id[word.lower().strip(self.filters)] for word in sentence.split() if word not in self.filters]

    def display(self, s = 3, w = 10): 
        #s & w are number of sentences & words to display (-1 displays all)
        if s == -1: s = len(self.sentences)
        if w == -1: w = len(self.vocab)
        print('{} unique words.'.format(len(self.vocab)))
        print('{} words in total.'.format(self.word_count))
        print('{} words is the length of the longest sentence.'.format(self.max_length))
        print(w, 'Most common words in the dataset:',[self.id2word[i] for i in range(1,w+1)])
        for i in range(s):
            print('Line {}:  {}'.format(i + 1, self.sentences[i]))
            print('\tLine {}:  {}'.format(i + 1, self.sequences[i]))
        print('...etc...')        


T = Tokeniser()
T.display()
