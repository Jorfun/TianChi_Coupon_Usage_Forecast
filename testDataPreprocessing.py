'''
    Process testing data in order to get our intended feature set. 
'''


from collections import defaultdict

'''
reference = dict()
reference = {'01': 0, '02': 31, '03': 60, '04': 91, '05': 120, '06': 151}
boudary = 15

def dateToNum(month, day):
    return reference[month] + int(day)
'''    
    
    
    
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
                # special case: user_id 2495873,1286474, 5733898... is not appeared in offline_train but exists in offline_test
                if temp[0] not in table:
                    newLine = newLine + '5.5'
                else:
                    newLine = newLine + table[temp[0]]
            else:
                newLine = newLine + temp[i]    
                
            if i < columnNum-1:
                newLine = newLine + ','
            
        fw.write(newLine+'\n')        
 
    fr.close()    
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
                # special case: user_id is not appeared in offline_train but exists in offline_test
                if temp[0] not in table:
                    newLine = newLine + '0' + ',' + temp[i]
                else:
                    newLine = newLine + table[temp[0]] + ',' + temp[i]
            else:
                newLine = newLine + temp[i]    
                
            if i < columnNum-1:
                newLine = newLine + ','
            
        fw.write(newLine+'\n')        
 
    fr.close()    
    fw.close()
    
 
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
                #print(table[temp[1]][0], '   ',type(table[temp[1]][0]), '   ',table[temp[1]][1], '   ',type(table[temp[1]][1]), '   ', temp[i])
                newLine = newLine + table[temp[1]][0] + ',' + table[temp[1]][1] + ',' + temp[i]
            else:
                newLine = newLine + temp[i]    
                
            if i < columnNum-1:
                newLine = newLine + ','
            
        fw.write(newLine+'\n')        
 
 
    fr.close()    
    fw.close()



'''    
def addHotPeriod(dayConsump, baseFilePath, outputFilePath):
    
    dateConsump = dict()
    
    fr = open(dayConsump, 'r') 
    
    for line in fr:
        temp = line.strip('\n').split(',')
        dateConsump[int(temp[0])] = temp[1]

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
    

         
directory = 'original_data' + '/'
offlineTestFilePath = directory+'ccf_offline_stage1_test_revised.csv'
offlineTestDiscountFilePath = directory+'ccf_offline_stage1_test_discount.csv'
userDistanceTableFilePath = directory+'userDistanceTable.csv'
offlineTestDistanceFilePath = directory+'ccf_offline_stage1_test_distance.csv'
userConsumpTableFilePath = directory+'userConsumpTable.csv'
offlineTestUserConsumpFilePath = directory+'ccf_offline_stage1_test_userConsump.csv'
merchantConsumpTableFilePath = directory+'merchantConsumpTable.csv'
offlineTestMerchantConsumpFilePath = directory+'ccf_offline_stage1_test_merchantConsump.csv'
twoMonthConsumpFilePath = directory+'day_consumption.csv'
#offlineTestHotPeriodFilePath = directory+'ccf_offline_stage1_test_hotPeriod.csv'

# process testing data
processDiscountRate(offlineTestFilePath, offlineTestDiscountFilePath)
processDistance(userDistanceTableFilePath, offlineTestDiscountFilePath, offlineTestDistanceFilePath)
addUserConsump(userConsumpTableFilePath, offlineTestDistanceFilePath, offlineTestUserConsumpFilePath)
addMerchantConsump(merchantConsumpTableFilePath, offlineTestUserConsumpFilePath, offlineTestMerchantConsumpFilePath)
#addHotPeriod(dayConsumpFilePath, offlineTestMerchantConsumpFilePath, offlineTestHotPeriodFilePath)