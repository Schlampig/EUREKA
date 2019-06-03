# EUREKA

## Source:
  * **original authors**: [Xylander23](https://github.com/xylander23/New-Word-Detection) is the original author, and then [Lyrichu](https://github.com/Lyrichu/NewWordDetection) modified the code to python3 version. <br>
  * **references**: [Code for Chinese Word Segmentation](https://github.com/Moonshile/ChineseWordSegmentation), [Blog about New Words Detection](http://www.matrix67.com/blog/archives/5044), [中文分词新词发现](https://github.com/zhanzecheng/Chinese_segment_augment). <br>
  * **old version**: an immature version of mine could be find [here](https://github.com/Schlampig/i_learn_deep/tree/master/NewWordDetection). <br>
 
<br>

## Data:
  * **stop-words dictionary**: a stop-words dictionary file could leverage the final performance of EUREKA, an example could be seen [here](https://github.com/Schlampig/EUREKA/blob/master/stop_words.txt) (this dictionary is copied from the [Lyrichu](https://github.com/Lyrichu/NewWordDetection)). <br>
  * **input corpus**: the input corpus is a long string, such as a novel text, or a concatenated documentation pieces. See an [example](https://github.com/Schlampig/EUREKA/blob/master/document.txt). <br>
  * **corpus in mongodb**: you can store each document as one sample in a collection of a mongodb database, with the format like this:
```
{"_id": ObjectId("123456789"), "content": your_corpus(long string)}
```

<br>

## Codes Dependency:
```
eureka -> model   
```

<br>

## Using Example:
```
from eureka import Eureka
model = Eureka()
model.load_dictionary()

# data from .txt file
####################################################################
import codecs
corpus = codecs.open("document.txt", "r", "utf-8").read()

n = len(corpus)
if n < 5000:
    print("The corpus is too small.")
elif n < 250000:
    res = model.discover_corpus(corpus)
else:
    res = model.discover_corpus_multi(corpus, corpus_size=200000, re_list=True)  # corpus_size is the length of sub-corpus in from the input corpus

# data from mongo
####################################################################
import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
col = client["your_database_name"]["your_collection_name"]
res = model.discover_corpus_mongo(col, n=20000, corpus_size=200000, re_list=True)  # n is the number of samples used in collections
```

<br>

## Requirements
  * Python>=3.5
  * pandas>=0.22.0
  * pkuseg
  * jieba>=0.39
  * tqdm>=4.19.5
  * Flask(optional, if runing the server.py)
  * pymongo(optional, EUREKA could handle mongo data but it essentially does not need this lib)
  * ipdb(optinoal, if debugging in command line)
  
<br>

## TODO
- [x] Naive spliting strategy for very large corpus.
- [x] Handle corpus stored in mongo.
- [ ] Add crawling strategy to automatically filter and find further infomation of the detected strings.
- [ ] Using more effective and efficient model.

<br>

## Allusion
  * *[Eureka](https://en.wiktionary.org/wiki/eureka)* is from Ancient Greek word *heúrēka*, which means *I have found*.
  * *[Eureka](https://www.bones.co.jp/eureka-seven)* is also a heroine from a Japanese anime called *Eureka Seven*.




