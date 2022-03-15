#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 08:54:16 2022

@author: jesus
"""

class C(object):

    def controls(self, attribute_value_pair):
        eval_string = attribute_value_pair[0] + " = " + str(attribute_value_pair[1])
        exec(eval_string)


value1, value2, value3 = (1, 2, 3)
my_object = C()

print("original values:", my_object.__dict__)

inputs = {"A":["self.arg1", value1],
          "S":["self.arg2", value2],
          "D":["self.arg3", value3]}

my_object.controls(inputs["A"]) #my object, not my class...
my_object.controls(inputs["S"])
my_object.controls(inputs["D"])

#Even this one works:
my_object.controls(("self.totally_new_attribute", "str('other value')"))


print("modified values:", my_object.__dict__)