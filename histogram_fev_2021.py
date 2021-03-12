import numpy as np

def PSD(Diam):
  Size = [1.19,1.00,0.85,0.71,0.59,0.50,0.425,0.355,0.30,0.25,0.21]
  #Size = [1.20,1.10,1.00,0.90,0.80,0.70,0.60,0.50,0.40,0.30,0.20]
  Malha = [16,18,20,25,30,35,40,45,50,60,70]

  Class = np.zeros(11,dtype=int)

  for item in Diam:
    
    if item > Size[0]:
      Class[0] = Class[0]+1     

    if item > Size[1] and item <= Size[0]:
      Class[1] = Class[1]+1 
      
    if item > Size[2] and item <= Size[1]:
      Class[2] = Class[2]+1       
      
    if item > Size[3] and item <= Size[2]:
      Class[3] = Class[3]+1       

    if item > Size[4] and item <= Size[3]:
      Class[4] = Class[4]+1    

    if item > Size[5] and item <= Size[4]:
      Class[5] = Class[5]+1    
      
    if item > Size[6] and item <= Size[5]:
      Class[6] = Class[6]+1       
   
    if item > Size[7] and item <= Size[6]:
      Class[7] = Class[7]+1  
      
    if item > Size[8] and item <= Size[7]:
      Class[8] = Class[8]+1   
      
    if item > Size[9] and item <= Size[8]:
      Class[9] = Class[9]+1       
    
    if item > Size[10] and item <= Size[9]:
      Class[10] = Class[10]+1  
      
  Class = Class[::-1] # write inverse order
  
  Perc = Class*100/np.sum(Class)
  
  return Class, Perc
