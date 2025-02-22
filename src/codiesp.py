import os

import pandas as pd
from nltk import sent_tokenize as splitter
from tqdm import tqdm

from .utils import (
    autoconfigure,
    from_txt
)


PROJECT_HOME = autoconfigure()

print(PROJECT_HOME)

PATH_CODIESP = os.path.join(PROJECT_HOME, "data", "final_dataset_v2_to_publish")
PATH_CODIESP_TRAIN = os.path.join(PATH_CODIESP, "train")
PATH_CODIESP_TRAIN_FILES = os.path.join(PATH_CODIESP_TRAIN, "text_files_en")

sentence_rows = []
for idx, txt_file in enumerate(tqdm(os.listdir(PATH_CODIESP_TRAIN_FILES))):
    for sent in splitter(from_txt(os.path.join(PATH_CODIESP_TRAIN_FILES, txt_file))):
        sentence_rows.append((txt_file, idx, sent))

CODIESP_SCHEMA = ["text_path", "text_id", "sentence"]
CODIESP = pd.DataFrame(sentence_rows, columns=CODIESP_SCHEMA)
