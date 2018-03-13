import re
import json
import string
import stopwords_list #file created to access stop words found in korean and thai, most commonly found language besides english in the data set
import vincent
import pandas
from collections import Counter
from collections import defaultdict
from nltk.corpus import stopwords
from nltk import bigrams


com = defaultdict(lambda : defaultdict(int))
com_max = []
punctuation = list(string.punctuation)

fname = '/Users/redonxharja/Documents/Projects/python/sentimentMiner/data/stream_metoo.json'

#create regular expressions to sort most commonly found occurrences in tweets
emoticons = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex = [
    emoticons,
    r'<[^>]+>',  # HTML
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hashtags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with apostrophes and dashes
    r'(?:[\w_]+)',  # rest of the words
    r'(?:\S)'  # misc
]

tokens_re = re.compile(r'(' + '|'.join(regex) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons + '$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def chart_maker(x, title): #abstract process of creating the charts to fit with multiple data forms
    data_set = x.most_common(20)
    labels, freq = zip(*data_set)
    data = {'data':freq, 'x':labels}
    bar = vincent.Bar(data, iter_idx="x")
    ax = vincent.AxisProperties(
        labels=vincent.PropertySet(angle=vincent.ValueRef(value=45)))
    bar.axes[0].properties = ax
    path = title + '.json'
    bar.to_json(path)


with open(fname, 'r') as f:
    count_terms = Counter()
    Counter2 = count_terms.__class__
    count_langs = Counter2() #create new instance of Counter to use in the same for loop
    created_metoo = [] #initialize array to store times tweets were created

    for line in f:
        tweet = json.loads(line) #load each json line as a separate tweet
        stop = stopwords.words('english') + stopwords_list.stopwords_kr_th + punctuation + ['rt', 'via', 'RT', '…', 'I', '“'] #creating list of stop terms
        filtered_terms = [term for term in preprocess(tweet['text']) if term in stopwords_list.englishWords and term not in stop and not term.startswith(('#', '@'))] #filtering out stop terms, hashtags, and @ mentions
        bigram_terms = bigrams(filtered_terms) #Create bigrams from terms to increase context
        count_terms.update(bigram_terms) #update our counter to enumerate our most common bigrams
        total_langs = [tweet['user']['lang']] #each needs to be in its own array so the letters in 'en' are not split into e and n.
        count_langs.update(total_langs)
        created_metoo.append(tweet['created_at']) #stores time data for each tweet to measure interest over the course of the five hours data was collected

    chart_maker(count_langs, 'lang_freq') #generates json file for a vega scaffold based on top 20 languages tweeted in data set
    chart_maker(count_terms, 'term_freq') #generates json file for a vega scaffold based on top 20 bigrams in data set

    idx = pandas.DatetimeIndex(created_metoo)
    ones = [1]*len(created_metoo) #array of ones 1s to enumerate the number of data points
    series = pandas.Series(ones, index=idx)
    one_min = series.resample('1Min').sum()
    time_chart = vincent.Line(one_min)
    time_chart.axis_titles(x="time",y="frequency")
    time_chart.to_json('time_chart.json')

f.close()

