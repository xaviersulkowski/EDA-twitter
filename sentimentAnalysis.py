import pandas as pd
import matplotlib.pyplot as plt
import tools


def plot_tweet_sentiments(database, sorted_by):
    corpus_df = tools.return_corpus(database, sorted_by)
    corpus_df = pd.DataFrame(corpus_df.tweets.apply(tools.remove_mentions))
    corpus_df = pd.DataFrame(corpus_df.tweets.apply(tools.remove_tags))
    corpus_df = pd.DataFrame(corpus_df.tweets.apply(tools.remove_url))
    corpus_df['polarity'] = corpus_df['tweets'].apply(tools.polarity)
    corpus_df['subjectivity'] = corpus_df['tweets'].apply(tools.subjectivity)

    plt.figure()
    for index, agency in enumerate(corpus_df.index):
        x = corpus_df.polarity.loc[agency]
        y = corpus_df.subjectivity.loc[agency]
        plt.scatter(x, y, color='C0')
        if agency == 'NYtimes':
            plt.text(x + .001, y - .004, corpus_df.index[index], fontsize=12)
        else:
            plt.text(x - .001, y + .002, corpus_df.index[index], fontsize=12)

    plt.title('Sentiment Analysis', fontsize=20)
    plt.xlabel('<-- Negative -------- Positive -->', fontsize=15)
    plt.ylabel('<-- Facts -------- Opinions -->', fontsize=15)
    plt.grid()
    plt.show()
