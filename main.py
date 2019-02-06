import gensim
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import tools
import trendTopics as tt
import sentimentAnalysis as sa
from CONFIG import STOP

"""read db"""
database = pd.read_pickle('./data/tweets.pkl')

"""clean up data"""
df = pd.DataFrame(database.content.apply(tools.hard_clean))
df = pd.DataFrame(df.content.apply(tools.lemmatize))
df = pd.DataFrame(df.content.apply(tools.leave_nouns_adj))
df = pd.DataFrame(df.content.apply(tools.remove_stopwords))
df['year'] = database.year
df['agency'] = database.agency
df['month'] = database.month

"""create dtm"""
corpus_year_data = tools.return_corpus(df, 'year')
cv = CountVectorizer(stop_words=STOP)
data_cv = cv.fit_transform(corpus_year_data.tweets)
data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
data_dtm.index = corpus_year_data.index

"""-------------------------TOPIC TRENDS----------------------------"""
"""Generate wordclouds"""
tt.generate_multi_wordclouds(data_dtm, 30)

dtm_sum = data_dtm.sum()
tt.generate_single_wordcloud(dtm_sum, 30)

"""Topic modeling with LDA"""
tokenized_data = df.content.apply(tools.word_tokenize)

# create bag of words model
dictionary = gensim.corpora.Dictionary(tokenized_data)
bow_corpus = [dictionary.doc2bow(doc) for doc in tokenized_data]
lda_model_bow = gensim.models.LdaMulticore(bow_corpus, num_topics=5, id2word=dictionary, passes=10)
lda_model_bow.save('./models/lda_bow.model')

for idx, topic in lda_model_bow.print_topics(-1):
    print('Topic: {} Words: {}'.format(idx, topic))

# create term frequency inverse document frequency lda model
tfidf = gensim.models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]
lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=4, id2word=dictionary, passes=10)
lda_model_tfidf.save('./models/lda_tfidf.model')

for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))


"""Topic trends time routine"""
tt.plot_topics_trend_routine(database, ['ebola', 'cancer', 'insurance', 'food', 'drug'])


"""------------------SENTIMENT ANALYSIS-----------------------------"""
sa.plot_tweet_sentiments(database, 'agency')