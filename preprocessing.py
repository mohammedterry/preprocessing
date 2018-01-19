import collections
import os
import keywords as kw

class Preprocess:
    def __init__(self, path = 'cleantext.txt'):  
        self.load(path)     

    def load(self, path):
        '''
        INPUTS: 
            - path (string): the input file containing the text to analyse (NB: for best results, text should be tidy - if not, use tidyup() first)
        '''
        with open(path, 'r', errors = 'ignore') as f: 
            self.sentences = [sentence.strip(kw.IGNORE) for sentence in f.readlines()]           

    def concatinate(self, input_paths = [f for f in os.listdir(os.getcwd()) if f.endswith('.txt')], output_path = 'cleantext.txt'):
        '''
        concatinates all text files in the directory while formatting the text as it goes
        INPUTS:
            - input_paths (list): default = all text files in current directory: list of filenames for  input text files to concatinate
            - output_path (string): default '00000.txt': this is the name and type of file the concatinated text is saved to
        OUTPUTS:
            - 00000.txt (file): the combined text from all input files with some formatting to make them neat and tidy (for more accurate analysis):
                - all words separated by a single whitespace
                - all sentences on their own line
                - all files separated by a marker +++filename+++
        '''
        with open(output_path, 'w') as output_file:  
            for path in input_paths:
                print(path)
                with open(path, 'r', errors = 'ignore') as input_file: 
                    output_file.write('\n+++' + path + '+++\n')
                    self._tidyup(input_file.read(), output_file)

    def _tidyup(self, raw_text, output_file):
        '''
        robust, lightweight, rule-based Tokeniser that finds sentence boundaries 
        (doesnt relying on capital letters) 
        it is also able to detect two words joint together like.this
        
        Rule 1:  no punctuation inside brackets create a new sentence (...him. Then...) 
        Rule 2a:  .!? followed by '" creates a new sentence starting AFTER the '"
        Rule 2b:  !? followed by anything creates a new sentence BUT not so for .
        Rule 2c:  .!? followed by ., doesnt create a new sentence
        Rule 3a:  1-9 before . doesnt create a new sentence
        Rule 3b:  abbrev. words before . dont usually create new sentences
        Rule 3c: words with normal word endings before . usually create new sentences
        Rule 3d:  closed brackets before . usually create new sentences
        
        INPUTS:
            - raw_text (string): the text to tidyup
        OUTPUTS:
            - output_file (file): the file where the tidy text is being written to
        '''
        #remove any prior formatting
        characters = kw.PADDING + raw_text.replace('<br />', ' ').replace('\n',' ') + kw.PADDING #remove newlines etc
        characters = ' '.join(characters.split()) #remove trailing whitespace
        #flags
        open_brackets = [0,0,0] #{[(<-- without --> }])    
        skip = False        
        #scan through characters
        for i in range(3, len(characters)-3):
            character= characters[i]
            output_file.write(character)
            #optional formatting to separate fused.words!like-this
            if not(character.isalpha() or character in kw.NUMBERS): 
                nex = characters[i+1]
                if nex != ' ':
                    output_file.write(' ')
            #keep track if we are inside brackets for Rule 1
            if character in kw.BRACKETS:
                for i in range(1,4): #cycle through each type of bracket and make a note
                    if character == kw.BRACKETS[i-1]: #{[( opening brackets
                        open_brackets[i-1] += 1
                    elif character == kw.BRACKETS[-i]: #)]} closing brackets
                        open_brackets[i-1] = max(0, open_brackets[i-1] - 1) #no negative values permitted - to avoid messing with sum() check later
            #RIPPLEDOWN RULES
            if not(sum(open_brackets)): #Rule 1
                if skip: #Rule 2a
                    output_file.write('\n')
                    skip = False
                if character in kw.STOPMARKS:
                    if nex in kw.SPEECHMARKS: #Rule 2a
                        skip = True
                    elif nex.isalpha() or nex == ' ': #Rule 2c
                        if character == '.': 
                            p = characters[i-1]
                            if p in kw.BRACKETS[3:]: #Rule 3d
                                output_file.write('\n')
                            elif p.isalpha(): #Rule 3a
                                #get all of previous word
                                prev = characters[i] 
                                j = 1
                                while characters[i-j].isalpha():
                                    prev += characters[i-j].lower()
                                    j += 1
                                prev = prev[::-1] #reverse it
                                if prev not in kw.ABBREVIATIONS: #Rule 3b
                                    if self._normal_ending(prev[:-1]):  #Rule 3c
                                        output_file.write('\n') 
                        else: #Rule 2b
                            output_file.write('\n')

    def _normal_ending(self, word):
        if len(word) >= 2:
            penultimate, ultimate = word[-2].lower(), word[-1].lower()
            if ultimate in kw.ENDINGS:
                if penultimate in kw.ENDINGS[ultimate]:
                    return True
        return False

    def analyse(self, ordered = True, padding = False, window_size = 3, threshold = 0.01):
        '''
        textual data analysed for: 
            - maximum sentence length (useful for knowing how much to pad)        
            - total word count
            - vocabulary (i.e. unique words)
            - most/least common words in the corpus
            - commonly associated words occuring before/after each word in the vocabulary
    
        INPUTS:
            - ordered (boolean): default True: the vocabulary of unique words will be ordered according to frequency of occurance (most-least common)
            - padding (boolean): default False: if true, each sentence will be padded to make them all the same length as the longest sentence
            - window_size (int): default 3: the number of words checked before and after the current word (i.e. window_size of 3 creates a window of 7 words [before,before,before,target,after,after,after])
            - threshold (float): default 0.05:
        OUTPUTS: 
            - vocab (list): a vocabulary (optionally sorted in order of occurance - i.e. most common word is first)
            - sequences (list) a dictionary of word IDs (each word in the vocabulary and a unique number- useful for training networks, etc)
            - collocations (dictionary): a collocations dictionary (each word in the vocabulary and commonly cooccuring words both before and after it)  
            (NB: all preprocessed information is displayed in terminal as well as written to an external file to be used after the program closes)          
        '''
        self.max_length = max([len(sentence.split()) for sentence in self.sentences])
        words = [word.lower().strip(kw.IGNORE) for sentence in self.sentences for word in sentence.split() if word not in kw.IGNORE]
        self.wordcount = len(words)
        word_freq = collections.Counter(words)
        if ordered: 
            self.vocab = [word for word, _ in word_freq.most_common()]            
        else: 
            self.vocab = [word for word in set(words)]
        self.id2word, self.word2id = self._wordEncodings(vocab = self.vocab) 
        self.sequences = [self._sequence(sentence, self.word2id) for sentence in self.sentences]
        if padding: 
            self.sequences = self._padding(self.sequences, self.max_length)
        self._collocations(self.vocab, self.id2word, self.sequences, window_size, threshold)        
        self.save(self.display(), self.context)
    
    def _wordEncodings(self, vocab):
        '''
        words are numbered off so that each word has a unique ID
        rather than use a hashing table to assign random IDs (which has the hashing problem)
        words are given numbers which correspond to their position in the vocabulary
        if the vocabulary is ordered - then their IDs will indicate their relative frequency of occurance
        - e.g. word "1" will be the most frequent word in the text analysed
        (NB: This approach of converting words into numbers is one of the more basic
        alternative approaches include Onehot vectors, bag of words, Sparse Distributed Vectors, hidden layer weights of a neural network, etc)

        INPUT: 
            - vocab (list): a list of unique words
        OUTPUT:
            - lookup (dictionary): the lookup table mapping IDs to Words
            - (dictionary): the lookup table mapping words to IDs
        '''
        lookup = {rank:word for rank,word in zip(range(1,len(vocab) + 1), vocab)}
        lookup[kw.PAD] = kw.PADDING
        return lookup, {v: k for k,v in lookup.items()}
        
    def _sequence(self, sentence, lookup):
        '''
        converts a sentence into a sequence of numbers/wordIDs
        
        INPUT:
            - sentence (string): the text to convert
            - lookup (dictionary): a word to id mapping
        OUTPUT:
            - (list): sequence of wordIDs
        '''
        return [lookup[word.lower().strip(kw.IGNORE)] for word in sentence.split() if word not in kw.IGNORE]

    def _padding(self, sequences, size):
        '''
        a padding symbol (e.g. '0') is appended to the end of each sequence 
        so that all sequencees have the same length (i.e. the length of the longest)
        this may be useful for training networks, etc

        INPUTS:
            - sequences (list): a list of numbers/wordIds
            - size (int): the size each sequence is to be padded to 
            (NB: assumes all sequences are shorter than or equal to this size)
        OUTPUTS:
            - sequences (list): the list of numbers/wordIDs with padding appended to the end
        '''
        for i in range(len(sequences)):
            sequences[i] += [kw.PAD]*(size - len(sequences[i])) 
        return sequences

    def _collocations(self, vocab, wordIDs, sequences, window_size, threshold): 
        '''
        this scans each word and collects the most common occuring words which co-occur before and after it

        INPUTS:
            - vocab (list): list of unique words
            - wordIDs (dictionary): ID-word mapping to convert IDs back into words
            - sequences (list): text as sequences of wordIDs (this is optional and we could have analysed the actual words)
            - window_size (int): the number of words which will be considered before / after a word 
            - threshold (float): words which occur less frequently than this lower bound percentage will not be saved as a collocation
        OUTPUTS:
            - context (dictionary): e.g. {...word : ([common,words,before,that,word], [common,words,after,that,word]) , ...}
        '''
        self.context = {word:[[],[]] for word in vocab}
        pad = [kw.PAD]*window_size # a buffer to compensate for the sliding window
        for sequence in sequences:
            sequence = pad + sequence + pad 
            for i in range(window_size*2 + 1,len(sequence)+1):
                window = sequence[i- (2*window_size + 1):i]
                target = window[window_size]
                if target != kw.PAD: #ignore the initial and final buffers
                    target = wordIDs[target] #convert word
                    self.context[target][0].extend(window[:window_size]) #add words seen before
                    self.context[target][1].extend(window[window_size+1:]) #add words seen after
        for k,v in self.context.items():
            before, after = v
            before_count, after_count = collections.Counter(before), collections.Counter(after)
            tot_before, tot_after = sum(before_count.values()), sum(after_count.values()) #total number of words seen before and after this word
            #only keep those collocated words which aren't buffer words and which occur more than the cutoff threshold
            self.context[k][0] = [wordIDs[word] for word, f in before_count.most_common() if word != kw.PAD if f /tot_before > threshold]            
            self.context[k][1] = [wordIDs[word] for word, f in after_count.most_common() if word != kw.PAD if f /tot_after > threshold]         

    def display(self, s = 3, w = 10): 
        '''
        displays the results of the analysis 
        
        INPUTS:
            - s (int): default 3: number of sentences to display from the input file (-1 displays all)
            - w (int): default 10: number of words to display (-1 displays all)
        OUTPUTS:
            - info (string): the data returned as a string
        '''
        if s == -1: 
            s = len(self.sentences)  
        if w == -1: 
            w = len(self.vocab)
        r = self.vocab[int(input('enter a number >'))]
        info = ''' 
            {} unique words.     
            {} words in total.
            {} words is the length of the longest sentence.
            {} most common words in the dataset: {}
            For the word "{}",
                most common words found before it are {}
                most common words found after it are {}
        '''.format(len(self.vocab), self.wordcount, self.max_length, w, [self.id2word[i] for i in range(1,w+1)], r, self.context[r][0], self.context[r][1])
        for i in range(s):
            info += '\nLine {}:  {}'.format(i + 1, self.sentences[i])
            info += '\n\tLine {}:  {}'.format(i + 1, self.sequences[i])
        info += '\n...etc...'    
        print(info)    
        return info

    def save(self, header, collocations):
        '''
        the collocations dictionary is dumped to an external file
        as well as the collocations for each word
        this also implicitely contains the vocabulary (the keys)
        ordered in the most-least frequent occurances
        so that - the first word in the dictionary is the most common in the vocabulary

        INPUT:
            - header (string): a small piece of text to append to the top of the file
            - collocations (dictionary): a hashtable of each word in the vocabulary (ordered by frequency of occurance) and the words commonly associated with it occuring before and after
                (e.g. {...word1: [[words,before,it],[words,after,it]]...} )
        OUTPUT:
            - vocabulary.py (file): containing the header and collocations dictionary
                (NB: this could also be achieved using pickle or numpy.save('context.npy', collocations) 
                - however, this way allows anyone to read the dictionary without running a program)
        '''
        with open('vocabulary.py','w') as f:
            f.write("'''" + header + "'''")
            f.write('\n\n\ncontext = {')
            for key, value in collocations.items():
                f.write('\n\t"' + str(key) + '"' + ' : ' + str(value) + ',') 
            f.write('\n}')

#TEST
#Preprocess('small_vocab').analyse()
Preprocess('refined_text.txt').analyse()

