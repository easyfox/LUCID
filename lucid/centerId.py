# coding utf8
# Python libary with opencv for detection on structural biology loops


__author__ = "Etienne Francois"
__contact__ = "etienne.francois:esrf.fr"
__copyright__ = "2013, ESRF"


import opencv
import cv
import numpy
import pylab
import scipy.ndimage
from toolbox import displayCv,white_detect,erode,dilate,open_image,smooth,imgInfo2cvImage
import meshGen
import Image
import myutils as utils
import scipy.stats
from PyMca import SimpleMath


#================================================================================#
#          									 #
#                      Pretreatment for loop centering                           #
#   										 #
#================================================================================#


#Launch pretreatment of the image and the loop detection
def find_loop(imgInfo,showVisuals=False,zoom=0,testingProc = False,faceFindProc = False):
    
    """|

    :param imgInfo: Information about the input image. Two types allowed yet : Image path or Numpy array
    :type imgInfo: String or Numpy array
    :param showVisuals: Display for debug
    :type showVisuals: Boolean
    :param zoom: Zoom level
    :type zoom: uint
    :param faceFindProc: For face finding procedure
    :type faceFindProc: Boolean
    :param testingProc: For testing procedure.
    :type testingProc: Boolean

    :returns: Return from loop detection (label,x,y). If it is a testing procedure, the return format is different (imageWidth, imageHeight, [loop detection function common return])

    """

    #Test what type of image data has been given as argument "imgInfo"
    img = open_image("reference.png") 
    if isinstance(imgInfo,numpy.ndarray):       
        im = imgInfo
    elif isinstance(imgInfo,str):
        #Treatment with the path of the image
        im = img2float(imgInfo)
    else:
        #Lauch TypeError exception if none type of image data supported is given
        raise TypeError("Unsupported type : Image path (str) or numpyarray (numpy.ndarray) needed")

    #Choose between differents ways of launching. Priority order : Normal, Face finding, TestCase procedure.
    if testingProc == False and faceFindProc == False:
        if zoom>0:
            return loop_detection(im,showVisuals,zoom)
        else:
            return loop_detection(im,showVisuals,zoom)
    elif faceFindProc == True:
        return face_detection(im,0,zoom)
    else:
        #TestCase procedure launcher : return format is different (imageWidth, imageHeight, [function common return])
        if zoom>0:
            return (im.shape[1],im.shape[0],loop_detection(im,zoom=zoom))
        else:
            return (im.shape[1],im.shape[0],loop_detection(im,zoom=zoom))


# Explicit launcher for face finding with pretreatment of the image and the face detection
def find_face(imgInfo,showVisuals=False,zoom=0):
    """|

    :param imgInfo: Information about the input image. Two types allowed yet : Image path or Numpy array
    :type imgInfo: String or Numpy array
    :param showVisuals: Display for debug
    :type showVisuals: Boolean
    :param zoom: Zoom level
    :type zoom: uint

    :returns: Return from loop detection.

    """
    return find_loop(imgInfo,showVisuals=showVisuals,zoom=zoom,faceFindProc=True)


#================================================================================#
#          									 #
#                      Center identifier procedure                               #
#   										 #
#================================================================================#


#Detection of loops in image
def loop_detection(imgInfo,showVisuals=False,zoom=0):

    """|

    :param imgInfo: Information about the input image. Two types allowed yet : Image path or Numpy array
    :type imgInfo: String or Numpy array
    :param showVisuals: Display for debug
    :type showVisuals: Boolean
    :param zoom: Zoom level
    :type zoom: uint

    :returns: (label,x,y) result from loop_detection function

    """
    im=imgInfo
    im = im[1:-1,1:-2]

    #miror for edge effect
    im = utils.expand(im,2,mode="mirror")

    #Low pass filter with FFT
    shape = im.shape
    mask = gaussian_mask((495,660),.5,.5,4)

    i1f = numpy.fft.fft2(im)
    i2f = numpy.multiply(i1f,mask)
    res = numpy.fft.ifft2(i2f)

    #Sub the background
    test = im-res.real

    #Save img for checking
    #pylab.imsave("/users/efrancoi/afterFFT.png",test)

    #Sobel filter
    imgnumpy = test

    dx = scipy.ndimage.sobel(imgnumpy,axis=0,mode='reflect')  # horizontal derivative
    dy = scipy.ndimage.sobel(imgnumpy,axis=1,mode='reflect')  # vertical derivative
    mag = numpy.hypot(dx,dy)  # magnitude

    #True img
    mag = mag[2:-2,2:-2]

    #threshold to get the edge found with sobel
    mag=scipy.stats.threshold(mag,15,255)
    mag=scipy.stats.threshold(mag,0,14,255)

    #Noise deletion
    mag = scipy.ndimage.morphology.binary_erosion(mag)
    mag = scipy.ndimage.morphology.binary_erosion(mag)
    mag = scipy.ndimage.morphology.binary_dilation(mag)
    mag = scipy.ndimage.morphology.binary_dilation(mag)
     
    mag=numpy.uint8(mag)

    #pylab.imsave("/users/efrancoi/essaiblabla2.png",mag,cmap=pylab.cm.Greys_r)

    newImage = numpy.zeros_like(mag)
    newImageTemp = numpy.zeros_like(mag)

    #zone scan
    n = (mag.shape)[1]-1
    while n>=0:
        if numpy.mean(mag[:,n])>0:
            newImage[:,n]=0
            break                         
        n-=1
    lst_seq = [[]]
    seq_num=0
    last_white = True
    while n>=0:
        nznp = numpy.nonzero(mag[:,n])[0]
        if len(nznp>0):
            last_white=True
            lst_seq[seq_num].append((nznp[0],n))
            lst_seq[seq_num].append((nznp[-1],n))
        else:
            if last_white == True:
                lst_seq.append([])
                seq_num+=1
                last_white=False
        n-=1
    ans = map(len, lst_seq)
    lst_final = lst_seq[ans.index(max(ans))]
    
    for points in lst_final:
        newImage[points]=255

    n = (newImage.shape)[1]-1
    while n>=0:
        
        if numpy.mean(newImage[:,n])>0:
            mag[:,n+1:]=0
            break                         
        n-=1
    
    n=0
    while n<((newImage.shape)[1]-1):
        if numpy.mean(newImage[:,n])>0:
            mag[:,:n]=0
            break                         
        n+=1



    n = (mag.shape)[0]-1
    while n>=0:
        if numpy.mean(mag[n,:])>0:
            newImage[n,:]=0
            break                         
        n-=1
    lst_seq = [[]]
    seq_num=0
    last_white = True
    while n>=0:
        nznp = numpy.nonzero(mag[n,:])[0]
        if len(nznp>0):
            last_white=True
            lst_seq[seq_num].append((n,nznp[0]))
            lst_seq[seq_num].append((n,nznp[-1]))
        else:
            if last_white == True:
                lst_seq.append([])
                seq_num+=1
                last_white=False
        n-=1
    ans = map(len, lst_seq)
    lst_final = lst_seq[ans.index(max(ans))]

    #print 'lst_seq 2', lst_final
    
    for points in lst_final:
        newImage[points]=255
        newImageTemp[points]=255

    n = (newImageTemp.shape)[0]-1
    while n>=0:
        if numpy.mean(newImageTemp[n,:])>0:
            mag[n+1:,:]=0
            newImage[n+1:,:]=0
            break                         
        n-=1
    
    n=0
    while n<((newImageTemp.shape)[0]-1):
        if numpy.mean(newImageTemp[n,:])>0:
            mag[:n,:]=0
            newImage[:n,:]=0
            break                         
        n+=1
    
    #scan for profiling
    lendif = []
    n = (newImage.shape)[1]-1
    while n>=0:
        nznp = numpy.nonzero(mag[:,n])[0]
        if len(nznp>0):
            newImage[nznp[0]:(nznp[-1]+1),n]=255
            lendif.append(nznp[-1]-nznp[0])
        n-=1
    nbPix = numpy.sum(newImage)/255
    if nbPix<20:
        return ("No loop detected",-1,-1)

    #derivate and prifle smoothing
    lendif2 = scipy.ndimage.gaussian_filter(lendif, sigma=15.0, order=0)
    sm=SimpleMath.SimpleMath()
    deriv=sm.derivate(range(len(lendif2)), lendif2)
    deriv2 = scipy.ndimage.gaussian_filter(deriv[-1], sigma=3, order=0)
    
    #analize profile
    centerValue = profileAnalyzer(deriv2)
    
    #get coord of center    
    x=0
    y=0
    m=0
    n = (newImage.shape)[1]-1
    while n>=0:
        nznp = numpy.nonzero(mag[:,n])[0]
        if len(nznp>0):
            if m==(centerValue):
                newImage[:,n]=150
                nznp = numpy.nonzero(mag[:,n])[0]
                y = nznp[0]+(nznp[-1]-nznp[0])//2
                newImage[y,:]=150
                x = n
            m+=1
        n-=1

    #pylab.imsave("/users/efrancoi/essaiblablamask.png",newImage,cmap=pylab.cm.Greys_r)

    return ("Coord",int(x),int(y))

#Detection of loop with the meshing systeme
def find_loop_mesh(imgInfo,showVisuals=False,zoom=0,virtCenter=(-1,-1)):
    
    """|
    
    :param imgInfo: Information about the input image. Two types allowed yet : Image path or Numpy array
    :type imgInfo: String or Numpy array
    :param showVisuals: Display for debug
    :type showVisuals: Boolean
    :param zoom: Zoom level
    :type zoom: uint
    :param virtCenter: A virtual center if reqal center use is not wanted
    :type virtCenter: Tuple (uint,uint)

    :returns: (label,x,y) result from loop_detection function

    """
    if showVisuals:
        (x,y,x2,y2),imageClone,image3,store,virtCenter = meshGen.generate_meshing_info(imgInfo,method=meshGen.LUCID_CENTER_PROC,showVisuals=showVisuals,zoom=zoom,virtCenter=virtCenter)
        cv.Rectangle(imageClone,(x,y),(x2,y2),cv.Scalar( 120, 120, 120 ))
    else:
        (x,y,x2,y2),image3 = meshGen.generate_meshing_info(imgInfo,method=meshGen.LUCID_CENTER_PROC,showVisuals=showVisuals,zoom=zoom,virtCenter=virtCenter)
   
    xres = x2-((x2-x)//2)
    yrestemp = -1
    yrestemp2 = -1
    yres = 0
    while y<y2 and (yrestemp < 0 or yrestemp2 < 0):
        y+=1
        y2-=1
        if image3[y,xres]>0:
            yrestemp = y
        if image3[y2,xres]>0:
            yrestemp2 = y2
    if y>=y2:
        yres = y2-((y2-y)//2)
    else:
        yres = yrestemp2 - ((yrestemp2-yrestemp)//2)
    if showVisuals:
        for num in range(len(store)):
            cv.Line(image3,virtCenter,store[num],cv.Scalar(120,120,120),2,8)
        cv.Line(imageClone,(xres-3,yres-3),(xres+3,yres+3),cv.Scalar(120,120,120),2,8)
        cv.Line(imageClone,(xres-3,yres+3),(xres+3,yres-3),cv.Scalar(120,120,120),2,8)
        cv.Line(imageClone,(virtCenter[0],virtCenter[1]-3),(virtCenter[0],virtCenter[1]+3),cv.Scalar(120,120,120),2,8)
        cv.Line(imageClone,(virtCenter[0]-3,virtCenter[1]),(virtCenter[0]+3,virtCenter[1]),cv.Scalar(120,120,120),2,8)
        #real center
        cv.Line(imageClone,((659//2),(463//2)-15),((659//2),(463//2)+15),cv.Scalar(120,120,120),2,8)
        cv.Line(imageClone,((659//2)-15,(463//2)),((659//2)+15,(463//2)),cv.Scalar(120,120,120),2,8)

        displayCv(('Resultat',imageClone),('RaysVisu',image3))
        cv.WaitKey(0)
    return "meshing",xres,yres
    
#Detection of degrees for the face's loop in image
def face_detection(imgInfo,showVisuals=False,zoom=0):
    
    """|
    
    :param imgInfo: Information about the input image. Two types allowed yet : Image path or Numpy array
    :type imgInfo: String or Numpy array
    :param showVisuals: Display for debug
    :type showVisuals: Boolean
    :param zoom: Zoom level
    :type zoom: uint

    :returns: (label,x,y) result from loop_detection function

    """ 

    image=imgInfo2cvImage(imgInfo)

    image2=cv.CloneImage(image)
    if zoom == 0:
        cv.AdaptiveThreshold(image2,image2,255,cv.CV_ADAPTIVE_THRESH_MEAN_C,cv.CV_THRESH_BINARY_INV,45,6)
    else:
        cv.AdaptiveThreshold(image2,image2,255,cv.CV_ADAPTIVE_THRESH_MEAN_C,cv.CV_THRESH_BINARY_INV,121,6)

    image3=cv.CloneImage(image2)
    cv.Zero(image3)

    storage = cv.CreateMemStorage()
    contours = cv.FindContours(cv.CloneImage    
    (image2),storage,cv.CV_RETR_EXTERNAL,cv.CV_CHAIN_APPROX_SIMPLE,(0,0))

    cv.DrawContours(image3,contours,cv.RGB(255,255,255),cv.RGB (255,255,255),2,cv.CV_FILLED)
    cv.Smooth(image3,image3,cv.CV_MEDIAN,11)
    
    image4 = cv.CloneImage(image3)

    if zoom == 0:
        erode(image4,image4,9)
        dilate(image4,image4,9)
    else:
        erode(image4,image4,25)
        dilate(image4,image4,25)


    count = white_detect(image4)

    if showVisuals:  
        displayCv(('Resultat',image),('ErosionDilation',image4),('AdaptiveThresh',image2),('FinalTreatmentVisualisation',image3))
        cv.WaitKey(0)
    return count

def gaussian_mask(shape,sigma,sigma2,mulsigma):

    h = numpy.zeros(shape[0])
    w = numpy.zeros(shape[1])

    h[(shape[0]//2)-(mulsigma*sigma):(shape[0]//2)+(mulsigma*sigma)]=1
    w[(shape[1]//2)-(mulsigma*sigma2):(shape[1]//2)+(mulsigma*sigma2)]=1

    b1 = scipy.ndimage.filters.gaussian_filter(h,sigma)
    b2 = scipy.ndimage.filters.gaussian_filter(w,sigma)

    h0 = numpy.empty_like(b1)
    h1 = numpy.empty_like(b2)

    h0[:shape[0] // 2] = b1[shape[0] - shape[0] // 2:]
    h0[shape[0] // 2:] = b1[:shape[0] - shape[0] // 2]
    h1[:shape[1] // 2] = b2[shape[1] - shape[1] // 2:]
    h1[shape[1] // 2:] = b2[:shape[1] - shape[1] // 2]

    g = numpy.outer(h0,h1)
    return g


def profileAnalyzer(deriv2):
    slowCount = 0
    maxValue = 0.0
    centerValue = 20
    ival=0
    maxDeriv=0
    firstIndex=0
    littleLoop=-1
    if float(len(deriv2[deriv2>0.5]))/float(len(deriv2))>0.4:        
        while ival<len(deriv2):      
            val = deriv2[ival]        
            if val>0.5:
                centerValue=ival
                break
            ival+=1
    else:
        while ival<len(deriv2):      
            val = deriv2[ival]        
            if val>deriv2[(ival+1)%len(deriv2)] and val>deriv2[(ival+2)%len(deriv2)] and val>deriv2[(ival+3)%len(deriv2)] and val>deriv2[(ival+4)%len(deriv2)] and val>deriv2[(ival+5)%len(deriv2)]:
                maxDeriv = val
                break
            ival+=1
        firstIndex = ival
        if firstIndex==0:
            firstIndex=1
        while ival<len(deriv2):     
            val = deriv2[ival]
            if val<0.3 and val>0:
                slowCount+=1        
            elif val<=0.0:
                maxValue = ival
                #print deriv2[ival]
                if numpy.mean(deriv2[ival:ival+ival])<0.0:
                    centerValue = maxValue
                    break
            else:
                slowCount=0
            #print (ival-slowCount)-firstIndex,";",slowCount,";",ival
            if (slowCount >= (ival-slowCount)/2) and maxDeriv>0.3:    
                centerValue=ival-slowCount
                break
            elif (ival-slowCount)-firstIndex<=0 and float(len(deriv2))/float(slowCount+firstIndex)<8 and maxDeriv<0.3 and littleLoop<0:
                littleLoop=firstIndex
            ival+=1
        #print littleLoop,max(deriv2[:centerValue])
        if littleLoop>0 and max(deriv2[:centerValue])>2:
            centerValue = littleLoop
    return centerValue

def img2float(fn):
    im = Image.open(fn)
    im2=im.convert("F");nim = numpy.fromstring(im2.tostring(),dtype="float32")
    nim.shape = im.size[1],im.size[0]
    return nim
