import os

class Constant():
    MODEL_PATH = 'model'
    PREPROCESSOR_PATH = os.path.join('model', 'processor')
    DATA_PATH = 'data'
    MAX_DATA = 10000
    FEATURES_PATH = os.path.join('model', 'features.pkl')
    DICT_FEAT_PATH = os.path.join('model', 'dict_feat.pkl')