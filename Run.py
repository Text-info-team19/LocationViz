from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, request, render_template
from nltk import ne_chunk, pos_tag, word_tokenize
import nltk

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
    file = open(text ,'r')
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

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)