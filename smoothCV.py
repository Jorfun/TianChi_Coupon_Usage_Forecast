'''
    Do clustering to all users according to feature 3 (online consumption ratio) 
    and feature 4 (coupon consumption ratio), assign each user to their closest
    cluster. Then we smooth all users' feature 3 and feature 4 according to their
    clusters' values (average).
'''


#import numpy as np
#import matplotlib.pyplot as plt
#import math
import sys
import time




# Get information of cluster center
def loadClusterCenter(k):

    clusterCenter = [[0] * 2 for i in range(k)]
    
    f = open('cluster/center(' + str(k) + ').csv', 'r')
    
    for idx, line in enumerate(f):
        temp = line.strip('\n').split(',')
        clusterCenter[idx][0] = float(temp[1])
        clusterCenter[idx][1] = float(temp[2])
    
    return clusterCenter


    
    
#   Get and smooth cross validation data (using dictionary to search users' cluster)
def smoothCVData(inputFile, outputFile, CVIndex, k, alpha):
    
    # Get cluster center information
    clusterCenter = loadClusterCenter(k)
    print(clusterCenter)
    
    
    # Save user clustering result (recording which cluster a certain user is belong to) to a dictionary
    f = open('cluster/usrclus('+str(k)+').csv', 'r')
    searchlines = f.readlines()
    f.close()
    
    userClusterDic = dict()
    
    for idx,line in enumerate(searchlines):
        temp = line.strip('\n').split(',')
        userClusterDic[temp[0]] = int(temp[1])
        
    
    fr = open(inputFile, 'r')
    fw = open(outputFile, 'w')
    
    userID = "XXXXXXX"
    userCluster = -1
    
    for idx,line in enumerate(fr):
        temp = line.strip('\n').split(',')
        
        # if current record has the same userID as previous record, we don't need to repeat smoothing.
        # Otherwise, we need to find the corresponding cluster of this user and smooth feature3 and feature4.
        if(temp[0] != userID):
            userID = temp[0]
            userCluster = userClusterDic.get(temp[0])
            
            if userCluster is None: sys.exit('No cluster found for '+userID+'\n') 
            
            smoothFeature3 = float(temp[4]) * alpha + (1 - alpha) * clusterCenter[userCluster-1][0]
            smoothFeature4 = float(temp[5]) * alpha + (1 - alpha) * clusterCenter[userCluster-1][1]
  
        fw.write(temp[2]+','+temp[3]+','+str(smoothFeature3)+','+str(smoothFeature4)+','+temp[6]+'\n')
        #print(temp[4],'  * ', str(alpha), ' + ', str(1-alpha), ' * ', str(clusterCenter[userCluster-1][0]), ' = ', str(float(temp[4]) * alpha + (1 - alpha) * clusterCenter[userCluster-1][0]))
        #print('userID: '+userID, 'userCluster: '+ str(userCluster), '\n')  
    
    fr.close()
    fw.close()    

    
    
    
start_time = time.time()    
    
CVIndex = 2
clusterNum = 10    
alpha = 0.2
    
#smooth training data

inputFile = 'traincv5f/train' + str(CVIndex) + '.csv'
outputFile = 'traincv5f/trainSmooth' + str(CVIndex) + '-' + str(clusterNum)+ '-' +str(alpha) + '.csv'
smoothCVData(inputFile, outputFile, CVIndex, clusterNum, alpha)

middle_time = time.time()
print('Time for smoothing training data: ', middle_time - start_time, '\n')


#smooth testing data
inputFile = 'testcv5f/test' + str(CVIndex) + '.csv'
outputFile = 'testcv5f/testSmooth' + str(CVIndex) + '-' + str(clusterNum)+ '-' +str(alpha) + '.csv'
smoothCVData(inputFile, outputFile, CVIndex, clusterNum, alpha)

end_time = time.time()
print('Time for smoothing testing data: ', end_time - middle_time)