from preprocessing_tweets import preprocess_tweet
from utils.exporting_dataframe import export_to_excel
import nltk
import pandas as pd
import os

def recursively_preprocess(path, filename, content_column, stopwords, nlp_model = None, opt_lemmatization = None):
    os.chdir(path)
    d = os.listdir()
    for item in d:
        if(os.path.isdir(item)):
            p = path+'/'+item
            recursively_preprocess(p, filename, content_column, stopwords, nlp_model, opt_lemmatization)
        else:
            f = os.path.splitext(item)[0]
            if(f == filename):
                # save the path
                full_path = path+"/"+item
                # print the path
                print(full_path)
                # pre process the data
                tw_data = preprocess_tweet(full_path, content_column, stopwords, nlp_model, opt_lemmatization)
                # export the clean data
                export_to_excel(tw_data, full_path, column='clean_data')
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
    content_column = "Content"

    # preprocess 
    print("Staring preprocessing")
    recursively_preprocess(path, "AccionPopular", content_column, stopwords)