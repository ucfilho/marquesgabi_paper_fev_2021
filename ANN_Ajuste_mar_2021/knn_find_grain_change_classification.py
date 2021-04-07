# -*- coding: utf-8 -*-
"""KNN_FIND_GRAIN_change_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Gxpb-d9_RMxP7Un7NvrmiAMujgI4YgxO
"""

import matplotlib.pyplot as plt
import random
import numpy as np
import cv2
import zipfile
from random import randint
from PIL import Image
import re
from sklearn.model_selection import train_test_split
import skimage
import pandas as pd
import sklearn
import matplotlib.pyplot as plt

from skimage import transform

# from sklearn.neural_network import MLPClassifier
# since its a multi-class prediction, in order to prevent error we need some library
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier

knn = OneVsRestClassifier(KNeighborsClassifier())

def knnGrain(df,df_class):
  y_valor=df['Type']

  quantidade= df.groupby('Type').size()

  df_G = df[df["Type"] == "G"] 
  Cut=['Unnamed: 0','Type','Width']
  FotosG= df_G.drop(Cut,axis=1)


  Size=28
  img_G=[]

  Num,cols=FotosG.shape
  for i in range(Num):
    data=np.array(FotosG.iloc[i]).reshape(Size,Size)
    img = Image.fromarray(data.astype('uint8'), mode='L')
    img=np.float32(img)
    img28=cv2.resize(img,(Size,Size), interpolation = cv2.INTER_AREA)
    img_G.append(img28)

  df_Z = df[df["Type"] == "Z"] 
  Cut=['Unnamed: 0','Type','Width']
  FotosZ= df_Z.drop(Cut,axis=1)

  # We'll choose which is grain and withdraw from 750 segmented photos

  Size=28
  img_Z=[]

  Num,cols=FotosZ.shape
  for i in range(Num):
    data=np.array(FotosZ.iloc[i]).reshape(Size,Size)
    img = Image.fromarray(data.astype('uint8'), mode='L')
    img=np.float32(img)
    img28=cv2.resize(img,(Size,Size), interpolation = cv2.INTER_AREA)
    img_Z.append(img28)

  GRAO=[0,146,149,166,217,222,223,257,268,286,455,482,538,612,644,647,651,677] # 0 ate 749
  GRAO=np.array(GRAO)
  Ind=FotosZ.index
  FotosNG=FotosZ.copy()
  for i in GRAO:
    FotosNG=FotosNG.drop(Ind[i])

  PERCENT=245.0/(len(FotosNG.index))
  FotosNG=FotosNG.sample(frac=PERCENT, replace=True)

  rows,col=FotosG.shape
  y_total=[] # grao-->zero, nao grao-->1
  for i in range(rows):
    y_total.append(0) #  # grao-->zero
  for i in range(rows,(2*rows)):
    y_total.append(1) #  # nao grao-->zero

  frames = [FotosG,FotosNG]
  result = pd.concat(frames)

  #Define data train and data test

  W_train, W_test, yw_train, yw_test = train_test_split(np.array(result), np.array(y_total), 
                                                      test_size=0.30, shuffle=True, 
                                                      random_state=42)

  train_images=W_train #imagens utilizadas para o treino
  train_labels=yw_train # resposta esperada para o treino
  test_images=W_test
  test_labels=yw_test
  

 
  knn.fit(train_images,train_labels)

  


  prediction = .predict(test_images)
  
  y_valor=np.copy(yw_test)
  data = {'y_Actual': y_valor,
          'y_Predicted': prediction
          }  # este dado esta no formato de dicionario

  df = pd.DataFrame(data, columns=['y_Actual','y_Predicted'])


  confusion_matrix = pd.crosstab(df['y_Actual'], df['y_Predicted'], rownames=['Actual'], colnames=['Predicted'])
  print(confusion_matrix)

  y_true = df['y_Actual']
  y_pred = df['y_Predicted']
  
  METRICS=sklearn.metrics.classification_report(y_true, y_pred)
  

  return y_pred,confusion_matrix,METRICS