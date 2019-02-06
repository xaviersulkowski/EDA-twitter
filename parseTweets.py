import pandas as pd
import os
import re
import codecs


# every other line (e.g comments) will be ignored
REGEX = r'\d+\|[A-Z][a-z]{2}\s[A-Z][a-z]{2}\s\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\s\+\d+\s20\d{1,2}\|(?<=\|).*'

agencyDict = {
    'reuters_health': 'Reuters',
    'msnhealthnews': 'MSN',
    'NBChealth': 'NBC',
    'wsjhealth': 'WSJ',
    'bbchealth': 'BBC',
    'KaiserHealthNews': 'Kaiser',
    'nprhealth': 'NPR',
    'usnewshealth': 'USnews',
    'everydayhealth': 'EH',
    'cbchealth': 'CBC',
    'cnnhealth': 'CNN',
    'foxnewshealth': 'FoxNews',
    'nytimeshealth': 'NYtimes',
    'gdnhealthcare': 'GDN',
    'latimeshealth': 'LAtimes',
    'goodhealth': 'GoodHealth'
}

monthDict = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12',
}

dataDict = {'ids': [], 'day': [], 'month': [], 'year': [], 'hour': [], 'url': [], 'content': [], 'agency': []}


def findfiles(rootdir, ext):
    return [os.path.join(rootdir, file) for file in os.listdir(rootdir) if file.endswith(ext)]


def parse_txt(filenames: list, out_path: str):
    database = pd.DataFrame.from_dict(dataDict)
    for file in filenames:
        print(file)
        with codecs.open(file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            lines = list(map(lambda x: re.findall(REGEX, x, flags=re.MULTILINE), lines))
            lines = list(filter(None, lines))
            lines = list(map(lambda x: x[0], lines))
            lines = list(map(lambda x: x.strip().split('|', 2), lines))

            dataDict['ids'] = list(map(lambda x: x[0], lines))
            dataDict['month'] = list(map(lambda x: monthDict[x[1][4:7]], lines))
            dataDict['day'] = list(map(lambda x: x[1][0:3], lines))
            dataDict['hour'] = list(map(lambda x: re.findall(r'(\d{1,2}:\d{1,2}:\d{1,2})', x[1], flags=re.MULTILINE)[0], lines))
            dataDict['year'] = list(map(lambda x: re.findall(r'20\d{1,2}', x[1], flags=re.MULTILINE)[0], lines))
            dataDict['url'] = list(map(lambda x: re.findall(r'https?\S+', x[2], flags=re.MULTILINE), lines))
            dataDict['content'] = list(map(lambda x: x[2], lines))
            dataDict['agency'] = [agencyDict[file.split('/')[-1][:-4]]] * len(lines)

            df = pd.DataFrame.from_dict(dataDict)
            database = pd.concat((database, df), ignore_index=True)

            f.close()

    database.to_pickle(out_path)


if __name__ == "__main__":
    basename = './data/Health-Tweets/'
    filenames = findfiles(basename, '.txt')
    parse_txt(filenames, './data/database.pkl')
