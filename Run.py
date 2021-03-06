import os
import nltk
import urllib2
from flask import Flask, render_template, request, redirect, url_for
from nltk import ne_chunk, pos_tag, word_tokenize

from nltk.tag import StanfordNERTagger
from nltk.tag.stanford import CoreNLPNERTagger
from itertools import groupby

# path to local directory where Stanfprd-NER is installed
# enter YOUR user name in the next line: stanford_dir = '/Users/<username>/stanford-ner-2017-06-09/'
stanford_dir = '/Users/hadas/stanford-ner-2017-06-09/'
jarfile = stanford_dir + 'stanford-ner.jar'
modelfile = stanford_dir + 'classifiers/english.all.3class.distsim.crf.ser.gz'
st = StanfordNERTagger(model_filename=modelfile, path_to_jar=jarfile)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selectedValue = request.form['selection']
        return redirect(url_for('click', selectedValue=selectedValue))
    return render_template('main.html')

@app.route('/main', methods=['GET', 'POST'])
def home1():
    if request.method == 'POST':
        selectedValue = request.form['selection']
        return redirect(url_for('click', selectedValue=selectedValue))
    return render_template('main.html')



@app.route('/<selectedValue>', methods=['GET', 'POST'])
def click(selectedValue):
    return render_template(selectedValue + '.html')

@app.route('/R_txt', methods=['POST'])
def my_form_post():
    text1 = request.form['myText']   
    ne_text=[]

    for sent in nltk.sent_tokenize(text1):
      for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
        if hasattr(chunk, 'label'):
	   #print(chunk.label(), ' '.join(c[0] for c in chunk))
           ne_text.append (' '.join(c[0] for c in chunk))     
    return str(ne_text)     

@app.route('/R_file', methods=['POST'])
def my_form_post1():
    text = request.form['myFile']
    fname = os.path.basename(text)
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))    
    file = open(ROOT_DIR+'/dataset/'+fname ,'r')
    my_sent = file.read()
    file.close()
    ne_text1=[]

    for sent in nltk.sent_tokenize(my_sent):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            #if hasattr(chunk, 'label'):
               if hasattr(chunk,'label') and chunk.label() == 'GPE':
               #print(chunk.label(), ' '.join(c[0] for c in chunk))
                #print(''.join(c[0] for c in chunk))            
                ne_text1.append (' '.join(c[0] for c in chunk))     
    return str(ne_text1)        

@app.route('/R_url', methods=['POST'])
def my_form_post2():
    text = request.form['myurl']
    ne_text2 = []
    netagged_words = st.tag(urllib2.urlopen(str(text)).read().decode('unicode-escape').split())

    for tag, chunk in groupby(netagged_words, lambda x: x[1]):
        if tag == "LOCATION":
            ne_text2.append(" ".join(w for w, t in chunk))
    return str(ne_text2)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
