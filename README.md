# Extensive Data Analysis
Repo is part of recruitment process to Lekta AI. It's also my first contact with NLP related topics.

## Task description 
Purpose of the task is to perform an Extensive Data Analysis of text data from Health News in Twitter Data Set, 
focusing on finding the topics of tweets.

Data set comes from [here](https://archive.ics.uci.edu/ml/datasets/Health+News+in+Twitter).

## Repo content
##### data directory 
Contains raw data in txt .format and  tweets.pkl file which is nothing else than parsed files and saved in python pickle format.
##### report directory 
PDF file for recruiters as task solution. 
##### scripts 
CONFIG.py file with basic configuration, there for eg. you can add additional stopwords for text analysis, it also here, 
too, download the necessary files for nltk lib. 

parseTweets.py with function which parsing tweets and save to pickle file. 

basicStats.py contains some functions to calculate simple statistic needed to report. 

sentimentAnalysis.py contains one function to sentiment analysis ;) 

trendTopics contains functions to plot wordclouds and topics popularity changes in time there is also function to create LDA/TFIDF model. 

In main.py I run functions from trendTopics and sentimentAnalysis. 

tools.py contains some needed functions.

## Features plans 
It's case which seems to be ideal for Jupyter Notebook project as step-by-step instruction how to handle problems 
like this... and it will appears... for sure. 


## Prepare environment
Prepared on Linux Ubuntu 18.04LTS with Python3.6.7.

Update system
```bash
sudo apt-get update
sudo apt-get upgrade
```

Prepare Python virtualenv
```bash
sudo apt-get install python3.6
sudo pip3 install virtualenv

(it's my favorite way to manage python's virtualenvs, it's not obligatory or something)
mkdir ~/venvs
cd ~/venvs/

virtualenv aads -p $(which python3)
```

Clone repo with https

```bash
cd directory
git clone https://github.com/paniks/EDA-twitter.git
```

Activate virtualenv and install requirements
```bash
(in project dir)

source path/to/venv/bin/activate
pip install -r requiments.txt
```

Run what you need.