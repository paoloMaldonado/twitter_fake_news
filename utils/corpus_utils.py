import nltk
from nltk.tokenize import word_tokenize
import spacy
import stanza

def tokenizer_punct(doc):
    tokenized = word_tokenize(doc, language="spanish")
    words = [word.lower() for word in tokenized if word.isalpha()]
    return words

def remove_stopwords(tokens, lst_stopwords):
    if lst_stopwords is not None:
        lst_text = [word for word in tokens if word not in lst_stopwords]
    return lst_text

def lemmatizer(tokens_sentence, nlp_model):
    text = ' '.join(tokens_sentence)
    lst_lemma = []
    doc = nlp_model(text)
    for sentence in doc.sentences:
        for word in sentence.words:
            lst_lemma.append(word.lemma)
    return lst_lemma

def join_tokens_into_sentence(tokens):
    sentence = ' '.join(tokens)
    return sentence

def preprocess_data(document, stopwords_list, nlp_model=None, opt_lemmatization=False):
    # tokenization
    h1 = tokenizer_punct(document)
    # remove stopwords
    h2 = remove_stopwords(h1, stopwords_list)
    # lemmatization (optional)
    if opt_lemmatization == True and nlp_model != None:
        h3 = lemmatizer(h2, nlp_model)
        return h3
    # join the tokens into one sentece
    return h2