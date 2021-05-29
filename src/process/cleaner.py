from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

class Cleaner:
    def __init__(self):
        self.stop_words = stopwords.words('english')
        self.stop_words.extend(list(string.punctuation))
    
    def __remove_stopwords(self, sentence):
        tokens = word_tokenize(sentence)
        splitted_sentence = [token for token in tokens if token not in self.stop_words]
        return ' '.join(splitted_sentence)

    def clean(self, data):
        data['questions'] = data['questions'].apply(lambda x: self.__remove_stopwords(x))
        return data