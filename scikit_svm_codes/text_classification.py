# -*- coding: utf-8 -*-
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np

categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)

print("\n".join(twenty_train.data[0].split("\n")[:10]))

print "data", twenty_train.data[0]

for t in twenty_train.target[:10]:
    print(twenty_train.target_names[t])

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)
print X_train_counts.shape
print X_train_counts[0, 0:100]
# get index of some word
print count_vect.vocabulary_.get(u'good')
print count_vect.vocabulary_.keys()
print "'good' count in doc0:", X_train_counts[0, count_vect.vocabulary_.get(u'good')]
print "sum of doc0:", np.sum(X_train_counts[0, :].data)
# 用频率
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
print X_train_tf.shape
print "'good' frequency in doc0:", X_train_tf[0, count_vect.vocabulary_.get(u'good')]

# 训练一个分类器
from sklearn.naive_bayes import MultinomialNB

clf = MultinomialNB().fit(X_train_tf, twenty_train.target)

# 测试数据集合
docs_new = ['God is love', 'OpenGL on the GPU is fast']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, twenty_train.target_names[category]))

# pipeline
from sklearn.pipeline import Pipeline

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
                     ])

text_clf = text_clf.fit(twenty_train.data, twenty_train.target)

# 测试性能
twenty_test = fetch_20newsgroups(subset='test', categories=categories, shuffle=True, random_state=42)
docs_test = twenty_test.data
predicted = text_clf.predict(docs_test)
print predicted
print predicted == twenty_test.target
print np.mean(predicted == twenty_test.target)

from sklearn.linear_model import SGDClassifier

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-3, n_iter=5, random_state=42)),
                     ])
_ = text_clf.fit(twenty_train.data, twenty_train.target)
predicted = text_clf.predict(docs_test)
np.mean(predicted == twenty_test.target)

# 测试效果详情
from sklearn import metrics

print(metrics.classification_report(twenty_test.target, predicted,
                                    target_names=twenty_test.target_names))
print metrics.confusion_matrix(twenty_test.target, predicted)