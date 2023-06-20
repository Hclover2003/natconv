import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as plt
import statsmodels.formula.api as smf 
import os
import re

# Set data directory
data_dir = "/Users/huayinluo/Downloads/candor(1)"
subdirs = [x[0] for x in os.walk(data_dir)]

all_transcripts=pd.DataFrame(columns=['conversation', 'turn_id', 'speaker', 'backchannel_given', 'backchannel_recieved', 'delta', 'n_words', 'backchannel_count'])

i=0
for folder in subdirs:
    if folder.endswith("transcription"):
        conv_id = folder.split("/")[-2] # Get conversation id   
        file = os.path.join(folder, "transcript_backbiter.csv")
        conv_transcript=pd.read_csv(file)
        conv_transcript["conversation"] = conv_id
        all_transcripts = pd.concat([all_transcripts, conv_transcript])
        i+=1
        print(f'finished {i} conversations')
all_transcripts.to_csv("/Users/huayinluo/Downloads/all_transcripts.csv")