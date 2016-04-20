#! /usr/bin/som python

from randomdots286 import *
p = Patterns(categories = 18, items_per_category = [20, 3, 8, 18, 18, 15, 16, 28, 22, 17, 12, 43, 28, 5, 6, 11, 10, 6], include_prototypes = False)
p.Save('my_patterns.pkl') #uncomment to save
p.Dendrograms('my_patterns.pdf') #the string is part of the filename (optional), extension is optional can be pdf or png or jpg, will create file as appropriate
#p.Load('my_patterns.pkl') #uncomment to load

