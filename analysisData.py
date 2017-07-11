'''
    Minor analysis toward traning data.

    Check if two classes is balanced within current training set.
    Check values and corresponding scaled values of a specific feature.
    Check values and all unique values of a specific feature.
'''


from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import RobustScaler


def checkFeatureValues(inputFilePath, outputFilePath, featureColumnNum):
       
    column = []
    unique_values = set()
 
    fr = open(inputFilePath, 'r')
    
    
    for idx,line in enumerate(fr):
        temp = line.strip('\n').split(',')
        
        try:
            column.append([temp[featureColumnNum]])
            unique_values.add(temp[featureColumnNum])
        except:
            print(temp)
        
    fr.close()
    

    fw = open(outputFilePath, 'w')
    
    fw.write('List all values:\n')
    for idx in range(0, len(column)):
        fw.write(column[idx][0]+'\n')
    fw.write('\n\n\n\n'+'List all unique values:\n')
    
    for value in unique_values:
        fw.write(value+'\n')
    
    fw.close()



def checkFeatureScaling(inputFilePath, outputFilePath, scaler, featureColumnNum):
       
    column = []
 
    fr = open(inputFilePath, 'r')
    
    
    for idx,line in enumerate(fr):
        temp = line.strip('\n').split(',')
        
        try:
            column.append([float(temp[featureColumnNum])])

        except:
            print(temp)
        
    fr.close()
    
    
    scaler.fit(column) 
    columnScaled = scaler.transform(column)    
    
    
    fw = open(outputFilePath, 'w')
    
    for idx in range(0, len(column)):
        fw.write(str(column[idx][0])+' -> '+str(columnScaled[idx,0])+'\n')
    
    fw.close()


def checkClassBalance(inputFilePath, outputFilePath):
    
    fr = open(inputFilePath, 'r')
    
    negativeCount = 0
    positiveCount = 0
    
    for idx,line in enumerate(fr):
        temp = line.strip('\n').split(',')
        
        if temp[10] == '0':
            negativeCount += 1
        else:
            positiveCount +=1
              
    fr.close()    
    
    fw = open(outputFilePath, 'w')
    
    fw.write('positiveCount: '+str(positiveCount)+'\n'+'negativeCount: '+str(negativeCount))
    
    fw.close()
    
    
    

    

directory = 'original_data' + '/'
inputFilePath = directory+'ccf_offline_stage1_train_couponRatio.csv'
outputFilePath = directory+'analysis.csv'



# Check if two classes is balanced within current training set
#checkClassBalance(inputFilePath, outputFilePath)


'''
# Check values and corresponding scaled values of a specific feature
featureColumnNum = 4
scaler = MinMaxScaler()
checkFeatureScaling(inputFilePath, outputFilePath, scaler, featureColumnNum)
'''


# Check values and all unique values of a specific feature
featureColumnNum = 5
checkFeatureValues(inputFilePath, outputFilePath, featureColumnNum)
