#! /usr/bin/som python

from randomdots286_ver2 import *
import scipy
from scipy import io
p = Patterns(categories = 18, 
			items_per_category = [20, 3, 8, 18, 18, 15, 16, 28, 22, 17, 12, 43, 28, 5, 6, 11, 10, 6],
			pattern_height=21, pattern_width = 21,
			max_units_set = 24, 
			feature_overlap = False, 
			category_overlap = False, 
			include_prototypes = False, 
			compression_height = 10, 
			compression_width = 10, 
			distortion_per_item = [1,3,4,2,3,4,3,4,2,5,5,3,4,4,4,4,4,5,4,5,2,3,2,2,3,2,3,3,2,3,1,2,2,2,3,2,3,2,4,1,3,1,2,2,3,2,2,3,2,2,2,3,2,2,3,2,2,3,2,3,2,4,2,4,2,3,3,3,3,4,2,2,3,3,3,2,3,4,3,2,3,2,3,3,2,2,4,2,2,3,4,3,3,5,3,2,3,2,3,2,2,2,4,4,2,3,2,3,3,3,4,2,2,4,4,3,4,3,2,4,2,2,2,2,3,2,2,3,2,1,2,4,3,2,2,2,2,2,4,3,2,2,2,2,2,4,5,3,4,2,2,2,2,4,3,2,3,3,4,4,2,3,4,2,4,3,2,3,2,2,2,2,2,4,2,2,2,4,4,2,2,4,4,3,2,4,3,2,2,4,2,2,2,2,2,4,4,3,3,2,2,2,2,3,3,2,3,2,2,4,2,2,3,2,2,2,4,3,4,4,2,2,3,3,4,4,4,3,4,2,2,3,2,3,3,3,2,3,3,2,2,4,3,3,4,3,3,3,3,2,2,3,2,3,2,2,2,2,2,3,3,2,2,2,2,2,2,2,2,2,2,3,3,3,2,2,2,3,3,5,2,2,2,2,3,3])
		
p.Save('my_patterns21_21_24_NP_10_12_v2.pkl') #uncomment to save
p.Dendrograms('my_patterns21_21_24_NP_10_12_V3.pdf') #the string is part of the filename (optional), extension is optional can be pdf or png or jpg, will create file as appropriate
pdict = {'p':p.patterns}
bdict = {'b':p.compressed_representations}
prdict = {'pr':p.prototypes}
#print b.categories, b.patterns.shape
scipy.io.savemat('themismat_21_21_24_NP_10_12_V2',pdict , appendmat=True, format='5', long_field_names=False, do_compression=False, oned_as='row')
scipy.io.savemat('themismat_21_21_24_NP_10_12_cr_V2',bdict , appendmat=True, format='5', long_field_names=False, do_compression=False, oned_as='row')
scipy.io.savemat('themismat_21_21_24_NP_10_12_pr_V2',prdict , appendmat=True, format='5', long_field_names=False, do_compression=False, oned_as='row')
	
			







