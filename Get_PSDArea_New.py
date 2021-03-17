import cv2
import numpy as np
import pandas as pd
from PIL import Image

def PSDArea(df_size):
  Frame = 13.14 # mm conferir se este representa o correto
  Size_foto=1200 # tamanho da foto (se mudar no big_segment.py tem q alterar aqui)
  fc = Frame / Size_foto
  Width=np.array(df_size['Width'])
  Size=28
  Nx, Ny = df_size.shape
  
  Area_todas = []
  Diam_todos = []
  for qual_img in range(Nx):
    L = Width[qual_img]*fc
    data=np.array(df_size.drop('Width',axis=1).iloc[qual_img]).reshape(Size,Size)
    img = Image.fromarray(data.astype('uint8'), mode='L')
    img=np.float32(img)
    
    mean_value = np.mean(img)
    img_new = img.copy()
    
    img28=cv2.resize(img,(Size,Size), interpolation = cv2.INTER_AREA)
    Foto=np.array(img28).reshape(28,28)
    
    '''
    for i in range(28):
      for j in range(28):
        if img[i,j] < mean_value*1.05:
          img_new[i,j] = 255
        else:
          img_new[i,j] = 0
    '''
    for i in range(28):
      for j in range(28):
        if img[i,j] < mean_value*0.9:
          img_new[i,j] = 255
        else:
          img_new[i,j] = 0
        if (i < 1) or (i>27) or (j <1) or (j>27):
          img_new[i,j] = 0
          
        '''  
        raio = ((i-14.0)**2+(j-14.0)**2)**0.5
        if (raio > 14.0*0.9):
          img_new[i,j] = 255
        else:
          img_new[i,j] = 0
        '''  
    
    #for qual_img in range(Nx):
    Area = np.sum(img_new) / (255.0 * 28 * 28)* L*L
    Diam = 2.0 * (Area/np.pi)**0.5
    Area_todas.append(Area)
    Diam_todos.append(Diam)
    
  return Area_todas, Diam_todos

