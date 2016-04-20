#! /usr/bin/som python

from randomdots286 import *
p = Patterns(categories = 3, items_per_category = [10, 8, 4, 1], include_prototypes = False)
p.Save('my_patterns.pkl') #uncomment to save
p.Dendrograms('my_patterns.pdf') #the string is part of the filename (optional), extension is optional can be pdf or png or jpg, will create file as appropriate
#p.Load('my_patterns.pkl') #uncomment to load
