def split_sentences(text, max_sentence_length = 24):
    '''
    rule-based algorithm to find sentence boundaries
    INPUT: large chunk of text
    OUTPUT: text formatted so that each sentence is on a newline
    '''
    sentence = text.replace('<br />', ' ').replace('\n', ' ').split() + [' ']*2 #ignore any prior newline formatting in text and pad
    line_length = 0 #keep track of the no. of words in the current line
    for i in range(len(sentence)-2):
        line_length += 1
        if sentence[i][-1] in ':!?':  #!?: appended to the end of a word usually indicate the end of a sentence
            sentence[i] += '\n' 
            line_length = 0
        if (sentence[i+1][0].isupper() or not sentence[i+1][0].isalpha()) and line_length > max_sentence_length:  #experimental - this detects a new sentence using capital letters alone!
            sentence[i] += '\n'
            line_length = 0
        if sentence[i][-1] in '.")]>': #fullstop at end of a word may just be an abbreviation Mr. - - (which can still be at the end of a sentence)
            if sentence[i+1][0].isupper() or not sentence[i+1][0].isalpha(): #next word starts with capital - a good sign that its a new sentence
                if not abbreviation(sentence[i]): #just make sure the word isnt an abbreviation - now we are sure this fullstop marks the end of a sentence
                    sentence[i] += '\n' 
                    line_length = 0
                elif line_length > 6: #this attempts to catch any abbreviations that happen to be the last word in the sentence!!!
                    sentence[i] += '\n' 
                    line_length = 0
    return ' '.join(sentence)

def abbreviation(word):
    '''
    Word is an abbreviation if it fulfils any one of these conditions:
    1) a commonly known abbreviation (hon.)
    2) single letter (C. or C) - except I
    3) single letters followed by periods (p.m. A.A.A.)
    4) contains no vowels nor lower case y (cf. vs. Dr.) - except occassionally for first letter (etc eg) - except its all in capitals as these are likely acronyms (CRB HP)
    '''
    known = 'Mr. Mrs.'.split()
    if word in known: 
        return True  #Rule1
    if word == 'I': 
        return False #Rule 2
    l = len(word)
    if l == 1:
        return True #Rule 2
    if l == 2:
        if word[0].isalpha() and word[-1] == '.': 
            return True #Rule 2
    if '.' in word[:-2]: 
        return True #Rule 3     
    allcaps, vowely = True, False
    if word[0].islower(): 
        allcaps = False
    for letter in word[1:]:
        if letter.islower(): 
            allcaps = False
        if letter in 'AEIOUaeiouy': 
            vowely = True
    return not(allcaps or vowely) #Rule 4

#TESTS
#1 testing abbreviation()
# tests = 'hon. ,. A. B C. MSc PhD pm A.A.A. eg cf vs Dr etc Oz mr Mr MRI my normal word'.split()
# for test in tests:
#    print(test, "=", abbreviation(test))

#2 testing split_sentences()
# sentence = '''
#     This is just a quick test! to see how well Mr. Mohammed's s.p.l.i.t.t.e.r. algorithm. works... or doesnt? hehehe.
#     It also has its own new lines which may not. indicate the end of
#     a sentence and thus these must be removed! can it do it? i hope so. 
#     Watch out for fal.se fullstops. e.g. like those. They dont indicate an end of sentence like this does. Impressive, no?
#     But the hardest, by Far, Is to detect a sentence boundary that ends with an abbreviation like this eg. Did it detect it?
#     o.k. fine. youre good. but how good. can you detect a new sentence without a fullstop to indicate it like this one here Well did it?
#     ah Easy Its Probably Just Detecting Capital Letters Like These
#     '''
# print(sentence)
# print(split_sentences(sentence))