import os
import collections

class Tokeniser:
    filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'    
 
    def __init__(self, path = 'small_vocab', ordered = True, hashing = False):  
        self.load(path = path, ordered = ordered)     
        self.tokenise(hashing = hashing)

    def load(self, path, ordered):
        input_file = os.path.join(path)
        with open(input_file, "r") as f:
            data = f.read()
        self.sentences = data.split('\n')
        self.max_length = max([len(sentence.strip(self.filters).split()) for sentence in self.sentences])
        self.words = [word.lower().strip(self.filters) for sentence in self.sentences for word in sentence.split() if word not in self.filters]
        word_freq = collections.Counter(self.words)
        if ordered:
            self.vocab = [word for word, _ in word_freq.most_common()]            
        else:
            self.vocab = [word for word in set(self.words)]

    def tokenise(self, hashing):
        if hashing: #some vocab gets lost due to hashing problem
            self.id2word = {(hash(w) % (len(self.vocab) - 1) + 1) : w for w in self.vocab}
        else: #number off according to frequency - e.g. 1 is most frequent word in vocab
            self.id2word = {i:w for i,w in zip(range(1,len(self.vocab) + 1), self.vocab)}
        self.word2id = {d[1]: d[0] for d in self.id2word.items()}

    def pad(self):
        pass
        
    def display(self, n = 3, f = 10):
        for i in range(n):
            print('Line {}:  {}'.format(i + 1, self.sentences[i]))
        print('...etc...')
        print('{} words is the length of the longest sentence.'.format(self.max_length))
        print('{} words in total.'.format(len(self.words)))
        print('{} unique words.'.format(len(self.vocab)))
        print(f, 'Most common words in the dataset:',[self.id2word[i] for i in range(1,f+1)])
        


T = Tokeniser()
T.display()

