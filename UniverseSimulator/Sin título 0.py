 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 09:45:50 2022

@author: jesus
"""
import math
def myround(x, base=5):
    init = base * math.floor(float(x) / base)
    
    if init >= 100:
        return '>' + str(100) 
    
    end =  base * math.ceil(float(x) / base)
    if init == end:
        end = end + 5
    return str(init) + '-' + str(end - 1)

if __name__ == "__main__":
    print(myround(0))
    print(myround(106))