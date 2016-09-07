#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Read data in a data structure.

							--->start_time
							--->end_time
							--->objectives
organization---> project
							--->papers       --->description
										   
1. From project.csv we can get start_time, end_time, objectives of projects.
2. From publication.csv we can get publications of projects.
3. From contractor.csv we can get which organization correspongding to which project.

Find out the valid project. And the dat structure of the valid projects are:

                              ---> similarity of papers
                organization: ---> number of papers
valid_proj --->
                organization: ---> number of papers
                              ---> similarity of papers

@Author: Zhewei


"""

from __future__ import division
import csv
from collections import defaultdict

import os
import gzip
import codecs
import numpy
import cPickle as Pickle
from unidecode import unidecode
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import cosine
from sklearn.metrics import euclidean_distances
from pyemd import emd

class _project:

	def __init__(self, name, starttime, endtime, obj):
	    self.id = name
	    self.start_date = starttime
	    self.end_date = endtime
	    self.objectives = obj
	    self.papers = dict()
	    self.organization = list()
	    
class _org_of_proj:
    def __init__(self, paper_number):
        self.paper_number = paper_number
        self.similarity = list()

        
def cleanData():
	print "Reading raw data..."
	# from project.csv we can get information of end_time
	wholeData = list()
	with open('data/project.csv','rb') as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
        	wholeData.append(row)
        	
	# now each row is a dictionary.
	"""
	Keep a dictionary for project.
	
	"""
	project = dict()
	for items in wholeData:
		if items['status'] == "Completed":
		    # some times the end_date is miss
			if items['end_date']:
				# then now we consider it as a valid sample
				start_date = transferYMD(items['start_date'])
				end_date = transferYMD(items['end_date'])
				project[items['rcn']] = _project(items['rcn'], start_date, \
				                                    end_date, items['objectives'])
				pass
			pass
		pass
		
		
	"""
	Read publication.csv, add publication information in projects.
	"""
	wholeData = None
	wholeData = list()
	with open('data/publication.csv', 'rb') as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	        wholeData.append(row)
	        
    
	for items in wholeData:
	    if items['project_id'] in project.keys():
	        project[items['project_id']].papers[items['id']] = items['description']
	    pass
	    
	with gzip.open('data/Allprojects.pickle.gz', 'wb') as f:
	    Pickle.dump((project), f)
	
	print "Analysis data..."
	"""
	Read organization information. And connect organization with project.
	The whole data structure is a dictionary, and for each key (organization),
	the values (projects) saved in a list.
	"""
	wholeData = None
	wholeData = list()
	with open('data/contractor.csv','rb') as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	        wholeData.append(row)
	        
	organization = defaultdict(list)
	for items in wholeData:
	    if items['project_id'] in project.keys():
	        project[items['project_id']].organization.append(items['organization_id'])
	        organization[items['organization_id']].append(project[items['project_id']])
	        
	        
	with gzip.open('data/org_to_projects.pickle.gz', 'wb') as f:
	    Pickle.dump((organization), f)
	# Let's see how many project samples we have now. 8388
	print "We have", len(project.keys()), "completed projects."
	
	"""
	Now scan the whole sample, find out the valid project that the appliers
	published paper before this project. If no papers before this project,
	then our method is useless.
	"""
	valid_proj = defaultdict(list)
	for target_proj in project.keys():
	    org_of_Proj = project[target_proj].organization	
	    for org in org_of_Proj:
	        Proj_of_org = organization[org]
	        for proj in Proj_of_org:
	            if proj.end_date < project[target_proj].start_date:
	                # then we think this project is valid to use to evalue
	                # the target project
	                if proj.papers.keys():
	                    # then the target project is a valid sample for our case
	                    temp = _org_of_proj(len(proj.papers.keys()))
	                    for papers in proj.papers.keys():
	                        # here calculate similarity
	                        doc1 = proj.papers[papers]
	                        doc2 = project[target_proj].objectives
	                        sim = similarity(doc1, doc2)
	                        print sim
	                        temp.similarity.append(sim)
	                        pass
	                    valid_proj[target_proj].append(temp)
	                    pass
	                pass
	            pass
	        pass
	    pass
	pass
	
	print "We have", len(valid_proj.keys()),"valid samples."
	with gzip.open('data/valid_projects.pickle.gz', 'wb') as f:
	    Pickle.dump((valid_proj), f)
	return valid_proj
	
	# 1993 samples.
	
	
	
def main():
    Data = cleanData()
    pass
	        
	        
	
def similarity(doc1, doc2):
    """
    These code is from
    http://vene.ro/blog/word-movers-distance-in-python.html
    """
    W, vocab_dict = wordEmbedding()
    _doc1 = doc1
    _doc2 = doc2
    vect = CountVectorizer(stop_words="english").fit([_doc1, _doc2])
    # print("Features:",  ", ".join(vect.get_feature_names()))
    # It seems like some specific number is missing in voca_dict.
    # Just simply ingore them

    # Word check... Then no word check...
    newFeature = list()
    for w in vect.get_feature_names():
        try:
            vocab_dict[unidecode(w)]
            newFeature.append(unidecode(w))
        except KeyError:
            pass
            
    
    v_1 = [0 for w in newFeature]
    v_2 = [0 for w in newFeature]
    
    for wNo, w in enumerate(newFeature):
        if w in _doc1:
            v_1[wNo] = 1
        elif w in _doc2:
            v_2[wNo] = 1
                
    
    W_ = W[[vocab_dict[w] for w in newFeature]]        
    D_ = euclidean_distances(W_)
    v_1 = numpy.asarray(v_1)
    v_2 = numpy.asarray(v_2)
    v_1 = v_1.astype(numpy.double)
    v_2 = v_2.astype(numpy.double)
    v_1 /= v_1.sum()
    v_2 /= v_2.sum()

    D_ = D_.astype(numpy.double)
    D_ /= D_.max()
    
    return emd(v_1, v_2, D_)
    
    
def wordEmbedding():
    """
    These code is from 
    http://vene.ro/blog/word-movers-distance-in-python.html
    """
    if not os.path.exists("data/embed.dat"):
	    print ("Caching word embeddings in memmapped format...")
	    from gensim.models.word2vec import Word2Vec
	    wv = Word2Vec.load_word2vec_format("/home/medialab/NLP_data/GoogleNews-vectors-negative300.bin.gz", binary = True)
	    fp = numpy.memmap("data/embed.dat", dtype=numpy.double, mode='w+', shape=wv.syn0.shape)
	    fp[:] = wv.syn0[:]
	    with open("data/embed.vocab", "w") as f:
		    for _, w in sorted((voc.index, word) for word, voc in wv.vocab.items()):
			    print >> f, unidecode(w)
			    pass
	    del fp, wv
	

    W = numpy.memmap("data/embed.dat", dtype=numpy.double, mode="r", shape=(3000000, 300))
    with open("data/embed.vocab") as f:
	    vocab_list = map(str.strip, f.readlines())
    
  
    vocab_dict = {w:k for k,w in enumerate(vocab_list)}
    return W, vocab_dict
            
	        




def transferYMD(Y_M_D):
	"""
	This is the function used for transfor the year-month-day to a float.
	
	"""
	y_m_d = Y_M_D
	year = float(y_m_d[0:4])
	moth = float(y_m_d[5:7])
	day  = float(y_m_d[8:])
	return year+(moth*30+day)/365
	
	pass

















if __name__ == '__main__':
    main()
