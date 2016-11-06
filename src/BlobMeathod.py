# -*- coding: utf-8 -*-
import math
from textblob import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

document1=tb(""" Welcome to Front-End JavaScript Frameworks: AngularJS course. This course is the third in the series of courses that form part of the Full-Stack Web Development Specialization. This course will give you an overview of client-side JavaScript frameworks, in particular AngularJS. You will learn about AngularJS, the model-view-controller framework, Angular directives, filters, and controllers. You will design a single page application using AngularJS. You will learn about client-server communication between your Angular application and a RESTful server. You will also learn about Web tools like Grunt, Gulp and Yo, and Yeoman workflow.At the end of this course, you will be able to:Set up, design and style a single page application using AngularJSEnable client-server communication between your Angular application and a RESTful serverMake use of web tools to setup and manage your Angular application.This course includes four modules, each corresponding to one calendar week of work. A module is structured into a set of lessons. In each lesson, there'll be a set of lecture videos, together with an exercise and a practice quiz to help you make sure you've mastered the material. At the end of each module an assignment in which you'll get to employ the skills you learnt in the module needs to be completed and submitted as per the given instructions. When you complete the course, you'll come away with an in-depth knowledge of front-end JavaScript development using AngularJS and make use of some Web development tools. If you have friends who might be interested in full-stack web development, please let them know about the class, and get them to sign up too (maybe forward this email to them). If you and your friends form a �study group� and work together to learn about full-stack web development, that would likely make the experience more fun, and help you learn more quickly too.Welcome once again to the Front-End JavaScript Frameworks: AngularJS course, and I hope you will gain a lot of knowledge and skills through the course.""")
bloblist = [document1]
for i, blob in enumerate(bloblist):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))