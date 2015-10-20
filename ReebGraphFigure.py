'''
-------------------------------------------------------------------------------------------
REEB GRAPH DEMO
This demo belongs to the paper 'A practial introduction to skeletons for the plant sciences'

The demo uses:
- the mahotas package (http://luispedro.org/software/mahotas)
- the numpy package (http://sourceforge.net/projects/numpy/)
- the scipy package (http://www.scipy.org/SciPy)

The code is free for non-commercial use.
Please contact the author for commercial use.

Please cite the paper if you use the code for your scientific project.

-------------------------------------------------------------------------------------------
Author: Alexander Bucksch
School of Biology and Interactive computing
Georgia Institute of Technology

Mail: bucksch@gatech.edu
Web: http://www.bucksch.nl

-------------------------------------------------------------------------------------------
Copyright (c) 2014 Alexander Bucksch
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above
    copyright notice, this list of conditions and the following
    disclaimer in the documentation and/or other materials provided
    with the distribution.

  * Neither the name of the Fiber Walk Demo Developers nor the names of its
    contributors may be used to endorse or promote products derived
    from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

#!/usr/bin/python

#use mahotas for reading the image
import mahotas as m
#import the image libary
from PIL import Image,ImageOps
#import pylab to show the image
from pylab import imshow
#import scipy and the ndimage data structure
from scipy import ndimage 
import scipy
# import numpy for standard numerical calculations
import numpy as np

# helper function to find closest neighbour 
# in the next level set in positive and negative directions along the last level set
def getClosestNb(avg):
    # distance and index negative direction
    negDist= 10000
    negRet = -1
    # distance and index positive direction
    posRet = -1
    posDist= -10000
    for idx,i in enumerate(lastAvg):
        if negDist > i-avg:
            negDist=i-avg
            negRet=idx
        if posDist < i-avg:
            posDist=i-avg
            posRet=idx
    
    return posRet,posDist,negRet,negDist

# read the image with mahotas as a grey image
img=m.imread('./BadRG.jpg',as_grey=True)
# read the image with mahotas again to obtain a color image where we can draw the ReebGraph in red (vertices) and green (edges)
imgColor2=m.imread('./BadRG.jpg')
# Threshhold to remove artifacts from the jpg compression
img=(img>100)
#get the dimensions of the image
x,y = np.shape(img)

# some storage arrays for the last line 
lastAvg=[]
# and the current averages of the contours
newAvg=[]

# loop over the whole image line by line is the discrete height function
# the white foreground pixels/True values in the image is the level set
for idx,i in enumerate(img):
    #flush the last contours 
    lastAvg=list(newAvg)
    #clear the current contours
    newAvg=[]
    #obtain the contours by using connected component labeling
    labeled, nr_objects = ndimage.label(i)

    xArr=[]
    
    #loop over the contours
    for jdx,j in enumerate(labeled):
        
        #collect all coordinates in the line if it belongs to the foreground
        if j>0: xArr.append(jdx)
        #if the background is startin (indicated by 0) take the avg of the collected foreground
        if j==0 and len(xArr)>0: 
            avg=np.mean(xArr)
            xArr=[]
            # draw the red pixel
            if img[idx,avg]==True:
                imgColor2[idx,avg]=(255,1,1)
                imgColor2[idx+1,avg]=(255,1,1)
                imgColor2[idx-1,avg]=(255,1,1)
                imgColor2[idx,avg+1]=(255,1,1)
                imgColor2[idx,avg-1]=(255,1,1)
                #draw edges if the distance is greater than one pixel to the last line
                labeled2, nr_objects2 = ndimage.label(img[idx-1])
                posIdx,posDist,negIdx,negDist=getClosestNb(avg)
                
                #Note: we use idx-2 in the condition below to compensate for little errors resulting from the thresholding of the jpg image. 
                # Theorethically 1 would be enough
                if posDist >1 and posIdx>=0:
                        if np.unique(img[idx+2,avg:avg+int(posDist)-1])[0]==True or np.unique(img[idx-2,avg:avg+int(posDist)-1])[0]==True: 
                            for l in range(0,int(posDist)):
                                if idx-l > 0 and idx+l < y:
                                    imgColor2[idx,avg+l]  =(1,255,1)
                                    imgColor2[idx+1,avg+l]=(1,255,1)
                                    imgColor2[idx-1,avg+l]=(1,255,1)
                                    imgColor2[idx,avg+l+1]=(1,255,1)
                                    imgColor2[idx,avg+l-1]=(1,255,1)
                if negDist <-1 and negIdx>=0:
                        if np.unique(img[idx-2,avg+int(negDist)+1:avg])[0]==True or np.unique(img[idx+2,avg+int(negDist)+1:avg])[0]==True:
                            for l in range(int(negDist),0):
                                    if idx-l > 0 and idx+l < y:
                                        imgColor2[idx,avg+l]  =(1,255,1)
                                        imgColor2[idx+1,avg+l]=(1,255,1)
                                        imgColor2[idx-1,avg+l]=(1,255,1)
                                        imgColor2[idx,avg+l+1]=(1,255,1)
                                        imgColor2[idx,avg+l-1]=(1,255,1)
                # collect the contours of the lines        
                newAvg.append(avg)


    
#save the image in the current directory                       
scipy.misc.imsave('./resultRG.jpg',imgColor2)
