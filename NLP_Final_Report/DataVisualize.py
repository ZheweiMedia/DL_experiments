#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
check if Innovative projects have more paper published.
What do we need? 
Program ---> projects ---> publications

@Author: Zhewei

"""

from __future__ import division
import csv

import os
import gzip
import codecs
import numpy
import gzip
import cPickle as Pickle
from collections import defaultdict
from DataAnalysis import _project, _org_of_proj
from DataAnalysis import wordEmbedding, similarity
from matplotlib.pyplot import figure, show
import matplotlib.pyplot as pyplot

class _proj_with_paper:
    def __init__(self, ID, dis, paperNo):
        self.ID = ID
        self.dis = dis
        self.paper_number = paperNo


def main():
        
    print "Reading raw data..."
    
    all_project = Pickle.load(gzip.open( 'data/Allprojects.pickle.gz', 'rb'))
    print "We have",len(all_project.keys()), "completed projects."
    
    # read whole project data to get progam_id information
    wholeData = list()
    with open('data/project.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            wholeData.append(row)
    # read publication.csv to find the projects have paper published
    wholePaper = list()
    with open('data/publication.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            wholePaper.append(row)
            
    # completed projects have paper published
	CompletedPapers = dict()
	for items in wholePaper:
	    if items['project_id'] in all_project.keys():
	        CompletedPapers[items['project_id']] = len(all_project[items['project_id']].papers.keys())
	
	print "We have", len(CompletedPapers.keys()), "completed projects have paper published."     
    program = defaultdict(list)
    for items in wholeData:
        if items['rcn'] in CompletedPapers.keys():
            program[items['program_id']].append(all_project[items['rcn']])
    
    print program.keys()
    
    innovationPorj = defaultdict(list)
    # word mover distance
    All_obj = defaultdict(list)
    for SinglePro in program.keys():
        Allobj = list()
        for proJ in program[SinglePro]:
            Allobj.append(proJ.objectives)
        # if only one project in a program, then it's useless to compare
        if len(Allobj) > 1:
            All_obj[SinglePro] = Allobj
            
    innovationPorj = Pickle.load(gzip.open( 'data/innovationPorj.pickle.gz', 'rb'))
            
    for SinglePro in program.keys()[0:2]:
        for proJNo, proJ in enumerate(innovationPorj[SinglePro]):
            totalNo = len(innovationPorj[SinglePro])
            print totalNo
            color = ((proJNo+25*totalNo)/(50*totalNo+25*totalNo),0,0)
            print 
            proJ, = pyplot.plot(proJ.dis, proJ.paper_number, 'o', color = color)
    
    pyplot.xlabel('Document distance. one VS. rest.')
    pyplot.ylabel('Publication quantity')      
    pyplot.show()



























if __name__ == '__main__':
    main()


