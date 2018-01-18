# Preprocessing
program for preprocessing words for NLP tasks

![](https://raw.githubusercontent.com/mohammedterry/preprocessing/master/screenshots.jpg)

## Sentence Boundary Detection
This part uses a rule-based algorithm to detect ends of sentences. 
It can even detect false full stops 
and ends of sentences without any punctuation marks used
![](https://raw.githubusercontent.com/mohammedterry/preprocessing/master/detecting%20sentence%20boundaries.jpg)
Here is it working on a real text file - this has been autoformatted using the algorithm!
![](https://raw.githubusercontent.com/mohammedterry/preprocessing/master/autoformatting%20using%20sentence%20splitter.jpg)

## Update
Ive completely remade the boundary detection rules 
This one is my own design completely 
and very lightweight
it analyses the sentence character-wise - not word-wise.  It also doesnt use a massive dictionary - its main power comes from the ability to recognise normal words!  Ever notice that words look almost the same from the endings.  THats how it works.  For the last letter of the word, there are only so many possible penultimate letters that can precede it to make a coherent word.  Voila!    The results are far more impressive.  Have a look
![](https://raw.githubusercontent.com/mohammedterry/preprocessing/master/new_splitter.jpg)
![](https://raw.githubusercontent.com/mohammedterry/preprocessing/master/beforeafter.jpg)
![](https://raw.githubusercontent.com/mohammedterry/preprocessing/master/so%20good.jpg)
