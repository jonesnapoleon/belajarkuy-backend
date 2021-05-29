import pickle
from tqdm import tqdm
import numpy as np
import os

from sklearn.metrics.pairwise import cosine_similarity

from src.model.lstm_conv import ConvLSTMModel
from src.util.constant import Constant

class Recommender:
    def __init__(self, data, preprocessor_path, model_path):
        self.data = data
        self.preprocessor = pickle.load(open(preprocessor_path, 'rb'))
        self.model = ConvLSTMModel(len(self.preprocessor.tokenizer.word_index) + 1, 
                                    self.preprocessor.maxlen, 
                                    self.preprocessor.n_class)

        self.model.build((None, self.preprocessor.maxlen))
        self.model.load_weights(model_path)
        self.__transform_data()
        self.__featuring_data()

    def __transform_data(self):
        self.x, self.label = self.preprocessor.transform(self.data, meta=True)

    def __featuring_data(self):
        if os.path.isfile(Constant.FEATURES_PATH) and os.path.isfile(Constant.DICT_FEAT_PATH):
            self.features = np.load(Constant.FEATURES_PATH, allow_pickle=True)
            with open(Constant.FEATURES_PATH, 'rb') as f:
                self.features = pickle.load(f)
            with open(Constant.DICT_FEAT_PATH, 'rb') as f:
                self.dict_feat = pickle.load(f)
            return

        self.features = {}
        self.dict_feat = {}

        BATCH = 64
        batched_data = []
        batched_row = []
        temp_data = []
        temp_row = []
        counter = 0

        for instance, (_, row) in zip(self.x, self.data.iterrows()):
            counter += 1
            temp_data.append(instance)
            temp_row.append(row)
            if counter == BATCH:
                counter = 0
                batched_data.append(np.array(temp_data))
                batched_row.append(temp_row)
                temp_data = []
                temp_row = []
        if counter != 0:
            batched_data.append(np.array(temp_data))
            batched_row.append(temp_row)
            
        for batched_instance, b_row in tqdm(zip(batched_data, batched_row), total=len(batched_data)):
            features = self.model(batched_instance, feature_only=True)
            for feature, row in zip(features, b_row):
                # Validation
                if row['subject'] not in self.features:
                    self.features[row['subject']] = {}
                if row['chapter'] not in self.features[row['subject']]:
                    self.features[row['subject']][row['chapter']] = []

                self.features[row['subject']][row['chapter']].append((feature, row))
                self.dict_feat[row['q_id']] = (feature.numpy(), row['subject'], row['chapter'])

        # self.features.dump(Constant.FEATURES_PATH)
        with open(Constant.FEATURES_PATH, 'wb') as f:
            pickle.dump(self.features, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open(Constant.DICT_FEAT_PATH, 'wb') as f:
            pickle.dump(self.dict_feat, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    def get_recommendations(self, id):
        recommendations = []

        feature, subject, chapter = self.dict_feat[id]
        lstm_feature = feature[:512]
        gram_2_feature = feature[512:512+256]
        gram_3_feature = feature[512+256:512+256*2]
        gram_4_feature = feature[512+256*2:512+256*3]
        gram_5_feature = feature[512+256*3:512+256*4]
        
        checked_text = {
            'lstm_feature': [],
            'gram_2_feature': [],
            'gram_3_feature': [],
            'gram_4_feature': [],
            'gram_5_feature': []
        }
        for el in self.features[subject][chapter]:
            checked_text['lstm_feature'].append(el[0][:512])
            checked_text['gram_2_feature'].append(el[0][512:512+256])
            checked_text['gram_3_feature'].append(el[0][512+256:512+256*2])
            checked_text['gram_4_feature'].append(el[0][512+256*2:512+256*3])
            checked_text['gram_5_feature'].append(el[0][512+256*3:512+256*4])

        similarity_feat = {
            'lstm': cosine_similarity([lstm_feature], checked_text['lstm_feature'])[0],
            'gram_2': cosine_similarity([gram_2_feature], checked_text['gram_2_feature'])[0],
            'gram_3': cosine_similarity([gram_3_feature], checked_text['gram_3_feature'])[0],
            'gram_4': cosine_similarity([gram_4_feature], checked_text['gram_4_feature'])[0],
            'gram_5': cosine_similarity([gram_5_feature], checked_text['gram_5_feature'])[0]
        }

        similarity = []
        for i in range(len(checked_text['lstm_feature'])):
            mean = (similarity_feat['lstm'][i] + similarity_feat['gram_2'][i] + similarity_feat['gram_3'][i] + similarity_feat['gram_4'][i] + similarity_feat['gram_5'][i]) / 5
            similarity.append(mean)
        
        sorted_val = np.argsort(similarity)[-5:]
        for el in sorted_val:
            recommendations.append(self.features[subject][chapter][el][1])
        
        return recommendations

    def recommend(self):
        while True:
            in_str = input("Put Id: ")
            try:
                recommendations = self.get_recommendations(in_str)
                for el in recommendations:
                    print(f'Class {el["class"]}')
                    print(f'Chapter {el["chapter"]}')
                    print(f'{el["eng"]}')
                    print()
            except Exception as e:
                print(e)
                print('No ID Available')