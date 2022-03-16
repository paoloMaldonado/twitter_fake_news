import pandas as pd 
import preprocessor as p
import spacy
import stanza
from tqdm import tqdm
from utils.twitter_utils import clean_tweets, find_hashtags
from utils.corpus_utils import preprocess_data


def preprocess_tweet(path, content_column ,stopwords, nlp_model=None, opt_lemmatization=False):
    # read file
    df_original = pd.read_excel(path, index_col=0, sheet_name="Tweets")
    
    # copy only the neccesary columns for preprocessing
    selected_columns = df_original[[content_column]]
    df = selected_columns.copy()
    
    # remove nulls
    if df[content_column].isnull().sum() > 0:
        df = df.dropna()
        df.reset_index(drop=True, inplace=True)
    
    # remove blanks ('')
    indices = []
    for i, doc in enumerate(df[content_column]):
        if len(doc) == 0:
            indices.append(i)
    df = df.drop(indices)
    df.reset_index(drop=True, inplace=True)
    
    df = df.assign(hashtags = df.Content.apply(lambda x : find_hashtags(x)))
    
    # remove urls, mentions and emojis
    p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.SMILEY)
    tw_data = clean_tweets(df, "hashtags")
    
    tqdm.pandas()
    tw_data = tw_data.assign(clean_data = tw_data.clean_tw.progress_apply(lambda x : preprocess_data(x, stopwords, nlp_model, opt_lemmatization)))
    
    return tw_data