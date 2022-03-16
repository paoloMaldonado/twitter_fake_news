import re
import pandas as pd 
import preprocessor as p

def find_hashtags(tweet):
    return re.findall('(#[A-Za-z]+[A-Za-z0-9-_À-ÿ]+)', tweet)

def hash_fix(h):
    h1 = re.sub(r'[0-9]+', '', h)
    h2 = re.sub(r'#', '', h1)
    if(h2.isupper()):
        h3 = h2.split()
    else:
        h3 = re.sub(r'([A-Z])', r' \1', h2).split()
    h4 = ' '.join(map(str, h3))
    return h4

def hash_dict(df, hash_col):
    tag_counts = df[hash_col].apply(pd.Series).stack().value_counts().to_frame()
    tag_counts = tag_counts.reset_index()
    tag_counts.columns = ['hash','freq']
    tag_counts = tag_counts.assign(clean_tag = tag_counts.hash.apply(lambda x: hash_fix(x)))
    tag_counts.set_index('hash', inplace=True)
    tag_dict = tag_counts['clean_tag'].to_dict()
    return tag_dict

def clean_tweets(df, column_hashtags):
    # Crear diccionario de hashtags
    tag_dict = hash_dict(df,column_hashtags)
    # Crear una columna con los tweets preprocesados
    df = df.assign(clean_tw = df.Content.apply(lambda x: p.clean(str(x))))
    # Reemplazar los hashtags
    df = df.assign(clean_tw = df.clean_tw.replace(tag_dict, regex=True))
    return df