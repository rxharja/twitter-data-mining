stopwords_kr_th = []
englishWords = []
with open('/Users/redonxharja/Documents/Projects/python/sentimentMiner/stopwords-th.txt','r', encoding="utf8") as f:
    for line in f:
        line = line.split('\n')
        stopwords_kr_th.append(line[0])

with open('/Users/redonxharja/Documents/Projects/python/sentimentMiner/stopwords-ko.txt','r', encoding="utf8") as g:
    for line in g:
        line = line.split('\n')
        stopwords_kr_th.append(line[0])
      
with open('/Users/redonxharja/Documents/Projects/python/sentimentMiner/englishWords.txt','r') as h:
    for line in h:
        line = line.split('\n')
        englishWords.append(line[0])
