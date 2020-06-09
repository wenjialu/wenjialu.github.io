'''
Authors: Luke Shrimpton, Sharon Goldwater, Ida Szubert
Date: 2014-11-01, 2017-11-05
Copyright: This work is licensed under a Creative Commons
Attribution-NonCommercial 4.0 International License
(http://creativecommons.org/licenses/by-nc/4.0/): You may re-use,
redistribute, or modify this work for non-commercial purposes provided
you retain attribution to any previous author(s).
'''
from __future__ import division;
from math import log;
#from pylab import mean;

#This version of the function substitutes counts directly into
#the equation for PMI, cancelling N.
def PMI(c_xy, c_x, c_y, N):
    # Computes PMI(x, y) where
    # c_xy is the number of times x co-occurs with y
    # c_x is the number of times x occurs.
    # c_y is the number of times y occurs.
    # N is the number of observations.
    return log(N*c_xy/(c_x*c_y), 2)

#Many of you did this version instead, which is less
#efficient computationally but probably easier to understand
def PMI2(c_xy, c_x, c_y, N):
    # Computes PMI(x, y) where
    # c_xy is the number of times x co-occurs with y
    # c_x is the number of times x occurs.
    # c_y is the number of times y occurs.
    # N is the number of observations.
    p_x = c_x/N
    p_y = c_y/N
    p_xy = c_xy/N
    return log(p_xy/(p_x*p_y), 2)


#Do a simple error check using value computed by hand
if(PMI(2,4,3,12) != 1): # these numbers are from our y,z example
    print("Warning: PMI is incorrectly defined")
else:
    print("PMI check passed")

# List of positive words:
pos_words = ["love","like","great"];
# List of negative words:
neg_words = ["hate","bad","terribl"];
# List of target words:
targets = ["@justinbieber","food", "politician","husband","wife","self","kid","child","son","daughter"];

# Collect all words of interest and store their term ids:
all_words = set(pos_words+neg_words+targets);
all_wids = set([word2wid[x] for x in all_words]);

# Define the data structures used to store the counts:
o_counts = {}; # Occurrence counts
co_counts = {}; # Co-occurrence counts

# Load the data:
fp = open("/afs/inf.ed.ac.uk/group/teaching/anlp/lab8/counts");
lines = fp.readlines();
N = float(lines[0]); # First line contains the number of observations.
for line in lines[1:]:
    line = line.strip().split("\t");
    wid0 = int(line[0]);
    if(wid0 in all_wids): # Only get/store counts for words we are interested in
        o_counts[wid0] = int(line[1]); # Store occurence counts
        co_counts[wid0] = dict([[int(y) for y in x.split(" ")] for x in line[2:]]); # Store co-occurence counts

print("positive words are: ", pos_words)
print("negative words are: ", neg_words)

for target in targets:
    targetid = word2wid[target]
    target_count = o_counts[targetid]; # Extract the count of the target word
    posPMIs = []
    negPMIs = []
    # compute PMI between target and each positive word, and
    # add it to the list of positive PMI values
    for pos in pos_words:
        pos_wid = word2wid[pos]; # Extract the word id for the positive word.
    pos_count = o_counts[pos_wid]; # Extract the occurrence counts for the positive word.
    if(pos_wid in co_counts[targetid]): # Check if the words actually co-occur
	    cc = co_counts[targetid][pos_wid]; # Extract the co-occurrence counts for the target and positive word pair.
	    posPMIs.append(PMI(cc,target_count,pos_count,N)); # Compute PMI and append to the list
    else:
	    pass; # No co-occurence, ignore the word. 
    # same for negative words
    for neg in neg_words:
        neg_wid = word2wid[neg]; # Extract the word id for the negative word.
    neg_count = o_counts[neg_wid]; # Extract the occurrence counts for the negative word.
    if(neg_wid in co_counts[targetid]): # Check if the words actually co-occur
	    cc = co_counts[targetid][neg_wid]; # Extract the co-occurrence counts for the target and negative word pair.
	    negPMIs.append(PMI(cc,target_count,neg_count,N)); # Compute PMI and append to the list
    else:
	    pass; # No co-occurence, ignore the word. 
#uncomment the following line when posPMIs and negPMIs are no longer empty.
    print(target, ": ", posPMIs, "(pos), ", negPMIs, "(neg)")\