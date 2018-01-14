#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from matplotlib import *
from offlineDataGenerator_avgRGB import *
from offlineDataGenerator_avgHSV import *
from offlineDataGenerator_ColorHistogram import *
from offlineDataGenerator_ColorLayout import *

import pickle
from Tkinter import *
from PIL import ImageTk, Image
import tkMessageBox
import tkFileDialog 
from ttk import Frame, Button, Label, Style
import numpy as np
from random import randint
from PIL import Image
import math
import csv

global imgs
global thumb
global thumb_mosaic
global baseImage
global fileList
global fileName

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
    
        
    def initUI(self):
        #title
        self.parent.title("HW4_Mosaic") 
        #pack_info
        self.pack(fill=BOTH, expand=1)
        #Button_SelectFile
        Button(self, text = "Select File", command = openFile).grid(row=0, column=0, pady=5)
        self.fileName = StringVar()
        Label(self, textvariable=self.fileName).grid(row=0, column=1, columnspan=2, pady=5, sticky=W)

        #Default_file
        self.fileName = StringVar(value = "./dataset/ukbench00000.jpg")
        # albl = Label(self, textvariable = self.fileName)
        # albl.grid(row=0, column=2, columnspan=3, pady=5, sticky=W)

        #Image_SelectedFile
        self.thumb = Label(self)
        self.thumb.grid(row=0, column=1, pady=5, sticky=W)
        image = Image.open(self.fileName.get())
        print image.size[0]
        print image.size[1]
        image = ImageTk.PhotoImage(image.resize((600, 450),Image.ANTIALIAS))
        self.thumb.configure(image = image)
        self.thumb.image = image

        self.thumb_mosaic = Label(self)
        self.thumb_mosaic.grid(row=0,column =3,pady=5, sticky=W)
        self.thumb_mosaic.configure(image = image)
        self.thumb_mosaic.image = image

        #mode_SelectMode
        Label(self, text = "Select Mode: ").grid(row=1, column=0, pady=5)
        mode = StringVar(self)
        #default
        mode.set("AVG_RGB")
        om = OptionMenu(self, mode, "Color_Layout", "Color_Histogram", "AVG_RGB","AVG_HSV")
        om.grid(row=1, column=1, pady=5, sticky=W)

        #mode_SelectDistanceAlgo.
        Label(self, text = "Select Distance Algorithm: ").grid(row=2, column=0, pady=5)
        distanceMode = StringVar(self)
        #default
        distanceMode.set("Euclidean_Distance")
        distanceOm = OptionMenu(self, distanceMode, "Euclidean_Distance", "Manhattan_Distance")
        distanceOm.grid(row=2, column=1, pady=5, sticky=W)

        #mode_selectCutGrids
        Label(self, text = "Cut Into n*n grids. n = ").grid(row=3, column=0, pady=5,sticky=W)
        self.grids =StringVar(value = "20")
        vcmd = (self.register(self.onValidate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.gridsTextField = Entry(self,textvariable = self.grids, width = 3, validate = 'key', validatecommand = vcmd)
        self.gridsTextField.grid(row=3, column=1, pady=1 ,sticky=W)
       
       #Button_START
        Button(self, text = "START", command = lambda: startSearching(self.fileName.get(), mode.get(), distanceMode.get(), int(self.gridsTextField.get()))).grid(row=4, column=0, pady=5)
        # self.imgs = []
        # #RankList
        # for i in xrange(10):
        #     self.imgs.append(Label(self))
        #     self.imgs[i].grid(row=i/5+4, column=i%5, padx=5, pady=10)


    def onValidate(self, d, i, P, s, S, v, V, W):
        return True if S in '1234567890' else False

 
 
def openFile ():
    fileName = tkFileDialog.askopenfilename(initialdir = "./dataset")
    app.fileName.set(fileName)
    image = Image.open(app.fileName.get())
    image = ImageTk.PhotoImage(image.resize((600, 450),Image.ANTIALIAS))
    app.thumb.configure(image = image)
    app.thumb.image = image
    app.thumb_mosaic.configure(image = image)
    app.thumb_mosaic.Image = Image

def startSearching (fileName, mode, distanceMode, grids):
    baseImage = Image.open(fileName)
    width ,height = baseImage.size
    fileList = os.listdir(fileName[:-16])
    fileName = fileName[-16:]
    csvName = ""
    formula = ""
    if mode == "AVG_RGB":
        csvName = "avg_RGB.csv"
        if distanceMode == "Euclidean_Distance":
            formula = avgRGB_Euclidean
        elif distanceMode == "Manhattan_Distance":
            formula = avgRGB_Manhattan

    elif mode == "AVG_HSV":
        csvName = "avg_HSV.csv"
        if distanceMode == "Euclidean_Distance":
            formula = avgHSV_Euclidean
        elif distanceMode == "Manhattan_Distance":
            formula = avgHSV_Manhattan

    elif mode == "Color_Layout":
        csvName = "ColorLayout.csv"
        formula = colorLayout_Euclidean

    elif mode == "Color_Histogram":
        csvName = "ColorHistogram.csv"
        formula = colorHistogram_Euclidean

    with open("./offlineData/" + csvName,'rb') as csvfile:
        Reader = csv.reader(csvfile)
        data = [row_ for row_ in Reader]

        blockW = width / grids
        blockH = height / grids
        output = Image.new('RGB',(blockW*grids,blockH*grids))
        for i in xrange(grids):
            for j in xrange(grids):
                blockBoundary = (i*blockW, j*blockH, (i+1)*blockW, (j+1)*blockH)
                imgCrop = baseImage.crop(blockBoundary)
                res = formula(imgCrop,data)
                print (' '*(3-len(str(i+1)))+str(i+1)+' x '+' '*(3-len(str(j+1)))+str(j+1) +' D = '+str(res[1]))
                print res[0]
                imgNew = Image.open("./dataset/" + res[0]).resize((blockW,blockH))
                output.paste(imgNew, blockBoundary)
    output.save("./product.jpg","JPEG",quality=85, optimize=True, progressive=True)


    img = Image.open("./product.jpg")
    image = ImageTk.PhotoImage(img.resize((600, 450),Image.ANTIALIAS))
    app.thumb_mosaic.configure(image = image)
    app.thumb_mosaic.image = image

    # print avg_RGB_Func(baseImage)
    # print avg_HSV_Func(baseImage)
    # # print Color_Histogram_Func(baseImage)
    # print Color_Layout_Func(baseImage)
    # print len(Color_Histogram_Func(baseImage)[0])
    # print len(baseImage.histogram())
    # if mode == "Q1-ColorHistogram":
    #     rank = Q1.Q1_run(baseImage,fileList)
  
    # elif mode == "Q2-ColorLayout":
    #     if os.path.exists("./offline/Q2_DCTData.csv"):
    #         rank = Q2.Q2_offline_run(fileName,fileList)
    #     else:
    #         rank = Q2.Q2_run(baseImage,fileList)


    # elif mode == "Q3-SIFT Visual Words":
    # 	if os.path.exists("./Q3.csv"):
    #         rank = Q3.Q3_offline_run(fileName,fileList)
    # elif mode == "Q4-Visual Words using stop words":
    #     if os.path.exists("./Q3.csv"):
    #         rank = Q4.Q4_offline_run(fileName,fileList)

    # for i in xrange(10):
    #     imgName = "./dataset/" + rank[i][1]
    #     image = Image.open(imgName)
    #     image = ImageTk.PhotoImage(image.resize((int(image.size[0]*0.8), int(image.size[1]*0.8)),Image.ANTIALIAS))
    #     app.imgs[i].configure(image = image)
    #     app.imgs[i].image = image
    #     print "Rank " + str(i+1) + " is number " + rank[i][1][7:-4] + ", distance is " + str(round(rank[i][0],3))

if __name__ == '__main__':
    root = Tk()
    size = 220, 220
    app = Example(root)
    root.geometry("2000x800")
    root.mainloop()
 

  