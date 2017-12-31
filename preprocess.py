import os
import collections

class Preprocess:
    IGNORE='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'    
    PAD = 0

    def __init__(self, path = 'small_vocab', ordered = True, hashing = False, padding = False, window_size = 3):  
        self.load(path = path, ordered = ordered)     
        self.tokenise(hashing = hashing) 
        self.sequences = [self.sequence(sentence, padding = padding) for sentence in self.sentences]
        self.collocations(window_size = window_size)
        self.display()

    def load(self, path, ordered):
        input_file = os.path.join(path)
        with open(input_file, "r") as f:
            data = f.read()
        self.sentences = [sentence.strip(self.IGNORE) for sentence in data.split('\n')]
        self.max_length = max([len(sentence.split()) for sentence in self.sentences])
        words = [word.lower().strip(self.IGNORE) for sentence in self.sentences for word in sentence.split() if word not in self.IGNORE]
        self.wordcount = len(words)
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
        self.id2word[self.PAD] = '<pad>'
        self.word2id = {d[1]: d[0] for d in self.id2word.items()}
        #alternatively, use sdr vectors to represent words

    def sequence(self, sentence, padding = True):
        pad = [] 
        if padding: pad = [self.PAD]*(self.max_length - len(sentence.split())) 
        return pad + [self.word2id[word.lower().strip(self.IGNORE)] for word in sentence.split()  if word not in self.IGNORE]

    def collocations(self, window_size): #sliding window size = +/- n
        self.pre = {word:[] for word in self.vocab}
        self.post = {word:[] for word in self.vocab}
        pad = [self.PAD]*window_size
        for sequence in self.sequences:
            sequence = pad + sequence + pad
            for i in range(window_size*2 + 1,len(sequence)+1):
                window = sequence[i- (2*window_size + 1):i]
                target = window[window_size]
                if target != self.PAD:
                    target = self.id2word[target]
                    self.pre[target].extend(window[:window_size])
                    self.post[target].extend(window[window_size+1:])
        for a, b in zip(self.pre.items(), self.post.items()):
            c1, c2 = collections.Counter(a[1]), collections.Counter(b[1])
            self.pre[a[0]] = [self.id2word[word] for word, f in c1.most_common() if word != self.PAD if f > 10 ]            
            self.post[b[0]] = [self.id2word[word] for word, f in c2.most_common() if word != self.PAD if f > 10 ]            

    def shift(self, sequence):
        return sequence[1:] + [self.PAD]

    def display(self, s = 3, w = 10): 
        #s & w are number of sentences & words to display (-1 displays all)
        if s == -1: s = len(self.sentences)
        if w == -1: w = len(self.vocab)
        print()
        print('{} unique words.'.format(len(self.vocab)))
        print('{} words in total.'.format(self.wordcount))
        print('{} words is the length of the longest sentence.'.format(self.max_length))
        print(w, 'Most common words in the dataset:',[self.id2word[i] for i in range(1,w+1)])
        r = self.vocab[w] 
        print('Most common words found immediately before "{}":'.format(r),self.pre[r])
        print('Most common words found immediately after "{}":'.format(r),self.post[r])
        print()
        for i in range(s):
            print('Line {}:  {}'.format(i + 1, self.sentences[i]))
            print('\tLine {}:  {}'.format(i + 1, self.sequences[i]))
        print('...etc...')        


P = Preprocess()
