#! /usr/bin/som python
import numpy as np
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt
import random as r
import string
import sys

import cPickle as pickle

import scipy.ndimage
import scipy.misc
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import pdist
from sklearn.preprocessing import normalize

import hashlib
import seaborn as sns
def Random(max_value, min_value = 0):
  """Random integer from min_value to max_value"""
  return int(r.randint(min_value, max_value))

class Patterns:
  """A class that creates, stores, and loads random dot patterns.

  Keyword arguments:
  categories             -- number of categories
  levels_of_distortion   -- levels within a category that increasingly distort items away from the prorotype
  items_per_level        -- how many category members per level
  items_per_category     -- if previous two parameters are given, this value is set to (1 + levels_of_distortion * items_per_level), otherwise if a list is provided this is used to generate categories; default value = None
  pattern_width          -- width of an individual category item (same for all items)
  pattern_height         -- ditto
  max_units_set          -- how many features/units set to 'on'/1
  include_prototypes     -- whether prototypes are included in the final set of patterns
  feature_overlap        -- whether prototypes may have common features with each other
  category_overlap       -- whether catgeory members may be closer to the prototype of another category than to their own
  compression_width      -- the width of the compressed version of the binary patterns
  compression_height     -- ditto
  distortion             -- parameter that controls the amount of compression/blurring that occurs; can be list/numpy array or scalar
  """
  def __init__(self, categories = None, levels_of_distortion = None, items_per_level = None, items_per_category = None,
               pattern_width = 30, pattern_height = 50, max_units_set = 20,
               feature_overlap = False, category_overlap = False, compression_overlap = False,
               compression_width = 20, compression_height = 25, distortion = 0.07,
               patterns = None, prototypes = None, include_prototypes = True):


    if levels_of_distortion is None and items_per_level is None and items_per_category is None:
      #if levels_of_distortion is None and items_per_level is None:
        #raise Exception('Please specify either both the levels_of_distortion and the items_per_level or just the items_per_category!')  
      #if items_per_category is None:      
        raise Exception('Please specify either both the levels_of_distortion and the items_per_level or just the items_per_category!')  

    self.categories = categories
    self.levels_of_distortion = levels_of_distortion

    if isinstance(items_per_level, list) or isinstance(items_per_level, np.ndarray):
      self.items_per_level = items_per_level
    elif isinstance(items_per_level, int):
      self.items_per_level = np.ones(categories)
      self.items_per_level.fill(items_per_level)
    else:
      self.items_per_level = None
 
    self.labels = []


    #if a list of items per category is provided the three variables above are ignored and reset
    if isinstance(items_per_category, list) or isinstance(items_per_category, np.ndarray):
      self.items_per_category = np.asarray(items_per_category)
      self.items_per_level = None
      self.levels_of_distortion = 1
      self.categories = len(items_per_category)
      #in this case items per category and items per level are identical

    elif isinstance(items_per_category, int):
      #self.items_per_level = np.ones(categories)
      #self.items_per_level.fill(items_per_level)
      self.items_per_category = np.ones(categories)
      self.items_per_category.fill(items_per_category)
      self.items_per_level = None
      self.levels_of_distortion = 1
    #otherwise just for sanity check, set this to the value calculated based on the following
    #elif items_per_category is None:
    else:
      self.items_per_category = None
      #self.items_per_category = np.ones(categories)
      #self.items_per_category.fill(1 + levels_of_distortion * items_per_level)
      #it is NOT the same as items_per_level, but it's redundent in this case
    
    self.pattern_num = 0
    #for c in range(self.categories):
      #if self.items_per_level is None:
        #items = int(self.items_per_category[c])
      #if self.items_per_category is None:
        #items = int(1 + levels_of_distortion * self.items_per_level[c])
      #for i in range(items):
        ##print c, i, self.pattern_num
        #self.pattern_num += 1
    self.include_prototypes = include_prototypes

    if self.items_per_category is not None:
      self.pattern_num = self.items_per_category.sum()
    elif self.items_per_level is not None:
      if self.include_prototypes:
        self.pattern_num = self.categories * (1 + self.levels_of_distortion * self.items_per_level[0])
      else:
        self.pattern_num = self.categories * (self.levels_of_distortion * self.items_per_level[0])
        
    #self.pattern_num = self.categories * (1 + self.levels_of_distortion * self.items_per_level)
    self.pattern_width = pattern_width
    self.pattern_height = pattern_height
    self.max_units_set = max_units_set
    
    self.feature_overlap = feature_overlap
    self.category_overlap = category_overlap
    self.compression_overlap = compression_overlap

    self.compression_width = compression_width #int(self.pattern_width*0.5)
    self.compression_height = compression_height #int(self.pattern_height*0.5)
    self.compressed_representations = np.zeros((self.pattern_num, self.compression_width, self.compression_height))
    
    
    if isinstance(distortion, list) or isinstance(distortion, np.ndarray):
      self.distortion = distortion
    else:
      self.distortion = np.ones(self.pattern_num)
      self.distortion.fill(distortion)
    
    if patterns is None:
      self.patterns = np.zeros((self.pattern_num, self.pattern_width, self.pattern_height))
    else:
      self.patterns = patterns
      
    if prototypes is None:
      self.prototypes = np.zeros((self.categories, self.pattern_width, self.pattern_height))
    else:
      self.prototypes = prototypes
      
    if patterns is not None and prototypes is not None:
      self.calculate_compressed_representations()
    else: 
      self.CreatePatterns()
      
      
  def calculate_compressed_representations(self):
    """Create the compression version of the patterns and return it."""
    #for each pattern
    for i, p in enumerate(self.patterns):
      #calculate what the self.compressed_representations is
      self.compressed_representations[i] = scipy.misc.imresize(p, (self.compression_width, self.compression_height), interp='bicubic', mode=None)
      self.compressed_representations[i] = scipy.ndimage.filters.gaussian_filter(self.compressed_representations[i], (1 - self.distortion[i]))
      
    self.compressed_representations += 0.00001
    self.compressed_representations /= np.linalg.norm(self.compressed_representations, axis = 0) #normalise
    #return self.compressed_representations.reshape((self.pattern_num, self.compression_width*self.compression_height))
  
  def Save(self, file_name = 'temp.pkl'):
     """Save to pickle file.

     Keyword arguments:
     file_name -- default value = 'temp.pkl'"""
     f = open(file_name, 'w')
     pickle.dump(self, f)
     
  def Load(self, file_name = 'temp.pkl'):
     """Save to pickle file.

     Keyword arguments:
     file_name -- default value = 'temp.pkl'"""
     f = open(file_name, 'r')
     new_self = pickle.load(f)
     self.__init__(categories = new_self.categories,
                   levels_of_distortion = new_self.levels_of_distortion,
                   items_per_level = new_self.items_per_level,
                   items_per_category = new_self.items_per_category,
                   pattern_width = new_self.pattern_width,
                   pattern_height = new_self.pattern_height,
                   max_units_set = new_self.max_units_set,
                   feature_overlap = new_self.feature_overlap,
                   category_overlap = new_self.category_overlap,
                   compression_overlap = new_self.compression_overlap,
                   compression_width = new_self.compression_width,
                   compression_height = new_self.compression_height,
                   distortion = new_self.distortion,
                   patterns = new_self.patterns,
                   prototypes = new_self.prototypes,
                   include_prototypes = new_self.include_prototypes
                  )
        
  def CreatePatterns(self):
    """Generate the patterns based on the pre-specificed properties."""
    self.create_patterns()
    self.calculate_compressed_representations()

    
  def create_patterns(self):
    """Generate the patterns based on the pre-specificed properties."""
    
    # for readability I have split this into various loops; who cares about time/space complexity
    # this loop generates the prototypes
    coord = [] #keep track of coordinates for setting features to 1
    o = 0 #counter for patterns overall, used further down
    hash_list = []
    #for each category and so therefore for each prototype we are about to create
    #(remember it's one prorotype per category)
    for i in range(0, self.categories):
      #we just started on this prototype for this category
      #so there is no way we have set anything to 1 
      units_set = 0
      #print 'create_patterns', self.categories, self.levels_of_distortion, self.items_per_category, self.items_per_level

      #while the units set are less than maximum we want to set
      #meaning that we will do the following untill all the units are set
      while (units_set < self.max_units_set):
        #while (p[i, x, y] == 1): # look for unit that is not set
          #get some random coordinates for the potentially 'on' feature
          x = Random(self.pattern_width-1)
          y = Random(self.pattern_height-1)
          #if we don't want overlap, uncomment the following three lines
          if not self.feature_overlap:
            while (x,y) in coord: # again look for unit that has not been set in previous patterns
              #print 'Coordinate ({0:3d}, {1:3d}) rejected because it causes feature overlap.'.format(x, y)
              print('Prototype for category {0:3d} rejected because it causes feature overlap.'.format(i))

              x = Random(self.pattern_width-1)
              y = Random(self.pattern_height-1)
          #after all this, we have discovered (hopefully) an appropriate x and y
          #so we use those random coordinates to set a feature to 1  
          self.prototypes[i, x, y] = 1
          
          #we just set a unit to on, so we want to know that for pattern i (x, y) is on
          #so in the near future when we generate a new set of coordinates
          #we can compare them to what we have generated previously
          coord.append((x,y))
          #and we are counting up how many we have set so far, so we know when to stop
          units_set = units_set + 1
          
      #so we are done with the ith prototype, we are now going to create the other members of the ith category
      #set the oth pattern to the prototype we just created above
      #print 'create_patterns', self.categories, self.levels_of_distortion, self.items_per_category, self.items_per_level

      if self.include_prototypes:
        self.patterns[o, :, :] = self.prototypes[i, :, :]
        #print self.patterns[o, :, :]
        #we have now moved up from the oth pattern
        #so we are on the (o+1)th 
        o += 1
        hash_list.append(hashlib.sha1(self.prototypes[i, :, :]).hexdigest())
        self.labels.append(str(i)+'*')
        
        if self.items_per_level is not None:
          items = int(self.items_per_level[i])
        elif self.items_per_category is not None:
          items = int(self.items_per_category[i] - 1)
      else:
        
        if self.items_per_level is not None:
          items = int(self.items_per_level[i])
        elif self.items_per_category is not None:
          items = int(self.items_per_category[i])          

      #here we are initialising two distances,
      #which we use further down to calculate the dist between 
      #a member of a category and the category prototype 
      dist = np.zeros([self.categories])
           
      #for every pattern in this category
      for l in range(self.levels_of_distortion):
        for e in range(items):
            print i, l, e, items
            #print 'create_patterns', self.categories, self.levels_of_distortion, self.items_per_category, self.items_per_level

            #calculate the value of distortion to send to generate_item
            distortion = l+1
            #send it a prototype and an amount of distortion
            item = self.generate_item(self.prototypes[i, :, :], distortion)
            item_hash = hashlib.sha1(item).hexdigest()

            while str(item_hash) in hash_list:
                item = self.generate_item(self.prototypes[i, :, :], distortion)
                item_hash = hashlib.sha1(item).hexdigest()
                #print str(item_hash), hash_list, min(dist), dist[i]
                #print str(item_hash) in hash_list

            #now we have generated an item we will calculate the distance of the current item
            #to all the prototypes per category we generated above
            #what we want is the current item to be closest to the prototype from which it was generated above
            #and not closer to any other prototype
            for c in range(self.categories):
                #calculate euclidan distance between item and all prototypes
                dist[c] = np.linalg.norm(item-self.prototypes[c,:,:])
            
            #initialise a counter for keeping track how many times we will re-create items
            counter = 0
            #if the minimum distance is not between an item and the ith prototype
            #it was generated from, do the following...
            if not self.category_overlap:
              while min(dist) != dist[i]:
                  item = self.generate_item(self.prototypes[i, :, :], distortion)
                  item_hash = hashlib.sha1(item).hexdigest()
                  counter += 1

                  #tell the user what happened
                  print('Item {0:3d} at level {1:2d} in category {2:2d} rejected because it causes category overlap; attempt: {3:3d}.'.format(o, l, i, counter+1))
                  #then generate a new item from the ith prototype, using the level of distortion we calculated above

                  while str(item_hash) in hash_list:
                      item = self.generate_item(self.prototypes[i, :, :], distortion)
                      item_hash = hashlib.sha1(item).hexdigest()
                      print str(item_hash), hash_list, min(dist), dist[i]
                      print str(item_hash) in hash_list
                      #increement this counter because things might get out of control, so we want to know
                      counter += 1
                  #we need to calculate new distances between our new item and the prototypes, so we can know which it's closest to
                  for c in range(self.categories):
                      dist[c] = np.linalg.norm(item-self.prototypes[c,:,:])
            print('Item {0:3d} at level {1:2d} in category {2:2d} saved!'.format(o, l, i))
            #since it has passed all the overlap requirements we can save the oth pattern        
            self.patterns[o, :, :] = item
            hash_list.append(hashlib.sha1(item).hexdigest())
            self.labels.append(str(i)+str(l)+str(e))

            #and move on to (o+1)th
            o += 1

  def generate_item(self, prototype, distortion):
    """Create a category member given a prototype and a distortion level."""
    item = np.zeros_like(prototype)
    distortion = distortion * 0.25
    indices = np.asarray(np.nonzero(prototype))
    noise = np.round(np.random.uniform(-distortion,distortion,indices.shape))
    noise = np.round(np.random.normal(loc=0.0, scale=distortion, size = indices.shape)).astype(int)

    indices += noise

    z = np.where(indices < 0)
    indices[z] = 0
    z = np.where(indices[0,:] >= self.pattern_width)
    indices[0, z] = self.pattern_width - 1
    z = np.where(indices[1,:] >= self.pattern_height)
    indices[1, z] = self.pattern_height - 1

    indices = tuple(indices)
    item[indices] = 1
    return item


  def dendrogram(self, X, metric = 'Euclidean', linkage = 'ward', x_label = 'Patterns'):
      """Generate hierarchical dendrogram.

      Keyword arguments:
      metric    -- distance metric; default value = 'Euclidean'
      linkage   -- default value = 'ward'"""
      X = X.reshape((X.shape[0], X.shape[1] * X.shape[2]))
      Z = sch.linkage(X, linkage)
      c, coph_dists = sch.cophenet(Z, pdist(X, metric))
      # Cophenetic Correlation Coefficient of clustering.
      # This compares (correlates) the actual pairwise distances of all your samples to those implied by the hierarchical clustering.
      # The closer the value is to 1, the better the clustering preserves the original distances.
      print 'Cophenetic correlation coefficient of clustering (the closer to 1, the better):', c

      # calculate full dendrogram
      fig = plt.figure(figsize=(20, 10))
      ax = fig.add_subplot(111)
      plt.title('Hierarchical Clustering Dendrogram')
      plt.xlabel(x_label)
      plt.ylabel(metric + ' Distance')
      sch.dendrogram(
          Z,
          leaf_rotation=90,  # rotates the x axis labels
          leaf_font_size=25,  # font size for the x axis labels
          labels = self.labels

      )
      ax.set_ylim(bottom=-0.5) 
      ax.tick_params(labelsize=25)
      
  def Dendrograms(self, fig_save_as = 'temp.pdf'):
      """Generate hierarchical dendrograms for both the binary and the compressed patterns."""
      X = self.patterns
      self.dendrogram(X, metric = 'Jaccard', x_label = 'Patterns')  
      plt.savefig('dendrogram_'+fig_save_as)

      X = self.compressed_representations
      self.dendrogram(X, metric = 'Euclidean', x_label = 'Compressed Patterns')  
      plt.savefig('compressed_dendrogram_'+fig_save_as)

      plt.show()  
      
      
    
if __name__ == "__main__":
  
  if sys.argv[1:] != []:
    p = Patterns()
    p.load(sys.argv[1])
  else:
    p = Patterns(categories = 3, items_per_category = [10, 8, 4, 1], include_prototypes = False)
    p.Dendrograms()

    #p = Patterns(categories = 10, items_per_category = 3, include_prototypes = False)
    #p.Dendrograms()
    #p = Patterns(categories = 4, levels_of_distortion = 4, items_per_level = 1, include_prototypes = False)
    #p.Dendrograms()
    
    #p = Patterns(categories = 4, items_per_category = 4, include_prototypes = False)
    #p.Dendrograms()

  
    #p.Save()
    #p.Load()

  #print p.patterns[0]
