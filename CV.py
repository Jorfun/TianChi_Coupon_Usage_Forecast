'''
    Use k-fold cross-validation to evaluate our feature set and model configuration.

    1. Load data from traning data file.
    2. Split the original dataset into k fold and do validation in turn.
        * Train classifier.
        * Output traning time.
        * Output classifier related parameters.
        * Output classifier performance (accuracy, roc_auc)
        * Draw ROC curve.
'''


from sklearn import tree
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.preprocessing import PolynomialFeatures
from collections import defaultdict
from itertools import cycle
import matplotlib.pyplot as plt
import numpy as np
import pydotplus
import random
import time        

        
    

def loadData(trainFilePath):
       
    xTrain = []
    yTrain = []
    trainCouponID = []


    f = open(trainFilePath, 'r')
     
    for line in f:
        temp = line.strip('\n').split(',')       
        
        try:
            trainCouponID.append(temp[2])
            xTrain.append([float(temp[3]), float(temp[4]), float(temp[5]), float(temp[6]), float(temp[7]), float(temp[8])]) 
            yTrain.append(float(temp[9]))                        
            
        except:
            print(temp)    
     
    f.close()
    
    ''' polynomial features '''
    # poly = PolynomialFeatures(degree=3)
    # xTrain = poly.fit_transform(xTrain)
    
    
    return xTrain, yTrain, trainCouponID




# calculateAverageAuc    PLUS    divide coupon_ids into two equal size sets, calculate average roc auc of each set.
def calculateAverageAucPlusAB(classifier, x_test, y_test, couponID_test, fw):

    # variables for averageAuc
    averageAuc = 0
    aucSum = 0
    aucCount = 0

    # variables for averageAucAB
    averageAucAB = []
    aucSumA = 0
    aucCountA = 0
    aucSumB = 0
    aucCountB = 0

    
    ''' 
        couponID_set用来保存所有出现的couponID(得到总数).
        coupon_x, coupon_y用来保存每个couponID对应的所有记录(为了后面针对不同couponID计算AUC).
        coupon_if_valid用来判断计算每个coupon_ID对应的AUC是否合法(是否只存在单个类的记录).
    '''
    couponID_set = set()
    coupon_x = defaultdict(list)
    coupon_y = defaultdict(list)
    coupon_if_valid = defaultdict(set)
    
    
    
    ''' 对couponID_test进行一次遍历, 记录一些相关信息. '''
    for coord, couponID in np.ndenumerate(couponID_test):  
        
        idx = coord[0]
        '''
        print('coord: ',coord)
        print('type(coord): ', type(coord))
        print('coord[0]: ', coord[0])
        print('x_test[coord[0]]: ', x_test[coord[0]])
        print('type(x_test[idx]): ', type(x_test[idx]))
        '''
        
        '''  
            对所有出现的couponID进行保存(couponID_set).
            将相同couponID的记录放在一起(方便后面针对单独couponID计算AUC).
            对所有couponID对应记录出现的类情况进行保存(遍历完后进行AUC计算合法性判断).
        '''
        if couponID != 'null':
            couponID_set.add(couponID)
            coupon_x[couponID].append(x_test[idx])      
            coupon_y[couponID].append(y_test[idx])    
            coupon_if_valid[couponID].add(y_test[idx])
    
    
    total_couponID_count = len(couponID_set)
    half_couponID_count = int(total_couponID_count / 2.0)
    fw.write('total couponID count for current cv set: '+str(total_couponID_count)+'\n')
    
    
    current_coupon_num = 0
    singleAuc = 0
    
    
    for couponID in couponID_set:
        current_coupon_num += 1
             
        if len(coupon_if_valid[couponID]) == 2:
            predictProbas = classifier.predict_proba(coupon_x[couponID])
            singleAuc = roc_auc_score(coupon_y[couponID], predictProbas[:, 1])
            
            '''
            print('couponID: '+couponID+'\n\n')
            print('coupon_x[couponID]: ', coupon_x[couponID], '\n\n')
            print('coupon_y[couponID]: ', coupon_y[couponID], '\n\n')
            print('predictProbas[:, 1]: ', predictProbas[:, 1], '\n\n')
            print('singleAuc: ', singleAuc, '\n\n')
            '''
            
            aucSum += singleAuc
            aucCount += 1 

            if current_coupon_num < half_couponID_count:
                aucSumA += singleAuc
                aucCountA += 1
            else:
                aucSumB += singleAuc
                aucCountB += 1                
              
    
    fw.write('valid coupon roc_auc count: '+str(aucCount)+'\n')
    fw.write('roc_auc countA: '+str(aucCountA)+'\n')
    fw.write('roc_auc countB: '+str(aucCountB)+'\n')
    
    
    averageAuc = aucSum/aucCount if aucCount != 0 else 0        
    averageAucAB.append([aucSumA/aucCountA if aucCountA != 0 else 0])
    averageAucAB.append([aucSumB/aucCountB if aucCountB != 0 else 0])
   
    return averageAuc, averageAucAB   




# output test    
def outputCVResults(classifier, x_test, y_test, couponID_test, cvIndex, color, directoryPath):
    
    predictProbas = classifier.predict_proba(x_test)
    print(predictProbas[:, 1], '\n')
    print(y_test, '\n')

    fpr, tpr, tresholds = roc_curve(y_test, predictProbas[:, 1])
    roc_auc = auc(fpr, tpr, reorder=True)
    
    
    fw = open(directoryPath+'CV'+str(cvIndex)+'.txt', 'w')
    
    fw.write('fpr    tpr:\n')
    for x,y in zip(fpr, tpr):
        fw.write(str(x)+'    '+str(y)+'\n')
    fw.write('\n\n')


    # Adaboost attributes
    fw.write('classes_   :\n'+str(classifier.classes_ )+'\n\n')
    fw.write('n_classes_   : '+str(classifier.n_classes_)+'\n\n')
    fw.write('estimator_weights_ : '+str(classifier.estimator_weights_  )+'\n\n')
    fw.write('estimator_errors_  : '+str(classifier.estimator_errors_ )+'\n\n') 

    # logistic regression attributes
    '''
    fw.write('coef_  :\n'+str(classifier.coef_  )+'\n\n')
    fw.write('intercept_  : '+str(classifier.intercept_  )+'\n\n')
    fw.write('n_iter_  : '+str(classifier.n_iter_  )+'\n\n') 
    '''
 
    # decision tree attributes
    '''
    fw.write('classes_ :\n'+str(classifier.classes_ )+'\n\n')
    fw.write('feature_importances_ : '+str(classifier.feature_importances_ )+'\n\n')
    fw.write('max_features_ : '+str(classifier.max_features_ )+'\n\n')
    fw.write('n_classes_ : '+str(classifier.n_classes_ )+'\n\n')
    fw.write('n_features_ : '+str(classifier.n_features_ )+'\n\n')
    fw.write('n_outputs_ : '+str(classifier.n_outputs_ )+'\n\n')
    '''
    
    # random forest attributes
    '''
    fw.write('classes_ :\n'+str(classifier.classes_ )+'\n\n')
    fw.write('n_classes_ : '+str(classifier.n_classes_ )+'\n\n')
    fw.write('n_features_ : '+str(classifier.n_features_ )+'\n\n')
    fw.write('n_outputs_ : '+str(classifier.n_outputs_ )+'\n\n')
    fw.write('feature_importances_ : '+str(classifier.feature_importances_ )+'\n\n')
    '''

    # classifier performance
    fw.write('example input: '+str(x_test[0,:])+'\n')
    fw.write('example label: '+str(y_test[0])+'\n')
    fw.write('example predicted probability: '+str(predictProbas[0,1])+'\n')
    fw.write('mean accuracy on the given test data and labels: %f \n' % classifier.score(x_test, y_test))
    fw.write('roc_auc_score(overall): '+str(roc_auc)+'\n')   
 
    start_time = time.time() 
    averageAuc, averageAucAB = calculateAverageAucPlusAB(classifier, x_test, y_test, couponID_test, fw)
    fw.write('Time for calculating average roc_auc AB: '+str(time.time()  - start_time)+'\n')
    fw.write('roc_auc_score(average over coupon_id): '+str(averageAuc)+'\n')
    fw.write('roc_auc_score(average over coupon_id) AB: '+str(averageAucAB)+'\n')

    fw.close()

    plt.plot(fpr, tpr, color=color, lw=2, label='ROC fold %d (area = %0.2f)' % (cvIndex, roc_auc))
    
    # draw decision tree
    '''
    dot_data = tree.export_graphviz(classifier, out_file=None) 
    graph = pydotplus.graph_from_dot_data(dot_data) 
    graph.write_pdf(directoryPath+'tree-'+str(cvIndex)+'.pdf') 
    '''




def cv(x, y, couponID, directoryPath):

    #xTrainTest = x[:10, :]
    
    x = np.array(x)
    y = np.array(y)
    couponID = np.array(couponID)
    
    print('x:\n', x, '\n')
    print('y:\n', y, '\n')
    print('couponID:\n', couponID, '\n')
    
    
    
    # SET CV PARAMETERS HERE !!!!
    cv = StratifiedKFold(n_splits=3)
    #cv = KFold(n_splits=3)
    colors = cycle(['cyan', 'blue', 'darkorange', 'yellow', 'indigo', 'seagreen'])
    cvIndex = 0
    
    

    for (train_index, test_index), color in zip(cv.split(x, y), colors):
    #for train_index, test_index in cv.split(x, y):
        cvIndex += 1
        x_train, x_test, y_train, y_test = x[train_index], x[test_index], y[train_index], y[test_index]
        couponID_test = couponID[test_index]

        print('train_index: %s\ntest_index: %s' % (train_index, test_index))
        print('couponID_test:\n', couponID_test, '\n')
        print('x_train:\n', x_train, '\n')
        print('x_test:\n', x_test, '\n')
        print('y_train:\n', y_train, '\n')
        print('y_test:\n', y_test, '\n')
        print('y_test.shape', str(y_test.shape), '\n')
        
        
        
        # SET CLASSIFIER PARAMETERS HERE !!!!
        start_time = time.time()
        #clf = tree.DecisionTreeClassifier(max_depth=4, class_weight='balanced')  #
        #clf = RandomForestClassifier(max_depth=3, n_jobs=-1, class_weight='balanced')
        #clf = LogisticRegression(class_weight='balanced')
        clf = AdaBoostClassifier(base_estimator=LogisticRegression(class_weight='balanced'), n_estimators=50)
        clf.fit(x_train, y_train)
        print('Time for training model: ', time.time()  - start_time, '\n')
        outputCVResults(clf, x_test, y_test, couponID_test, cvIndex, color, directoryPath)
        
        
        
    plt.plot([0, 1], [0, 1], color='k', lw=2, linestyle='--', label='Luck')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()   

    
    
    
directoryPath = 'original_data' + '/'
trainFilePath = directoryPath+'training.csv'
#outputFilePath = directoryPath+'cvResults.csv'

x, y, trainCouponID = loadData(trainFilePath)
  
#print(xTrain)
#print('\n')
#print(yTrain)

cv(x, y, trainCouponID, directoryPath)
