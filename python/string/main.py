#!/usr/bin/env python  
# -*- coding:utf-8 -*-  

str1 = "0123456789"
str2 = "0123456789"
print(id(str1), id(str2))

str3 = str1 + str2 + "0123456789"
str4 = "012345678901234567890123456789"
print(id(str3), id(str4))

str5 = str1 + str2
str6 = str1 * 2

print(id(str5), id(str6))

# 执行结果
# 2829986588656 2829986588656
# 2829985733168 2829985733008
# 2829985733328 2829986502816
