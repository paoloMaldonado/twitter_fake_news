from preprocessing_tweets import preprocess_tweet
from utils.exporting_dataframe import export_to_excel
import nltk
import pandas as pd
import os

import time
from datetime import timedelta

def recursively_preprocess(path, directory_to_export, content_column, sheet, stopwords, nlp_model = None, opt_replies = False, opt_lemmatization = False):
    os.chdir(path)
    d = os.listdir()
    for item in d:
        if(os.path.isdir(item)):
            p = path+'/'+item
            recursively_preprocess(p, directory_to_export, content_column, sheet, stopwords, nlp_model, opt_replies, opt_lemmatization)
        else:
            # if the parent directory is Partidos Politicos
            if(path.split("/")[-1] == "Partidos Políticos"):
                # save the path
                full_path = path+"/"+item
                # print the path
                print(full_path)
                # pre process the data
                tw_data = preprocess_tweet(full_path, content_column, sheet, stopwords, nlp_model, opt_replies, opt_lemmatization)
                # export the clean data
                if not tw_data.empty:
                    export_to_excel(tw_data, directory_to_export, full_path, column='clean_data')
    os.chdir("../")
    return

if __name__ == "__main__":
    # download the tokenized model
    nltk.download('punkt')
    
    # load the stopwords file
    stopwords = []
    stop = pd.read_csv("../stopwords/stopwords_spanish.csv")
    for word in stop.stopword:
        stopwords.append(word)

    # load the stanza model for lemmatization
    # stanza.download('es') # download Spanish model
    # nlp_model = stanza.Pipeline(lang='es', processors='tokenize, mwt, pos, lemma', tokenize_pretokenized=True)

    path = "C:/Users/jorpa/Documents/ESAN/twitter_fakeNews/data"
    content_column = "texto"
    sheet_name = 'Respuestas'
    directory_to_export = "clean replies"

    # preprocess 
    #start_time = time.monotonic()
    print("Starting preprocessing")
    recursively_preprocess(path, directory_to_export, content_column, sheet_name, stopwords, opt_replies=True)
    #end_time = time.monotonic()

    #print(timedelta(seconds=end_time - start_time))
