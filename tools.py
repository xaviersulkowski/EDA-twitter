import re
import pandas as pd
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from CONFIG import *

__wnl = WordNetLemmatizer()


def lowercase(text: str) -> str: return text.lower()


def remove_punctuation(text: str) -> str: return re.sub('[%s]' % re.escape(PUNCTUATION), '', text)


def remove_numberwords(text: str) -> str: return re.sub(r'\w*\d\w*', '', text)


def remove_stopwords(text: str) -> str: return " ".join(x for x in text.split() if x not in STOP)


def remove_tags(text: str) -> str: return re.sub(r'#\w*', '', text)


def remove_mentions(text: str) -> str: return re.sub(r'@\w*', '', text)


def remove_url(text: str) -> str: return re.sub(r'https?\w*?\S*?', '', text)


def remove_amp(text: str) -> str: return re.sub(r'\w*?\S*?amp\w*?\S*?', '', text)


def remove_multispaces(text: str) -> str: return re.sub(r' +', ' ', text)


def polarity(text: str): return TextBlob(text).sentiment.polarity


def subjectivity(text: str): return TextBlob(text).sentiment.subjectivity


def if_noun_adj(tag: str) -> bool: return tag[:2] == 'NN' or tag[:2] == 'JJ'


def flatten_list(l: list) -> list: return [item for sublist in l for item in sublist]


def hard_clean(text: str):
    text = lowercase(text)
    text = remove_stopwords(text)
    text = remove_punctuation(text)
    text = remove_numberwords(text)
    text = remove_tags(text)
    text = remove_mentions(text)
    text = remove_url(text)
    text = remove_amp(text)
    text = remove_multispaces(text)
    return text


def leave_nouns_adj(text: str) -> str:
    tokenized = word_tokenize(text)
    nouns_adj = [word for (word, pos) in pos_tag(tokenized) if if_noun_adj(pos)]
    return ' '.join(nouns_adj)


def lemmatize(text: str) -> str:
    return " ".join(
        __wnl.lemmatize(word, tag[0].lower()) if tag[0].lower() in ['a', 'n', 'v']
        else __wnl.lemmatize(word)
        for word, tag in pos_tag(word_tokenize(text)))


def return_corpus(database: pd.DataFrame, sorted_by: str) -> pd.DataFrame:
    df = pd.DataFrame(data={sorted_by: database[sorted_by], 'tweet': database.content})
    data_combined = {key: list(df.tweet[df[sorted_by] == key]) for key in df[sorted_by].unique()}
    for key, value in data_combined.items():
        data_combined[key] = [" ".join(value)]

    corpus_df = pd.DataFrame.from_dict(data_combined).transpose()
    corpus_df.columns = ['tweets']
    corpus_df = corpus_df.sort_index()

    return corpus_df
