
from glob import glob
import pandas as pd

def load_subtitle(dataset_path):
    subt_file_path = glob(dataset_path +"/*.ass")
    scripts =[]
    ep_nums = []

    for path in subt_file_path:
        with open(path,'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = lines[27:]
            
            lines =[",".join(line.split(',')[9:]) for line in lines]
        lines = [line.replace('\\N',"") for line in lines]
        script= " ".join(lines)
        scripts.append(script)

        ep_no = int(path.split("-")[-1].strip().split(".")[0])
        ep_nums.append(ep_no)
            
    df = pd.DataFrame.from_dict({"episodes":ep_nums,"script":scripts})
    return df