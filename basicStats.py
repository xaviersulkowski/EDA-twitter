import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tools


def find_expressions(database: pd.DataFrame, expression: str, sorted_by: str, percentage: bool) -> dict:
    data = tools.return_corpus(database, sorted_by)
    ex_amount = {key: len(re.findall(r'%s' % expression, data.loc[key].tweets)) for key in data.index}
    if percentage is True:
        ex_per = {key: value/len(database[database[sorted_by] == key]) for key, value in ex_amount.items()}
        return ex_per
    else:
        return ex_amount


def popular_expressions(database: pd.DataFrame, expression: str) -> pd.Series:
    data = pd.DataFrame(database.content.apply(tools.lowercase))
    data = pd.DataFrame(data.content.apply(tools.remove_punctuation))
    data = pd.DataFrame(data.content.apply(tools.remove_stopwords))
    data = pd.DataFrame(data.content.apply(tools.remove_numberwords))
    tags = tools.flatten_list(list(map(lambda x: re.findall(r'%s' %expression, x), data.content.values)))
    freq = pd.Series(tags).value_counts()
    return freq


def soft_clean(text: str) -> str: return " ".join(x for x in text.split() if x != 'RT')


database = pd.read_pickle('./data/tweets.pkl')

"""RETWEET PERCENTAGE"""
amount = find_expressions(database, 'RT', 'agency', True)
plt.figure()
plt.bar(amount.keys(), amount.values())
plt.title('How often agency retweets', fontsize=15)
plt.xlabel('Agency name', fontsize=10)
plt.ylabel('Retweets in tweet', fontsize=10)
plt.grid()
plt.show()


"""URL PERCENTAGE"""
amount = find_expressions(database, 'https?', 'agency', True)
plt.figure()
plt.bar(amount.keys(), amount.values())
plt.title('URL distribution per agency', fontsize=15)
plt.xlabel('Agency name', fontsize=10)
plt.ylabel('URL distribution', fontsize=10)
plt.grid()
plt.show()

"""TAGS PERCENTAGE"""
amount = find_expressions(database, '#\S+', 'agency', True)
plt.figure()
plt.bar(amount.keys(), amount.values())
plt.title('How often agencies uses hashtags', fontsize=15)
plt.xlabel('Agency name', fontsize=10)
plt.ylabel('Hashtags per tweet', fontsize=10)
plt.grid()
plt.show()

"""MENTIONS PERCENTAGE"""
amount = find_expressions(database, '@\S+', 'agency', True)
plt.figure()
plt.bar(amount.keys(), amount.values())
plt.title('How often agencies mentions', fontsize=15)
plt.xlabel('Agency name', fontsize=10)
plt.ylabel('Mentions per tweet', fontsize=10)
plt.grid()
plt.show()

"""w/ w/o URL"""

urls_amount = sum(find_expressions(database, 'https?', 'agency', False).values())

fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
data = [urls_amount/len(database), (len(database) - urls_amount)/len(database)]
labels = [f'{data[0]*100:1.1f}% Tweets\nwith URLs', f'{data[1]*100:1.1f}% Tweets\nwithout URLs']
wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-180, shadow=True)
bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

ax.set_title('How often tweets includes URLs', fontsize=15)

"""POPULAR expressions"""
popular_tags = popular_expressions(database, '#\S+')
popular_mentions = popular_expressions(database, '@\S+')

print('POPULAR TAGS')
print(popular_tags.head(10))
print('POPULAR MENTIONS')
print(popular_mentions.head(10))

"""nChar per tweet"""
data_clean = pd.DataFrame(database.content.apply(soft_clean))
data_clean = pd.DataFrame(data_clean.content.apply(tools.remove_mentions))
data_clean = pd.DataFrame(data_clean.content.apply(tools.remove_amp))
data_clean['agency'] = database.agency

nChar = {agency: list(map(lambda x: len(x), data_clean.content[data_clean.agency == agency]))
         for agency in data_clean.agency.unique()}

labels, data = [*zip(*nChar.items())]
plt.figure()
plt.boxplot(data, showfliers=False)
plt.xticks(range(1, len(labels) + 1), labels)
plt.show()