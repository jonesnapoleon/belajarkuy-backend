import warnings
warnings.filterwarnings('ignore')
import os
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"]="true"

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Embedding, Dense, LSTM, Dropout, Conv1D, GlobalAveragePooling1D, Concatenate

class ConvLSTMModel(Model):

    def __init__(self, 
                 total_words, 
                 input_length,
                 n_class):
        super(ConvLSTMModel, self).__init__()
        self.dropout = Dropout(rate=0.2)
        self.input_layer = Input((input_length))
        self.embedding = Embedding(total_words, 512, input_length=input_length)
        
        # LSTM
        self.lstm1 = LSTM(256, return_sequences=True)
        self.lstm2 = LSTM(512)
        
        # 2 gram
        self.gram2 = Conv1D(256, 2, activation='relu')

        # 3 gram
        self.gram3 = Conv1D(256, 3, activation='relu')

        # 4 gram
        self.gram4 = Conv1D(256, 4, activation='relu')

        # fivegram
        self.gram5 = Conv1D(256, 4, activation='relu')

        self.pool = GlobalAveragePooling1D()

        # Concatenate
        self.concatenate = Concatenate()

        # Classificator
        self.dense1 = Dense(256, activation='relu')
        self.classificator = Dense(n_class, activation='softmax')
        self.out = self.call(self.input_layer)

    def call(self, inputs, feature_only=False, training=None):
        x = self.embedding(inputs)
        lstm_x = self.lstm1(x)
        lstm_x = self.dropout(lstm_x, training=training)
        lstm_x = self.lstm2(lstm_x)

        gram_2 = self.gram2(x)
        gram_2 = self.pool(gram_2)

        gram_3 = self.gram3(x)
        gram_3 = self.pool(gram_3)

        gram_4 = self.gram4(x)
        gram_4 = self.pool(gram_4)
        
        gram_5 = self.gram5(x)
        gram_5 = self.pool(gram_5)

        x = self.concatenate([lstm_x, gram_2, gram_3, gram_4, gram_5])

        if feature_only:
            return x

        x = self.dropout(x, training=training)

        x = self.dense1(x)
        return self.classificator(x)