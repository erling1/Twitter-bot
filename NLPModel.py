# Core TensorFlow and Keras
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, Lambda, LSTM
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

# Data processing and visualization
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Custom modules
from scrape import ScrapAndFilter
import json

class NLPmodel:

    def __init__(self):

        self.tokenizer = Tokenizer()
        self.max_length = 5


    def fit_tokenizer(self, news_headlines,sentiment):

        self.tokenizer.fit_on_texts(news_headlines)
        sequences = self.tokenizer.texts_to_sequences(news_headlines)

         # Maximum length of each sequence
        padded_sequences = pad_sequences(sequences, maxlen=self.max_length)

        

        vocab_size = len(self.tokenizer.word_index) + 1
        embedding_dim = 16

        labels = np.array(sentiment)

        labels_categorical = to_categorical(labels, num_classes=3)



        model = Sequential([
    
        Embedding(vocab_size, embedding_dim, input_length=self.max_length), LSTM(64, return_sequences=True), LSTM(32),
                                                                    tf.keras.layers.Dropout(0.2),
                                                                    Dense(3, activation='softmax')  ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
       

        print("Type Padded Seq: ", type(padded_sequences))
        print("Type Labels:", type(labels_categorical))
        
        history = model.fit(padded_sequences, 
                   labels_categorical,
                   epochs=10,
                   batch_size=32,
                   validation_split=0.2)
        
        return model


    def predict(self, headlines, model):
        new_sequence = self.tokenizer.texts_to_sequences(headlines)
        new_padded = pad_sequences(new_sequence, maxlen=self.max_length)
        
        # Get prediction probabilities
        prediction = model.predict(new_padded)

        print(len(prediction))
        print(len(headlines))

        print(np.shape(prediction))

        
        
        
        # Get probabilities for each class
        sentiment_prob = {
            'Negative': prediction[0][0],
            'Neutral': prediction[0][1],
            'Positive': prediction[0][2]
        }
        
        return prediction





test = ScrapAndFilter()

news_headlines = test.filter_news()



with open('norwegian_political_headlines_10000.json', 'r') as file:
    data = json.load(file)



headlines = []
labels = []

headlines = [item['headline'] for item in data]
labels = [label['sentiment'] for label in data]


model = NLPmodel()

seq_model = model.fit_tokenizer(headlines, labels)

preds = model.predict(news_headlines, seq_model)



print(preds)






#model.fit_tokenizer(news_headlines=news_headlines)

#test on data:
#model.predict(news_headlines=news_headlines)