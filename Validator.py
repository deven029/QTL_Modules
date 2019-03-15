from flask import Flask
from expletives import badwords
app = Flask(__name__)

@app.route("/header_check/<string:header>")
def header_combinations(header):
    header_combination = []
    header_length = len(header)
    for i in range (header_length-2):
        header_combination.append(header[i:i+3])
    for i in range (header_length-3):
        header_combination.append(header[i:i+4])
    for i in range(header_length - 4):
        header_combination.append(header[i:i + 5])
    for i in range(header_length - 5):
        header_combination.append(header[i:i + 6])
    for i in range(header_length - 6):
        header_combination.append(header[i:i + 7])
    for i in range(header_length - 7):
        header_combination.append(header[i:i + 8])
    for i in range(header_length - 8):
        header_combination.append(header[i:i + 9])
    for i in range(header_length - 9):
        header_combination.append(header[i:i + 10])
    for i in range(header_length - 10):
        header_combination.append(header[i:i + 11])
    for header_word in header_combination:
        if badwords.__contains__(header_word):
            return '0'
    else:
        return '1'

@app.route("/message_check/<string:message>")
def message_template_check(message):
    promotional_words = message.split()
    filename = ('promoWordDict.txt')
    f = open(filename)
    wordlist = f.readlines()
    wordlist = [w.strip() for w in wordlist if w]
    for promo_word in promotional_words:
        if wordlist.__contains__(promo_word):
            return '0'
    else:
        return '1'


app.run()
