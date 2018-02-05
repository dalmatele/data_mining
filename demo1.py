#!/usr/bin/python

import codecs
from math import sqrt

users = {
        "Angelica": {
            "Blues Traveler": 3.5,
            "Broken Bells": 2.0,
            "Norah Jones": 4.5,
            "Phoenix": 5.0,
            "Slightly Stoopid": 1.5,
            "The Strokes": 2.5,
            "Vampire Weekend": 2.0
        },
        "Bill": {
            "Blues Traveler": 2.0,
            "Broken Bells": 3.5,
            "Norah Jones": 4.0,
            "Phoenix": 2.0,
            "Slightly Stoopid": 3.5,
            "Vampire Weekend": 3.0,
            "DeadMau5": 4.0
        },
        "Chan": {
            "Blues Traveler": 5.0,
            "Broken Bells": 1.0,
            "Norah Jones": 4.5,
            "Phoenix": 5.0,
            "Slightly Stoopid": 1.5,
            "DeadMau5": 1.0
        },
        "Dan": {
            "Blues Traveler": 3.0,
            "Broken Bells": 4.0,
            "Phoenix": 3.0,
            "Slightly Stoopid": 4.5,
            "The Strokes": 4.0,
            "DeadMau5": 4.5,
            "Vampire Weekend": 2.0
        }
    }
class recommender:
    """
    @param k k nearest neighbor
    @param metric distance formula to use
    @param n maximum number of recommendations to make
    """
    def __init__(self, data, k = 1, metric = 'pearson', n = 5):
        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.productionid2name = {}
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson
        if type(data).__name__ == 'dict':
            self.data = data


    def convertProductID2name(self, id):
        if id in self.productionid2name:
            return self.productionid2name[id]
        else:
            return id
    def userRatings(self, id, n):
        print ("Ratings for " + self.userid2name[id])
        ratings = self.data[id]
        print(len(ratings))
        ratings = list(ratings.items())
        ratings = [(self.convertProductID2name(k), v) for (k, v) in ratings]
        ratings.sort(key = lambda artistTuple: artistTuple[1], reverse = True)
        ratings = ratings[:n]
        for rating in ratings:
            print("%s\t%i" % (rating[0], rating[1]))

    def loadBookDB(self, path = ''):
        self.data = {}
        i = 0
        f = codecs.open(path + "BX-Book-Ratings.csv", "r", "utf8")
        for line in f:
            i += 1
            fields = line.split(";")
            user = fields[0].strip('"')
            book = fields[1].strip('"')
            rating = int(fields[2].strip().strip('"'))
            if user in self.data:
                currentRatings = self.data[user]
            else:
                currentRatings = {}
            currentRatings[book] = rating
            self.data[user] = currentRatings
        f.close()
        f = codecs.open(path + "BX-Books.csv", "r", "urf8")
        for line in f:
            i += 1
            fields = line.split(';')
            isbn = fields[0].strip('"')
            title = fields[1].strip('"')
            author = fields[2].strip().strip('"')
            title = title + " by" + author
            self.productionid2name[isbn] = title
        f.close()
        f = codes.open(path + "BX-Users.csv", "r", "utf8")
        for line in f:
            i += 1
            fields = line.split(';')
            userid = fields[0].strip('"')
            location = fields[1].strip('"')
            if len(fields) > 3:
                age = fields[2].strip().strip('"')
            else:
                age = "NULL"
            if age != "NULL":
                value = location + " (age: " + age + ")"
            else:
                value = location
            self.userid2name[userid] = value
            self.username2id[location] = userid
        f.close()
        print(i)

    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            for key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        denominator = (sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n))
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator
    def computeNearestNeighbor(self, username):
        distances = []
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username], self.data[instance])
                distance.append((instance, distance))
        distances.sort(key=lambda artistTuple: artistTuple[1], reverse = True)
        return distances
