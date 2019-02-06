import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('wordnet')

STOP = stopwords.words('english')
ADDITIONAL_STOPWORDS = ["‘", "’", 'health', 'rt', 'today', 'day', 'people', 'life', 'hospital', 'goodhealth', 'time', 'ways',
                        'disease', 'new', 'healthy', 'report', 'video', 'audio', 'year', 'medical', 'good', 'case',
                        'patient', 'doctor', 'expert', 'report', 'nh']
STOP.extend(ADDITIONAL_STOPWORDS)

PUNCTUATION = string.punctuation.replace('#', '').replace('@', '')