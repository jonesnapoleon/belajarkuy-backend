import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pandas as pd

from src.util.constant import Constant
from src.recommender import Recommender
from src.process.cleaner import Cleaner

def init_recommender():
    data = pd.read_csv(os.path.join(Constant.DATA_PATH, 'raw', 'train.csv'))

    if os.path.isfile(Constant.FEATURES_PATH) and os.path.isfile(Constant.DICT_FEAT_PATH):
        print('[LOG] Found Dumped File')
    else:
        print('[LOG] Cleaning Data')
        cleaner = Cleaner()
        data = cleaner.clean(data)

    preprocessor_path = os.path.join(Constant.PREPROCESSOR_PATH, 'preprocessor.pkl')
    model_path = os.path.join(Constant.MODEL_PATH, 'conv_lstm', 'Conv1D-LSTM (acc_0.85-val_acc_0.61-train_f1_0.79-val_f1_0.47).h5')

    recommender = Recommender(data, preprocessor_path, model_path)
    return recommender