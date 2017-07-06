# -*- coding: utf-8 -*-
"""
Author: Phillip Martin (phillipmar50@gmail.com)

Description: Given dictionary matching foals' AIDs to their mothers' AIDs, calculates
mean reciprocal rank of mothers' similarities to their foals, creates histrogram of
reciprocal ranks of mothers.

To Use:
1. Change bmD dictionary to include all foal-mother pairs in format described below.
2. Run file.

Issues:
1. Readability (variable names, descriptions of dictionaries and lists, etc.)
2. Default mRank is 0 right now, could cause problems when calculating reciprocal ranks

"""

import collections
import matplotlib.pyplot as plt
import GetPropertiesAPI as GP
import importlib
importlib.reload(GP)

# Dictionary of occurences of a foal matched with occurences of its mother: dictionary of {indices: [list of [foal AIDs], list of [mother AIDs]]}
bmD = {1: [[899, 125, 900, 127, 128, 129, 130], [131, 132]], 2: [[134, 135, 136], [137, 138, 139]], 3: [[140, 141, 143], [145, 146, 147, 148, 149, 150]]}

# Create list of all mother AIDs
momL = []
for i in bmD:
    for mAid in bmD[i][1]:
        momL.append(mAid)

# Rank all mothers for each foal AID: dictionary of {foal AIDs: dictionary of {sorted similarity scores: mother AIDs}}
rankD = {}
for i in bmD:
    for bAid in bmD[i][0]:
        resp = GP.simScore(bAid, momL)
        mAidL = resp['response'][0]['daid_list']
        scoreL = resp['response'][0]['score_list']
        scoreD = {}
        for j in range(len(mAidL)):
            scoreD[scoreL[j]] = mAidL[j] # dictionary of {similarity score: mother AID} for each foal
        rank = collections.OrderedDict(sorted(scoreD.items(), reverse=True)) # sort each scoreD
        rankD[bAid] = rank

# Create list of each mother's rank for her foal
# Just a list, items no longer specific to foal or mother AIDs
rankL = []
for b in rankD:
    for i in bmD:
        if b in bmD[i][0]:
            momL = bmD[i][1]
    mRank = 0
    for m in rankD[b]:
        if rankD[b][m] in momL and mRank == 0:
            mRank = list(rankD[b].keys()).index(m)
    rankL.append(mRank)

# Create list of reciprocal ranks
recipRankL = []
for r in rankL:
    recipRankL.append(1/r)

# Calculate mean reciprocal rank
total = 0
for i in recipRankL:
    total+=i
MRR = total/len(recipRankL)
 
# Create histogram
lst = recipRankL
fig = plt.figure()
fig.suptitle('Reciprocal Rank Distribution', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.85)
ax.set_xlabel('Reciprocal Rank')
ax.set_ylabel('Number of Occurences')
plt.hist(lst)
plt.margins(0.05)
plt.show()