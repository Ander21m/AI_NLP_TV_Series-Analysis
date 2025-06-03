import spacy
from nltk import sent_tokenize
import os
import sys
import pathlib
from ast import literal_eval
folder_path = pathlib.Path().parent.resolve()
sys.path.append(os.path.join(folder_path,'../'))
from utils import load_subtitle
import pandas as pd
class NameEntityRecongnizer:
    def __init__(self):
        self.nlp_model = self.load_model()

    def load_model(self):
        nlp = spacy.load('en_core_web_trf')
        return nlp
    
    def get_inference(self,script):
        script_sentences = sent_tokenize(script)

        output = []

        for sentence in script_sentences:
            doc = self.nlp_model(sentence)
            ners = set()
            for entity in doc.ents:
                
                if entity.label_ == "PERSON":
                    
                    fullname =entity.text
                    first_name = fullname.split(" ")[0]
                    first_name = first_name.strip()
                    ners.add(first_name)           
                    
            output.append(ners)

        return output
    
    def get_ners(self,dataset_path,save_path = None):
        
        if save_path is not None and os.path.exists(save_path):
            df = pd.read_csv(save_path)
            df['ners'] = df['ners'].apply(lambda x: literal_eval(x) if isinstance(x,str) else x)
            return df

        df = load_subtitle(dataset_path)
        
        df['ners'] = df['script'].apply(self.get_inference)

        if save_path is not None:
            df.to_csv(save_path,index = False)

        return df