import pickle
from tensorflow.keras.models import model_from_json
import sys, os, re, csv, codecs, numpy as np, pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask import request, jsonify, json, render_template
from hate_speech_api import app
from tensorflow.keras import backend as K
import tensorflow as tf
import string
import re

MAX_NB_WORDS = 50000
data = pd.read_csv("hate_speech_api/resources/train.csv").fillna("none")

tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
tokenizer.fit_on_texts(data['text'].values)
word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

graph = tf.get_default_graph()


import praw


reddit = praw.Reddit(client_id='h9C1XC7RcYuNfA',
client_secret='Vpgia9o1iTVeHi5cGO38CmjD_xs', user_agent='Utsav bot')


def remove_URL(text):
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub(r'',text)

def remove_html(text):
    html=re.compile(r'<.*?>')
    return html.sub(r'',text)

def remove_punct(text):
    table=str.maketrans('','',string.punctuation)
    return text.translate(table)

CONTRACTION_MAP = {
"ain't": "is not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I would",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"i'd": "i would",
"i'd've": "i would have",
"i'll": "i will",
"i'll've": "i will have",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}

def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text



# Reference : https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)



def get_submission(url):
	subm = reddit.submission(url = url)
	title=subm.title
	selftext=subm.selftext
	new_str=title+' '+selftext
	
	new_str=expand_contractions(new_str)
	new_str=remove_URL(new_str)
	new_str=remove_punct(new_str)
	new_str=remove_html(new_str)
	
	new_str=remove_emoji(new_str)
	
	
	return new_str
	

def load_model():
	global loaded_model
	json_file = open('hate_speech_api/resources/lstm_no_glove.json', 'r')
	loaded_model = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model)
	loaded_model.load_weights("hate_speech_api/resources/lstm_no_glove.h5")

load_model()

@app.route('/', methods=['GET','POST'])
def page():
	return render_template('index.html')

def predict_test(n_str):

		n_str=get_submission(n_str)
		n_str = n_str.encode('utf-8')
		#nstr=str(nstr)
		predictions=score(n_str)
		app.logger.info('API called for string: ' + str(n_str) +'. (returned): ' + str(predictions))
		

		labels = ['AskIndia', 'Business/Finance', 'Coronavirus','Non-Political', 'Policy/Economy', 'Politics', 'Science/Technology']
		#print(labels[np.argmax(predictions)])

		return labels[np.argmax(predictions)]


@app.route('/pred', methods=['GET','POST'])
def predict():
	try:
		if request.method == 'POST':
			data = request.get_json(force=True)
			n_str = data.get('text')
			n_str=get_submission(n_str)

		if request.method == 'GET':
			n_str= request.args.get('text')

		n_str = n_str.encode('utf-8')
		#nstr=str(nstr)
		predictions=score(n_str)

		app.logger.info('API called for string: ' + str(n_str) +'. (returned): ' + str(predictions))
		

		labels = ['AskIndia', 'Business/Finance', 'Coronavirus','Non-Political', 'Policy/Economy', 'Politics', 'Science/Technology']
		print(labels[np.argmax(predictions)])

		return jsonify(labels[np.argmax(predictions)]),200

	except AssertionError as error:
		app.logger.error('API called for string: ' + n_str + 'Error: '+ error)

@app.route('/automated_testing', methods=['GET','POST'])
def getfile():
	f = request.files['upload_file']
	lines = list(f)
	res=dict()
	for i in lines:
		i=i.decode()
		print(str(i))
		flair=predict_test(i)
		print(flair)
		res[i]=flair

	res = json.dumps(res)
	#json_links_flares = json.loads(dict_links_flares)
	print(res)
	return res
		



def score(n_str):
	n_str = [n_str.decode("utf-8")]
	new_string = tokenizer.texts_to_sequences(n_str)
	new_string = pad_sequences(new_string, maxlen=512)

	with graph.as_default():
		prediction=loaded_model.predict(new_string)

	#K.clear_session()
	#prediction = loaded_model.predict(new_string)
	return prediction






