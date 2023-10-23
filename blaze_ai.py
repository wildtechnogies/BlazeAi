from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import time

class Blaze():
    def __init__(self, text):
        self.text = text
        self.stopWords = set(stopwords.words("english"))
        self.words = word_tokenize(text)

    stopWords = set(stopwords.words("english"))

    def get_summary(self):

        # Creating a frequency table to keep the
        # score of each word

        freqTable = dict()
        for word in self.words:
            word = word.lower()
            if word not in self.stopWords:
                if word in freqTable:
                    freqTable[word] += 1
                else:
                    freqTable[word] = 1

        # Creating a dictionary to keep the score of each sentence
        sentences = sent_tokenize(self.text)
        sentenceValue = dict()

        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq

        sumValues = 0
        for sentence in sentenceValue:
            sumValues += sentenceValue[sentence]

        # Average value of a sentence from the original text

        average = int(sumValues / len(sentenceValue))

        summary = ''
        for sentence in sentences:
            if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
                summary += " " + sentence

        return summary

    def exact_Search(self, query):
        words = word_tokenize(query)
        freqTable = dict()
        for word in words:
            word = word.lower()
            if word not in self.stopWords:
                if word in freqTable:
                    freqTable[word] += 1
                else:
                    freqTable[word] = 1

        # Creating a dictionary to keep the score of each sentence
        sentences = sent_tokenize(self.text)
        sentenceValue = dict()

        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq

        try:
            match = max(zip(sentenceValue.values(), sentenceValue.keys()))[1]
            return match
        except:
            return "Couldn't find relevant data"

print('#'*30 + 'Blaze AI Student v0.1' + '#'*30)
x = str(input('Enter the data to be loaded : '))
model = Blaze(x)
print('Model Loaded')
print('#'*30 + 'Summary' + '#'*30)
print(model.get_summary())
print('#'*30 + 'Summary' + '#'*30)
time.sleep(3)
while True:
    query = str(input('Enter the question : '))
    if query != None:
        print('#'*30)
        print('Answer found : ' + model.exact_Search(query))
    else: continue