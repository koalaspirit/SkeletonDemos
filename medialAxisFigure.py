'''
-------------------------------------------------------------------------------------------
REEB GRAPH DEMO
This demo belongs to the paper 'A practial intorduction to skeletons for the plant sciences'

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

#use mahotas for reading the image 
#and the medial axis calculation
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

# read the image with mahotas as a grey image
img=m.imread('./testimg4.jpg',as_grey=True)
# read the image with mahotas again to obtain a color image where we can draw the ReebGraph in red (vertices) and green (edges)
imgColor=m.imread('./testimg4.jpg')
# Threshhold to remove artifacts from the jpg compression
img=(img>100)
#get the dimensions of the image
x,y = np.shape(img)

#use the distance transform to obtain the distances per pixel of the medial axis
dmap = m.distance(img,metric='manhatten')
#use mathamatical morphology to obtain the medial axis (thinning function of mahotas)
skelImg=m.thin(img)

# draw the medial axis in the image
for idx,i in enumerate(skelImg):
    for jdx,j in enumerate(i):
        if skelImg[idx,jdx]==True:
            imgColor[idx,jdx]=(255,1,1)
            try:
                imgColor[idx+1,jdx]=(255,1,1)
            except:
                pass
            imgColor[idx-1,jdx]=(255,1,1)
            try:
                imgColor[idx,jdx+1]=(255,1,1)
            except:pass
            imgColor[idx,jdx-1]=(255,1,1)
            
#save the image in the current directory                    
scipy.misc.imsave('./resultMA.jpg',imgColor)
