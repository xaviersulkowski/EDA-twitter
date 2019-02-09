# Extensive Data Analysis
Repo is part of recruitment process to Lekta AI. It's also my first contact with NLP related topics.

## Task description 
Purpose of the task is to perform an Extensive Data Analysis of text data from Health News in Twitter Data Set, 
focusing on finding the topics of tweets.

Data set comes from [here](https://archive.ics.uci.edu/ml/datasets/Health+News+in+Twitter).

## Repo content
##### data directory 
Contains raw data in txt .format and  tweets.pkl file which is nothing else than parsed files and saved in python pickle format.
##### notebook 
Jupyter notebook it's a great tool to connect report text form with 'real time' running code so I used it to prepare task solution. 
Just look inside to check my way of thinking.   
  
  
\
\
Repo also contains script version with generated pdf report on other branch. 

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