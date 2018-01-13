import os
import collections

class Preprocess:
    IGNORE='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'    
    PAD = 0

    def __init__(self, path, ordered = True, hashing = False, padding = False, window_size = 3, threshold = 0.05):  
        self.load(path = path, ordered = ordered)     
        self.tokenise(hashing = hashing) 
        self.sequences = [self.sequence(sentence) for sentence in self.sentences]
        if padding: self.padding()
        self.collocations(window_size = window_size, threshold = threshold)

    def load(self, path, ordered):
        input_file = os.path.join(path)
        with open(input_file, "r") as f: data = f.read()
        self.sentences = [sentence.strip(self.IGNORE) for sentence in data.split('\n')]
        self.max_length = max([len(sentence.split()) for sentence in self.sentences])
        words = [word.lower().strip(self.IGNORE) for sentence in self.sentences for word in sentence.split() if word not in self.IGNORE]
        self.wordcount = len(words)
        word_freq = collections.Counter(words)
        if ordered: self.vocab = [word for word, _ in word_freq.most_common()]            
        else: self.vocab = [word for word in set(words)]

    def tokenise(self, hashing):
        if hashing: #some vocab gets lost due to hashing problem
            self.id2word = {(hash(w) % (len(self.vocab) - 1) + 1) : w for w in self.vocab}
        else: #number off according to frequency - e.g. 1 is most frequent word in vocab
            self.id2word = {i:w for i,w in zip(range(1,len(self.vocab) + 1), self.vocab)}
        self.id2word[self.PAD] = '<pad>'
        self.word2id = {d[1]: d[0] for d in self.id2word.items()}
        #alternatively, use sdr vectors to represent words

    def sequence(self, sentence):
        return [self.word2id[word.lower().strip(self.IGNORE)] for word in sentence.split() if word not in self.IGNORE]

    def padding(self):
        for i in range(len(self.sequences)):
            self.sequences[i] += [self.PAD]*(self.max_length - len(self.sequences[i])) 

    def collocations(self, window_size, threshold): #sliding window size = +/- n
        self.context = {word:[[],[]] for word in self.vocab}
        pad = [self.PAD]*window_size
        for sequence in self.sequences:
            sequence = pad + sequence + pad
            for i in range(window_size*2 + 1,len(sequence)+1):
                window = sequence[i- (2*window_size + 1):i]
                target = window[window_size]
                if target != self.PAD:
                    target = self.id2word[target]
                    self.context[target][0].extend(window[:window_size])
                    self.context[target][1].extend(window[window_size+1:])
        for a in self.context.items():
            c1, c2 = collections.Counter(a[1][0]), collections.Counter(a[1][1])
            tot1, tot2 = sum(c1.values()), sum(c2.values())
            self.context[a[0]][0] = [self.id2word[word] for word, f in c1.most_common() if word != self.PAD if f /tot1 > threshold ]            
            self.context[a[0]][1] = [self.id2word[word] for word, f in c2.most_common() if word != self.PAD if f /tot2 > threshold]         
        #save this to file for use with sdrs, etc 
        # alternatively use pickle or numpy packages
        # e.g. np.save('context.npy', self.context)
        with open('vocabulary.py', 'w') as f: 
            f.write('context = {')
            for key, value in self.context.items():
                f.write('"' + str(key) + '"' + ' : ' + str(value) + ',\n\t') 
            f.write('}')

    def shift(self, sequence):
        return sequence[1:] + [self.PAD]

#new function called Sdrs
#from sdr import SDR
#create vocab in sdr form
#first create vocab list using 1D sdrs - so that duplicate words that were mispelt are combined
# record size of vocab before & after conversion - indicating number of typos in vocab
# then create a second vocab list of 3D sdrs - with contexts provided

    def display(self, s = 3, w = 10): 
        #s & w are number of sentences & words to display (-1 displays all)
        if s == -1: s = len(self.sentences)
        if w == -1: w = len(self.vocab)
        print()
        print('{} unique words.'.format(len(self.vocab)))         #unique words, len(self.vocab_sdr)
        print('{} words in total.'.format(self.wordcount))
        #number of typos detected, len(self.vocab) - len(self.vocab_sdr1D)
        print('{} words is the length of the longest sentence.'.format(self.max_length))
        print(w, 'Most common words in the dataset:',[self.id2word[i] for i in range(1,w+1)])
        r = self.vocab[int(input('enter a number >'))] 
        print('Most common words found before "{}":'.format(r),self.context[r][0])
        print('Most common words found after "{}":'.format(r),self.context[r][1])
        print()
        for i in range(s):
            print('Line {}:  {}'.format(i + 1, self.sentences[i]))
            print('\tLine {}:  {}'.format(i + 1, self.sequences[i]))
        print('...etc...')        

#test
#Preprocess('small_vocab').display()