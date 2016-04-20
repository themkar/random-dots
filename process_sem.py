import pickle

fileObject = open('my_patterns.pkl','r')  
b = pickle.load(fileObject)  
print p.categories, p.shape