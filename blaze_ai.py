import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from flask import Flask, request, render_template

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

model = Blaze('')

def loadModel(text):
    global model
    model = Blaze(text)
    return model.get_summary()

def search(query):
    global model
    return model.exact_Search(query)

app = Flask(__name__)
def blazeAi_response(user_input):
    global model
    try:
        return  model.exact_Search(user_input)
    except:
        return "Data isn't loaded"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    bot_response = blazeAi_response(user_input)
    return bot_response

@app.route('/process_file', methods=['POST'])
def process_file():
    file = request.files['file']
    if file and file.filename.endswith('.txt'):
        file.save(file.filename)
        with open(file.filename) as f:
            dta = ' '
            cont = f.readlines()
            for line in cont:
                dta += line
            bot_response = loadModel(dta)
        return bot_response
    else:
        return "Invalid file. Please upload a .txt file."


if __name__ == '__main__':
    app.run(debug=True)
