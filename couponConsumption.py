'''
    Get some information about coupon consumption from training data.
    * how many coupons were used.
    * how many coupons were received.
    * how many coupons were used 15 days later since their receive date.
    * how many coupons were used within 15 days period since their receive date.
    * other related ratios.
'''


reference = dict()
#daysOfMonths = {'01': 31, '02': 29, '03': 31, '04': 30, '05': 31, '06': 30}
reference = {'01': 0, '02': 31, '03': 60, '04': 91, '05': 120, '06': 151}
boudary = 15




def dateToNum(month, day):
    #print(month, '\n')
    #print(day, '\n')
    #print(reference[month] + int(day), '\n\n')
    return reference[month] + int(day)




def getStatistics(inputFilePath, outpurFilePath, isOffline):
    
    record_count = 0
    coupon_use = 0
    coupon_receive = 0
    
    above15_coupon_use = 0
    below15_coupon_use = 0
    coupon_id_idx = 0
    
    if isOffline:
        coupon_id_idx = 2
    else:
        coupon_id_idx = 3
  
  
    fr = open(inputFilePath, 'r')
    
 
    for idx,line in enumerate(fr):
        temp = line.strip('\n').split(',')
        
        if temp[coupon_id_idx] != 'null':
            coupon_receive += 1
            
            if temp[6] != 'null':
                coupon_use += 1              
                date_consumption = temp[6]
                date_received = temp[5]
                interval = dateToNum(date_consumption[4:6], date_consumption[6:]) - dateToNum(date_received[4:6], date_received[6:])
                #print(interval, ' = ',dateToNum(date_consumption[4:6], date_consumption[6:]), ' - ', dateToNum(date_received[4:6], date_received[6:]))
                
                if interval > 15:
                    above15_coupon_use += 1
                else:
                    below15_coupon_use += 1

                '''
                print(temp[6], '\n')
                coupon_use_date = str(temp[6])
                print(coupon_use_date[4:6], '\n')
                print(coupon_use_date[6:], '\n')
                exit()
                '''

    fr.close()
    
    record_count = idx + 1
    
    
    fw = open(outputFilePath, 'w')
    fw.write('above15_coupon_use = '+str(above15_coupon_use)+'\n')
    fw.write('below15_coupon_use = '+str(below15_coupon_use)+'\n')
    fw.write('coupon_use = '+str(coupon_use)+'\n')
    fw.write('coupon_receive = '+str(coupon_receive)+'\n')
    fw.write('record_count = '+str(record_count)+'\n')
    fw.write('above15_coupon_use / coupon_use = '+str(above15_coupon_use/coupon_use)+'\n')
    fw.write('coupon_use / coupon_receive = '+str(coupon_use/coupon_receive)+'\n')
    fw.write('coupon_receive / record_count = '+str(coupon_receive/record_count)+'\n')
    fw.write('coupon_use / record_count = '+str(coupon_use/record_count)+'\n')  
    fw.close()    
    

    

inputFilePath = 'original_data/ccf_offline_stage1_train.csv'
outputFilePath = 'original_data/ccf_offline_stage1_train_info.csv'

getStatistics(inputFilePath, outputFilePath, isOffline = True)

'''
inputFilePath = 'original_data/ccf_online_stage1_train.csv'
outputFilePath = 'original_data/ccf_online_stage1_train_info.csv'

getStatistics(inputFilePath, outputFilePath, isOffline = False)
'''