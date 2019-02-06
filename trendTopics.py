import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

import tools


def find_trending_topics(document_term_matrix: pd.DataFrame, n_topics: int) -> dict:
    trending_topics = {year: document_term_matrix.loc[year].nlargest(n_topics) for year in document_term_matrix.index}
    return trending_topics


def generate_single_wordcloud(document_term_matrix: pd.DataFrame, n_topics: int) -> dict:
    trending_topics = pd.DataFrame(document_term_matrix.nlargest(n_topics)).to_dict()[0]
    wordcloud = WordCloud(background_color='white', max_font_size=150, colormap='Dark2') \
        .generate_from_frequencies(trending_topics)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Most trending tweets")
    return wordcloud


def generate_multi_wordclouds(document_term_matrix: pd.DataFrame, n_topics: int) -> list:
    trending_topics = find_trending_topics(document_term_matrix, n_topics)
    ncol = 2
    nrow = int(np.ceil(len(document_term_matrix.index) / ncol))
    fig = plt.figure()
    wordclouds = []
    for cnt, year in enumerate(trending_topics.keys()):
        dict_ = trending_topics[year].to_dict()
        wordcloud = WordCloud(background_color='white', max_font_size=150, colormap='Dark2')\
            .generate_from_frequencies(dict_)
        ax = fig.add_subplot(nrow, ncol, cnt+1)
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        ax.set_title(f"Most trending tweets in {year}")
        wordclouds.append(wordcloud)
    return wordclouds


def plot_topics_trend_routine(database: pd.DataFrame, topics_list: list):

    topics = {key: [] for key in topics_list}

    df = pd.DataFrame(database.content.apply(tools.lowercase))
    df = pd.DataFrame(df.content.apply(tools.lemmatize))
    df['year'] = database.year
    df['month'] = database.month

    for topic in topics.keys():
        for year in sorted(database.year.unique()):
            for month in sorted(database.month.unique()):
                df_tmp = pd.DataFrame(df[(df.year == year) & (df.month == month)])
                n_tweets = len(df_tmp)
                n_tweets_with_key = df_tmp.content.str.contains(topic).sum()
                if n_tweets == 0:
                    topics[topic].append(0)
                else:
                    topics[topic].append((n_tweets_with_key / n_tweets) * 100)

    xticks = []
    for year in sorted(database.year.unique()):
        for month in sorted(database.month.unique()):
                if month == '01':
                    xticks.append(f'{month}.{year}')
                else:
                    xticks.append(f'{month}')

    plt.figure()
    plt.yticks(range(0, 91, 10), [str(x) + "%" for x in range(0, 91, 10)], fontsize=8)
    plt.xticks(range(0, 60, 1), xticks, fontsize=8, rotation=70)
    plt.ylim(-1, 60)
    for key, value in topics.items():
        plt.plot(topics[key], label=key)
    plt.grid()
    plt.xlabel('Months from 2011 to 2015')
    plt.ylabel('Tweets which contains keyword [%]')
    plt.title('Ratio of tweets with keyword to all Tweets', fontsize=15)
    plt.legend()

