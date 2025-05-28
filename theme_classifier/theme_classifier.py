


from nltk import sent_tokenize
import torch
import pandas as pd
import numpy as np
from transformers import pipeline
from utils import load_subtitle
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')

class ThemeClassifier():
    def __init__(self,theme_lists):
        self.model_name =  "facebook/bart-large-mnli"
        self.device =  0 if torch.cuda.is_available() else "cpu"
        self.theme_lists = theme_lists
        self.theme_classifier = self.load_model(self.device,self.model_name)

    def load_model(self,device,model_name):
        theme_classifier = pipeline(
            "zero-shot-classification",
            model= model_name,
            device = device
        )

        return theme_classifier
    
    def get_themes_inference(self,script):
        script_sentences = sent_tokenize(script)
        sentence_batch_size = 20
        script_batches = []
        for index in range(0,len(script_sentences),sentence_batch_size):
            sent = " ".join(script_sentences[index:sentence_batch_size + index])

            script_batches.append(sent)
        theme_output = self.theme_classifier(
        script_batches[:2],
        self.theme_lists,
        multi_label =  True
        )

        themes ={}

        for output in theme_output:
            for label,score in zip(output["labels"],output["scores"]):
                if label not in themes:
                    themes[label] = []

                themes[label].append(score)
        themes = {key : np.mean(np.array(value)) for key,value in themes.items()}

        return themes
    
    def get_themes(self,dataset_path,save_path = None):

        df = load_subtitle(dataset_path)
        output_themes = df['script'].apply(self.get_themes_inference)
        theme_df = pd.DataFrame(output_themes.tolist())
        df[theme_df.columns] = theme_df
        if save_path is not None:
            df.to_csv(save_path,index = False)