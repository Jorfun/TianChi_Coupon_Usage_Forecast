'''
    Process training data in order to get our intended feature set. 
'''


from collections import defaultdict
import numpy as np

reference = dict()
reference = {'01': 0, '02': 31, '03': 60, '04': 91, '05': 120, '06': 151}
boundary = 15




def dateToNum(month, day):
    return reference[month] + int(day)




# remove all records without coupon_id    
def onlyRecordsWithCouponID(inputFilePath, outputFilePath):
    fr = open(inputFilePath, 'r')
    fw = open(outputFilePath, 'w')
    

    for line in fr:
        temp = line.strip('\n').split(',')
        
        if temp[2] != 'null':
            fw.write(line)
              
    fr.close()    
    fw.close()

    
    
    
# transfrom all discount_rate data into [0,1]
def processDiscountRate(inputFilePath, outputFilePath):
    fr = open(inputFilePath, 'r')
    fw = open(outputFilePath, 'w')    
 
    for line in fr:
        temp = line.strip('\n').split(',')
        symbolPos = temp[3].find(':')
        
        if symbolPos > 0:
            #print(temp[3],'    ',temp[3][symbolPos:],'    ',temp[3][:symbolPos])
            discountRate = str(1 - float(temp[3][symbolPos+1:]) / float(temp[3][:symbolPos]))
            columnNum = len(temp)
            newLine = ''
            
            for i in range(columnNum):
                if i == 3:
                    newLine = newLine + discountRate    
                else:
                    newLine = newLine + temp[i]    
                
                if i < columnNum-1:
                    newLine = newLine + ','
            
            fw.write(newLine+'\n')
            
        else:      
            fw.write(line) 
 
 
    fr.close()    
    fw.close()    


    
    
# distance lookup table for null distance records. Average of all distance values of coupon received records
def userDistanceTable(inputFilePath, outputFilePath):
    
    userDist = defaultdict(list)
    
    fr = open(inputFilePath, 'r')   
 
    for line in fr:
        temp = line.strip('\n').split(',')
        
        if temp[2] != 'null' and temp[4] != 'null':
            userDist[temp[0]].append(float(temp[4]))
            
    
    fr.seek(0)  
    fw = open(outputFilePath, 'w')

    for line in fr:
        temp = line.strip('\n').split(',')
        userRecordNum = len(userDist[temp[0]])
        
        if userRecordNum > 0:
            newDist = str(sum(userDist[temp[0]]) / userRecordNum)
        else:
            newDist = str(5.5)           

        fw.write(temp[0]+','+newDist+'\n')        
 
    fr.close()
    fw.close()
 
    
    
    
 # transfrom null distance data into user's average distance
def processDistance(userDistanceTable, baseFilePath, outputFilePath):
    # read data from table
    table = dict()
    
    fr = open(userDistanceTable, 'r') 

    for line in fr:
        temp = line.strip('\n').split(',')
        table[temp[0]] = temp[1]     

    fr.close()    
    
    
    # process distance values and output new file
    fr = open(baseFilePath, 'r')
    fw = open(outputFilePath, 'w')    
    
    for line in fr:
        temp = line.strip('\n').split(',')

        columnNum = len(temp)
        newLine = ''        
        
        for i in range(columnNum):
            if i == 4 and temp[i] == 'null': 
                newLine = newLine + table[temp[0]]
            else:
                newLine = newLine + temp[i]    
                
            if i < columnNum-1:
                newLine = newLine + ','
            
        fw.write(newLine+'\n')        
 
    fr.close()    
    fw.close()


    
    
 # feature - users' degree of coupon consumption, coupon_consump / coupon received
def userConsumpTable(inputFilePath, outputFilePath):
    
    userCouponInfo = defaultdict(lambda: [0,0])
    
    fr = open(inputFilePath, 'r')   
 
    for line in fr:
        temp = line.strip('\n').split(',')
        
        if temp[2] != 'null':
            userCouponInfo[temp[0]][0] += 1
            
            if temp[6] != 'null':
                userCouponInfo[temp[0]][1] += 1
    
    fr.close()  
    fw = open(outputFilePath, 'w')
    
    for key in userCouponInfo:
        if userCouponInfo[temp[0]][0] != 0:
            ratio = str(userCouponInfo[key][1] / userCouponInfo[key][0])
        else:
            ratio = '0'
       
        fw.write(key+','+ratio+'\n')        
 
    fw.close()
    


    
def addUserConsump(userConsumpTable, baseFilePath, outputFilePath):
    table = dict()
    
    fr = open(userConsumpTable, 'r') 

    for line in fr:
        temp = line.strip('\n').split(',')
        table[temp[0]] = temp[1]     

    fr.close()    
    
    fr = open(baseFilePath, 'r')
    fw = open(outputFilePath, 'w')    
    
    for line in fr:
        temp = line.strip('\n').split(',')

        columnNum = len(temp)
        newLine = ''        
        
        for i in range(columnNum):
            if i == 5:
                newLine = newLine + table[temp[0]] + ',' + temp[i]
            else:
                newLine = newLine + temp[i]    
                
            if i < columnNum-1:
                newLine = newLine + ','
            
        fw.write(newLine+'\n')        
 
    fr.close()    
    fw.close()




# version one  -  two features: 1. 商户x的消费记录个数 / 总消费记录个数 (商户的消费热度)    2.商户x的coupon消费个数 / 该商户coupon received个数
def merchantConsumpTable(inputFilePath, outputFilePath):
    
    merchantConsumpInfo = defaultdict(lambda: [0,0,0])
    totalRecordsNum = 0
    
    fr = open(inputFilePath, 'r')  
    
    
    for line in fr:
        temp = line.strip('\n').split(',')    
         
        if temp[6] != 'null':
            merchantConsumpInfo[temp[1]][0] += 1
            totalRecordsNum += 1  
        
        if temp[2] != 'null':
            merchantConsumpInfo[temp[1]][1] += 1
    
            if temp[6] != 'null':
                merchantConsumpInfo[temp[1]][2] += 1
        
        
    fr.close()
    
    fw = open(outputFilePath, 'w')
    
    for merchant in merchantConsumpInfo:
        f1 = merchantConsumpInfo[merchant][0] / totalRecordsNum
        f2 = merchantConsumpInfo[merchant][2] / merchantConsumpInfo[merchant][1] if merchantConsumpInfo[merchant][1] != 0 else 0
        fw.write(merchant+','+str(f1)+','+str(f2)+'\n')
    
    fw.close()

  
  
'''
# version two  -  two features: 1. 商户x的coupon消费个数 / 总coupon消费个数 (商户优惠券消费热度)    2.商户x的coupon消费个数 / 该商户coupon received个数
def merchantConsumpTable(inputFilePath, outputFilePath):
    
    merchantConsumpInfo = defaultdict(lambda: [0,0])
    totalCouponConsump = 0
    
    fr = open(inputFilePath, 'r')  
    
    
    for line in fr:
        temp = line.strip('\n').split(',')    
        
        if temp[2] != 'null':
            merchantConsumpInfo[temp[1]][0] += 1
    
            if temp[6] != 'null':
                merchantConsumpInfo[temp[1]][1] += 1
                totalCouponConsump += 1
        
    fr.close()
    
    fw = open(outputFilePath, 'w')
    
    for merchant in merchantConsumpInfo:
        f1 = merchantConsumpInfo[merchant][1] / totalCouponConsump
        f2 = merchantConsumpInfo[merchant][1] / merchantConsumpInfo[merchant][0] if merchantConsumpInfo[merchant][0] != 0 else 0
        fw.write(merchant+','+str(f1)+','+str(f2)+'\n')
    
    fw.close()  
'''  
  
  
  
def addMerchantConsump(merchantConsumpTable, baseFilePath, outputFilePath):
    table = defaultdict(lambda: ['0','0'])
    
    fr = open(merchantConsumpTable, 'r') 

    for line in fr:
        temp = line.strip('\n').split(',')
        table[temp[0]][0] = temp[1]
        table[temp[0]][1] = temp[2]        

    fr.close()    
    
    
    fr = open(baseFilePath, 'r')
    fw = open(outputFilePath, 'w')    
    
    for line in fr:
        temp = line.strip('\n').split(',')

        columnNum = len(temp)
        newLine = ''        
        
        for i in range(columnNum):
            if i == 6:
                newLine = newLine + table[temp[1]][0] + ',' + table[temp[1]][1] + ',' + temp[i]
            else:
                newLine = newLine + temp[i]    
                
            if i < columnNum-1:
                newLine = newLine + ','
            
        fw.write(newLine+'\n')        
 
 
    fr.close()    
    fw.close()



def addHotPeriod(twoMonthConsump, baseFilePath, outputFilePath):
    dayConsump = []

    fr = open(twoMonthConsump, 'r')

    for line in fr:
        temp = line.strip('\n').split(',')
        dayConsump.append((int(temp[0]),int(temp[1])))

    fr.close()    

    points = np.array(dayConsump)

    # get x and y vectors
    x = points[:,0]
    y = points[:,1]

    # calculate polynomial
    z = np.polyfit(x, y, 8)
    #print(z, '\n')
    f = np.poly1d(z)
    #print(f, '\n')
    
    x_new = list(range(0,59))    
    y_new = f(x_new)
    totalSum = sum(y_new)
    print('totalSum: ', totalSum, '\n')
    fr = open(baseFilePath, 'r') 
    fw = open(outputFilePath, 'w') 

    for line in fr:
        temp = line.strip('\n').split(',')
        
        receiveDate = temp[8]
        receiveDateNum = dateToNum(receiveDate[4:6], receiveDate[6:]) % 60
        accumuConsump = 0
        
        for x_new in range(receiveDateNum, receiveDateNum+15):
            if x_new >= 60:
                x_new = x_new % 60

            y_new = f(x_new)
            accumuConsump += y_new   
                
        ratio = accumuConsump / totalSum
        
        
        '''
        x_new = list(range())
        y_new = f(x_new)
        accumuConsump = sum(y_new)
        '''
        
        '''
        print('receiveDateOrdinal: ', receiveDateOrdinal, '\n')
        print('x_new: ', x_new, '\n')
        print('y_new: ', y_new, '\n')
        print('accumuConsump: ', accumuConsump, '\n')
        print('ratio: ', ratio, '\n')
        '''
        
        columnNum = len(temp)
        newLine = ''        
        
        for i in range(columnNum):
            if i == 8:
                newLine = newLine + str(ratio) + ',' + temp[i]
            else:
                newLine = newLine + temp[i]    
                
            if i < columnNum-1:
                newLine = newLine + ','
            
        fw.write(newLine+'\n')          
    
    
    
    
'''     
# version 1   
def markLabel(inputFilePath, outputFilePath):
    fr = open(inputFilePath, 'r') 
    fw = open(outputFilePath, 'w') 
    
    for line in fr:
        temp = line.strip('\n').split(',')
        label = '-1'
        
        if temp[2] != 'null' and temp[9] != 'null':
            label = '1'
        else:
            label = '0'       
        
        columnNum = len(temp)
        newLine = ''        
        
        for i in range(columnNum):
            if i == 8:
                newLine = newLine + label + ',' + temp[i]
            else:
                newLine = newLine + temp[i]    
                
            if i < columnNum-1:
                newLine = newLine + ','
            
        fw.write(newLine+'\n')           
        
        
    fr.close()    
    fw.close()    
'''    
        
     
# version 2: only 15 below cousumption will be considered as positive   
def markLabel(inputFilePath, outputFilePath):
    fr = open(inputFilePath, 'r') 
    fw = open(outputFilePath, 'w') 
    
    for line in fr:
        temp = line.strip('\n').split(',')
        label = '-1'
        consumpDate = temp[10]
        
        if temp[2] != 'null' and consumpDate != 'null':
            receiveDate = temp[9]
            
            if dateToNum(consumpDate[4:6], consumpDate[6:]) - dateToNum(receiveDate[4:6], receiveDate[6:]) <= boundary:
                label = '1'
            else:
                label = '0'
                
        else:
            label = '0'       
        
        columnNum = len(temp)
        newLine = ''        
        
        for i in range(columnNum):
            if i == 9:
                newLine = newLine + label + ',' + temp[i]
            else:
                newLine = newLine + temp[i]    
                
            if i < columnNum-1:
                newLine = newLine + ','
            
        fw.write(newLine+'\n')           
        
        
    fr.close()    
    fw.close()    

        
         

directory = 'original_data' + '/'
offlineTrainFilePath = directory+'ccf_offline_stage1_train.csv'
offlineTrainCouponFilePath = directory+'ccf_offline_stage1_train_coupon.csv'
offlineTrainDiscountFilePath = directory+'ccf_offline_stage1_train_discount.csv'
userDistanceTableFilePath = directory+'userDistanceTable.csv'
offlineTrainDistanceFilePath = directory+'ccf_offline_stage1_train_distance.csv'
userConsumpTableFilePath = directory+'userConsumpTable.csv'
offlineTrainUserConsumpFilePath = directory+'ccf_offline_stage1_train_userConsump.csv'
merchantConsumpTableFilePath = directory+'merchantConsumpTable.csv'
offlineTrainMerchantConsumpFilePath = directory+'ccf_offline_stage1_train_merchantConsump.csv'
twoMonthConsumpFilePath = directory+'two_month_consump.csv'
offlineTrainHotPeriodFilePath = directory+'ccf_offline_stage1_train_hotPeriod.csv'
trainingSetFilePath = directory+'training.csv'

# process training data
onlyRecordsWithCouponID(offlineTrainFilePath, offlineTrainCouponFilePath)
processDiscountRate(offlineTrainCouponFilePath, offlineTrainDiscountFilePath)
userDistanceTable(offlineTrainFilePath,userDistanceTableFilePath)
processDistance(userDistanceTableFilePath, offlineTrainDiscountFilePath, offlineTrainDistanceFilePath)
userConsumpTable(offlineTrainFilePath, userConsumpTableFilePath)
addUserConsump(userConsumpTableFilePath, offlineTrainDistanceFilePath, offlineTrainUserConsumpFilePath)
merchantConsumpTable(offlineTrainFilePath, merchantConsumpTableFilePath)
addMerchantConsump(merchantConsumpTableFilePath, offlineTrainUserConsumpFilePath, offlineTrainMerchantConsumpFilePath)
addHotPeriod(twoMonthConsumpFilePath, offlineTrainMerchantConsumpFilePath, offlineTrainHotPeriodFilePath)
markLabel(offlineTrainHotPeriodFilePath, trainingSetFilePath)




'''    
# deprecated
def addHotPeriod(dayConsump, baseFilePath, outputFilePath):
    
    dateConsump = dict()
    
    fr = open(dayConsump, 'r') 
    
    for line in fr:
        temp = line.strip('\n').split(',')
        dateConsump[int(temp[0])] = int(temp[1])

    fr.close()
    
    
    fr = open(baseFilePath, 'r') 
    fw = open(outputFilePath, 'w') 

    for line in fr:
        temp = line.strip('\n').split(',')
        
        receiveDate = temp[8]
        receiveDateOrdinal = dateToNum(receiveDate[4:6], receiveDate[6:])
        accumuConsump = 0
        
        for i in range(receiveDateOrdinal, receiveDateOrdinal+15):
            if i in dateConsump:
                accumuConsump += dateConsump[i]
        
        
        columnNum = len(temp)
        newLine = ''        
        
        for i in range(columnNum):
            if i == 8:
                newLine = newLine + str(accumuConsump) + ',' + temp[i]
            else:
                newLine = newLine + temp[i]    
                
            if i < columnNum-1:
                newLine = newLine + ','
            
        fw.write(newLine+'\n')      
'''        