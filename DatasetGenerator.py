import os
import numpy as np
from PIL import Image

import torch
from torch.utils.data import Dataset

#-------------------------------------------------------------------------------- 

class DatasetGenerator (Dataset):
    
    #-------------------------------------------------------------------------------- 
    
    def __init__ (self, pathImageDirectory, pathDatasetFile, transform):
    
        self.listImagePaths = []
        self.listImageLabels = []
        self.transform = transform
        self.lineItems = [] 
        #---- Open file, get image paths and labels
    
        fileDescriptor = open(pathDatasetFile, "r")
        line = True 
        #---- get into the loop
        
        line = fileDescriptor.readline()

                
            
            #--- if not empty
        if line:
            self.lineItems = line.split()
            print(self.lineItems[0])
            imagePath = os.path.join(pathImageDirectory, self.lineItems[0])
            imageLabel = "24"
            imageLabel = [int(i) for i in imageLabel]
            self.listImagePaths.append(imagePath)
            self.listImageLabels.append(imageLabel)
        
            
        fileDescriptor.close()
    
    #-------------------------------------------------------------------------------- 
    
    def __getitem__(self, index):
        
        imagePath = self.listImagePaths[index]
        
        imageData = Image.open(imagePath).convert('RGB')
        imageLabel= torch.FloatTensor(self.listImageLabels[index])
        
        if self.transform != None: imageData = self.transform(imageData)
        
        return imageData, imageLabel
        
    #-------------------------------------------------------------------------------- 
    
    def __len__(self):
        
        return len(self.listImagePaths)
    
 #-------------------------------------------------------------------------------- 
    def get_path(self):
        return self.lineItems[0]
