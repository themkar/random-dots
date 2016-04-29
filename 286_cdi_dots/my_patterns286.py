#! /usr/bin/som python

from randomdots286 import *
import scipy
from scipy import io
p = Patterns(categories = 18, items_per_category = [20, 3, 8, 18, 18, 15, 16, 28, 22, 17, 12, 43, 28, 5, 6, 11, 10, 6],pattern_height=21, pattern_width = 21,max_units_set = 24, feature_overlap = False, category_overlap = False, include_prototypes = False, compression_height = 10, compression_width = 10)
p.Save('my_patterns21_21_24_NP_10_12.pkl') #uncomment to save
p.Dendrograms('my_patterns21_21_24_NP_10_12.pdf') #the string is part of the filename (optional), extension is optional can be pdf or png or jpg, will create file as appropriate
pdict = {'p':p.patterns}
bdict = {'b':p.compressed_representations}
#print b.categories, b.patterns.shape
scipy.io.savemat('themismat_21_21_24_NP_10_12',pdict , appendmat=True, format='5', long_field_names=False, do_compression=False, oned_as='row')
scipy.io.savemat('themismat_21_21_24_NP_10_12_cr',bdict , appendmat=True, format='5', long_field_names=False, do_compression=False, oned_as='row')

p = Patterns(categories = 18, items_per_category = [20, 3, 8, 18, 18, 15, 16, 28, 22, 17, 12, 43, 28, 5, 6, 11, 10, 6],pattern_height=21, pattern_width = 21,max_units_set = 24, feature_overlap = True, category_overlap = False, include_prototypes = False, compression_height = 10, compression_width = 10)
p.Save('my_patterns21_21_24_NP_10_12_FO.pkl') #uncomment to save
p.Dendrograms('my_patterns21_21_24_NP_10_12_FO.pdf') #the string is part of the filename (optional), extension is optional can be pdf or png or jpg, will create file as appropriate
pdict = {'p':p.patterns}
bdict = {'b':p.compressed_representations}
#print b.categories, b.patterns.shape
scipy.io.savemat('themismat_21_21_24_NP_10_12_FO',pdict , appendmat=True, format='5', long_field_names=False, do_compression=False, oned_as='row')
scipy.io.savemat('themismat_21_21_24_NP_10_12_FO_cr',bdict , appendmat=True, format='5', long_field_names=False, do_compression=False, oned_as='row')

p=Patterns(categories = 18, items_per_category = [20, 3, 8, 18, 18, 15, 16, 28, 22, 17, 12, 43, 28, 5, 6, 11, 10, 6],pattern_height=21, pattern_width = 21,max_units_set = 24, feature_overlap = True, category_overlap = False, include_prototypes = False, compression_height = 10, compression_width = 10, distortion = 0.21)
p.Save('my_patterns21_21_24_NP_10_12_FO_d0p21.pkl') #uncomment to save
p.Dendrograms('my_patterns21_21_24_NP_10_12_FO_d0p21.pdf') #the string is part of the filename (optional), extension is optional can be pdf or png or jpg, will create file as appropriate
pdict = {'p':p.patterns}
bdict = {'b':p.compressed_representations}
#print b.categories, b.patterns.shape
scipy.io.savemat('themismat_21_21_24_NP_10_12_FO_d0p21',pdict , appendmat=True, format='5', long_field_names=False, do_compression=False, oned_as='row')
scipy.io.savemat('themismat_21_21_24_NP_10_12_FO_cr_d0p21',bdict , appendmat=True, format='5', long_field_names=False, do_compression=False, oned_as='row')










