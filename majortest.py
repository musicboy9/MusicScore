import math
# c d e f g a b 
# 0 2 4 5 7 9 11

def majortest(fftList):
    melodycnt = [0] * 12
    for i in fftList:
        freq = i[0]
        temp = math.log(freq / 261.63 * 2, 2) * 12
        i = round(temp)
        melodycnt[int (i % 12)] += 1

    # shop major
    
    if melodycnt[5] < melodycnt[6]: # F#
        
        if melodycnt[0] < melodycnt[1]: # C#
            
            if melodycnt[7] < melodycnt[8]: # G#
                
                if melodycnt[2] < melodycnt[3]: # D#
                    
                    if melodycnt[9] < melodycnt[10]: # A#
                        
                        if melodycnt[4] < melodycnt[5]: # E#
                            
                            if melodycnt[11] < melodycnt[0]: # B#
                                return 'cis'
                            
                            return 'fis'
                            
                        return 'b'
                        
                    return 'e'
                
                return 'a'
                
            return 'd'
            
        return 'g'
       
        
    # flat major
    
    if melodycnt[10] > melodycnt[11]:
        
        if melodycnt[3] > melodycnt[4]:
            
            if melodycnt[8] > melodycnt[9]:
                
                if melodycnt[1] > melodycnt[2]:
                    
                    if melodycnt[7] > melodycnt[8]:
                        
                        if melodycnt[0] > melodycnt[1]:
                            
                            if melodycnt[4] > melodycnt[5]:
                                
                                return 'ces'
                                
                            return 'ges'
                            
                        return 'des'
                        
                    return 'aes'
                    
                return 'ees'
                
            return 'bes'
            
        return 'f'
        
    return 'c'
                                