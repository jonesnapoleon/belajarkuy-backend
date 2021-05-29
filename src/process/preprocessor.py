import numpy as np

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

from sklearn.preprocessing import OneHotEncoder

class Preprocessor():
    
    def __init__(self):
        self.tokenizer = Tokenizer(filters='')
        self.encoder = OneHotEncoder()
        self.maxlen = 0
        self.n_class = 0
    
    def fit(self, data):
        self.tokenizer.fit_on_texts(data['questions'].values)
        self.encoder.fit(data[['chapter']])

    def transform(self, data, meta=False):
        labels = self.encoder.transform(data[['chapter']]).toarray()
        sequences = self.tokenizer.texts_to_sequences(data['questions'].values)

        if not meta:
            self.maxlen = max([len(x) for x in sequences])
            self.n_class = len(labels[0])
        
        sequences = np.array(pad_sequences(sequences, maxlen=self.maxlen, padding='pre'))
        return sequences, labels

    def text_to_sequence(self, text):
        seq = self.tokenizer.texts_to_sequences([text])
        return np.array(pad_sequences(seq, maxlen=self.maxlen, padding='pre'))

    def fit_transform(self, data):
        self.fit(data)
        return self.transform(data)
