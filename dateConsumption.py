'''
    Analyse the relationship between coupon consumption and day/week/month/two month.
'''


from collections import defaultdict
import matplotlib.pyplot as plt




reference = dict()
#daysOfMonths = {'01': 31, '02': 29, '03': 31, '04': 30, '05': 31, '06': 30}
reference = {'01': 0, '02': 31, '03': 60, '04': 91, '05': 120, '06': 151}
January1st = 5



  
def dateToNum(month, day):
    return reference[month] + int(day)   




def dateToDayOfWeek(month, day):
    result = (reference[month] + int(day) + January1st) % 7 
    return result if result != 0 else 7




def getStatistics(inputFilePath, weekConsumpFilePath, monthConsumpFilePath, monthConsumpForNormFilePath, twoMonthConsumpFilePath, isOffline):
    
    weekConsump = defaultdict(lambda: 0)
    monthConsump = defaultdict(lambda: 0)
    twoMonthConsump = defaultdict(lambda: 0)
    monthConsumpForNorm = []
    

    if isOffline:
        coupon_id_idx = 2
    else:
        coupon_id_idx = 3
  
    
    fr = open(inputFilePath, 'r')  
    
    for line in fr:
        temp = line.strip('\n').split(',')
        consumpDate = temp[6]
        
        if temp[coupon_id_idx] != 'null' and consumpDate != 'null':
            month = consumpDate[4:6]
            day = consumpDate[6:]
            dayOfWeek = str(dateToDayOfWeek(month, day))  
            weekConsump[dayOfWeek] += 1
            monthConsump[day] += 1
            #print(dateToNum(month, day) % 60)
            twoMonthConsump[dateToNum(month, day) % 60] += 1
            monthConsumpForNorm.append(day)
            
    fr.close()
    
    
    sortedDayConsump = sorted(weekConsump)
    fw = open(weekConsumpFilePath, 'w')
    
    for key in sortedDayConsump:
        fw.write(key+','+str(weekConsump[key])+'\n')
    
    fw.close() 
    
    
    sortedMonthConsump = sorted(monthConsump)
    fw = open(monthConsumpFilePath, 'w')

    for key in sortedMonthConsump:
        fw.write(key+','+str(monthConsump[key])+'\n')
    
    fw.close()     

    
    sortedTwoMonthConsump = sorted(twoMonthConsump)
    fw = open(twoMonthConsumpFilePath, 'w')

    for key in sortedTwoMonthConsump:
        fw.write(str(key)+','+str(twoMonthConsump[key])+'\n')
    
    fw.close()     

    
    fw = open(monthConsumpForNormFilePath, 'w')

    for value in monthConsumpForNorm:
        fw.write(value+'\n')
    
    fw.close() 
    
    


def draw(inputFilePath):
    consumpCount = []
    time = []
    
    f = open(inputFilePath, 'r')
    
    for idx,line in enumerate(f):
        temp = line.strip('\n').split(',')
        consumpCount.append(temp[1])
        time.append(idx+1)
    
    plt.plot(time,consumpCount)   
    plt.show()




inputFilePath = 'original_data/ccf_offline_stage1_train.csv'
weekConsumpFilePath = 'original_data/week_consumption.csv'
monthConsumpFilePath = 'original_data/month_consumption.csv'
monthConsumpForNormFilePath = 'original_data/month_consump_norm.csv'
twoMonthConsumpFilePath = 'original_data/two_month_consump.csv'

getStatistics(inputFilePath, weekConsumpFilePath, monthConsumpFilePath, monthConsumpForNormFilePath, twoMonthConsumpFilePath, isOffline = True)
draw(twoMonthConsumpFilePath)
