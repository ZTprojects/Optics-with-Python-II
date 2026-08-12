import numpy as np
import matplotlib.pyplot as plt
import myfuncs as mf
plt.close('all')








"""(31)_<<<<<<<<<<<<<<<<<<_USABLE SPECTRAL RANGE_>>>>>>>>>>>>>>>>>>>>>>_(31)"""
print("\n\n(31)_USABLE SPECTRAL RANGE_(31)")
#Visual demo: 4_OWP2_INKSCAPE_TransmissionGratingSpectrometer.pdf and
#4_OWP2_INKSCAPE_UsefulSpectralRange.pdf
#For formulae, check the OWP2_LATEX_FORMULAE LaTeX file.

#Let's check the angular dispersion for a transmissive grating where the angle
#of incidence is perpendicular.
wl = np.arange(400, 700.1, 0.1)
N = 200#1/mm
N = N / 10**6

beta=np.arcsin(N*wl)
mf.plot(   (wl, np.rad2deg(beta), '-', 'r'),
        xlabel="Wavelength [nm]", ylabel="Angle of diffraction [°]",
        title="β(λ)"   )
#We can see that delta beta is smaller than 4°, so the approximation can be 
#used.
#An approximation for the angular dispersion using the start and end points of
#the plot:
ad = (   beta[-1] - beta[0]   ) / (700 - 400)
print("Angular dispersion [mrad/nm] = {0:0.4f}".format(ad*1000))



#Via numerical derivation at 550nm:
ad = np.gradient(   beta, wl   )
print("Angular dispersion [mrad/nm] at 550nm = {0:0.4f}".format(ad[np.argmin(np.abs(wl-550))]*1000))

mf.plot(   (wl, ad, '-', 'r'),
        xlabel="Wavelength [nm]", ylabel="Angular dispersion [mrad/nm]",
        title="δβ/δλ"   )
#The approximation was valid.



#Let's calculate the USR (Usable Spectral Range) for a transmission grating
#spectrometer!
nc = 640
p = 6000#nm
f=58 * 10 ** 6#nm
wl0 = 550#nm the central wavelength that reaches the center of the CMOS chip. 
#This is where we will calculate the AD.
usr = (   nc*p   ) / (   f*ad[np.argmin(np.abs(wl-wl0))]   )
print("USR [nm]: {0:0.2f}".format(usr))



#Calculate the reciprocal linear dispersion!
k_avg = usr / nc
print("Average reciprocal linear dispersion [nm/pixel]: {0:0.2f}".format(k_avg))








"""(32)_<<<<<<<<<<<<<<<<<<_DETECTOR: CMOS CHIP_>>>>>>>>>>>>>>>>>>>>>>>>_(32)"""
print("\n\n(32)_DETECTOR: CMOS CHIP_(32)")
#Visual demo: 4_OWP2_INKSCAPE_CMOSChip.pdf
#In the system that is assumed to be used here, - a CMOS chip - there are small
#squares, each of which is a photodetector. On each detector, there is a filter
#that only transmits a small range of wavelength (red, green, blue), and these
#transmitted rays reach the detector. This is how only a single colour is recor-
#ded. 

#As a result of this, these "mosaic" sensors capture 25% of the red,
#25% of the blue and 50% of the green incoming light.

#When we convert an RGB picture into a gray toned picture, the conversion looks
#like this:
# = 0.299*I_R + 0.587*I_G + 0.114*I_B

#Let's load and convert an RGB image into a gray toned one and examine it!
#The file is originally from the university course Optics with Python II***.
img = plt.imread('HgCd_sp_TG.jpg')#***
print('Size of the RGB picture:',img.shape)      
#pixelcount_y, pixelcount_x, number of colour channels
#Let's plot this!
plt.figure(figsize=(12,8))
plt.xlabel("Column indices")
plt.ylabel("Line indices")
plt.title("RGB image of a Hg_Cd lamp")
plt.tight_layout(pad=4)
plt.imshow(img)



#Convert the RGB image into a gray toned one!
factors = [0.299, 0.587, 0.114]     #The factors, as mentioned earlier.
im = np.dot(img, factors)           #scalar product with factors   
#example: b = [[1, 2, 3], [4, 5, 6]], then np.dot(b, factors)[0] = 
#b[0][0]*factors[0] + b[0][1]*factors[1] + b[0][2]*factors[2].
#Notice how this reduced the dimension count!

print('Size of the gray toned picture:',im.shape)  
#There is only 1 colour channel! 

#Now check the img and im variables in the variable explorer!
#The im shows the scalar intensity values of the image for every pixel in the
#table!

#If you look at the img variable, then you see only 3 columns at first. This is 
#because the variable explore only presents the table in 2D. Notice the Axis
#and Index descriptions below the table and try changing the values associated
#with them!

#The img variable has a shape like this: img[y, x, 3]!
#If Axis = 0, then you are locked onto the y axis, and by altering the Index
#values, you change which y you are looking at.

#Example 1: Axis=0, Index=500, then you are looking at the RGB vector of the
#HORIZONTAL LINE of y[500], so you have a table of dimension 3*640.

#Example 2: Axis=1, Index=400, then you are looking at the RGB vector of the
#VERTICAL LINE of x[400], so you have a table of dimension 3*480.

#Example 3: Axis=2, Index=2, then you are looking at the "blue values" of the
#ENTIRE PICTURE, pixel by pixel, so you have a table of dimension 640*480.

#im has only 1 colour channel, so you can immediately see the entire picture
#pixel by pixel without having to adjust anything in the variable explorer!



hlines = im.shape[0]    #480 horizontal lines!
vlines = im.shape[1]    #640 vertical lines!
#...and there is only 1 colour channel!
plt.figure(figsize=(12,8))
plt.xlabel("Column indices")
plt.ylabel("Line indices")
plt.title("Gray toned image of a Hg_Cd lamp")
plt.tight_layout(pad=4)
plt.imshow(im, cmap="gray")      #cmap="gray" tells the program to show a gray 
                                 #picture based on the intensity values!


plt.figure(figsize=(12,8))
plt.xlabel("Column indices")
plt.ylabel("Line indices")
plt.title("Blue toned image of a Hg_Cd lamp")
plt.tight_layout(pad=4)
plt.imshow(im, cmap="Blues")     #It doesn't have to be gray toned. Suit yourself!



#Now we will pick out one of the brighter horizontal lines to study!
i0 = 235
j = np.arange(0, vlines, 1)
I = im[i0,:]    #i0: the horizontal line, ":": everything from the other set!
                #This will have a dimension of 640.
mf.plot(   (j, I, '-', 'red', {"label":str(i0)+". line"}),
            xlabel="Column indices", ylabel="Intensity [r.u]",
            title="Spectrum of a Hg_Cd lamp",
            legend=1, legLoc="upper right"   )








"""(33)_<<<<<<<<<<_SPECTROMETER'S WAVELENGTH CALIBRATION_>>>>>>>>>>>>>>_(33)"""
print("\n\n(33)_SPECTROMETER'S WAVELENGTH CALIBRATION_(33)")
#Let's check the peaks!
peaks = mf.maxList(j, I, y1=50)
for i in range(len(peaks)):
    print(   f"Index: {peaks[i][0]:d},      Intensity: {peaks[i][2]:0.2f}"  )



#Now we need to check a database for the wavelength peaks and calibrate!
wl_peaks = np.array(   [435.83350, 467.81493, 479.99123, 508.58217, 546.07500,
                          576.96100, 579.06700, 643.84695]   )
mf.plot(   (   [p[0] for p in peaks]   , wl_peaks, 'o', 'r'),
            xlabel="Column index", ylabel="Wavelength [nm]",
            title="Wavelength calibration")



#Now the calibration may begin:
peaks = np.array(peaks)     #this is so that we can use the indexing peaks[:,0]!
                            #peaks[:,0] does not work if "peaks" is a list!
coeff = np.polyfit(   peaks[:,0], wl_peaks, 1)



calLine = 0
for i in range(len(coeff)):
    calLine = calLine + peaks[:,0] ** i * coeff[len(coeff)-i-1]  



mf.plot(   (   [p[0] for p in peaks]   , wl_peaks, 'o', 'r', {"label":"From database"}),
            (  [p[0] for p in peaks], calLine, '-', 'b', {"label":"Calibration"}),
            xlabel="Column index", ylabel="Wavelength [nm]",
            title="Wavelength calibration", legend=1, legLoc="upper left")


#The reciproc linear dispersion via the calibration line:
print(f"Reciproc linear dispersion using the calibration: {coeff[0]:0.2f} nm/pixel")

#If we look at index = 0, which is the first pixel, then:
print(f"The smallest possible value of λ: {coeff[1]:0.2f} nm.")

#If the index is 640, then we get the maximum:
print(f"The greatest possible value of λ: {calLine[-1]:0.2f} nm.")

#And so, the usable spectral range:
print(f"Thus, the USR is: {coeff[0]*vlines:0.2f} nm.")

#All these values are close to the previous ones!

#Check the difference between the calibration and database points!
diff = wl_peaks - calLine

mf.plot(   (   [p[0] for p in peaks]   , diff, 'o', 'r'),
            xlabel="Column index", ylabel="Wavelength difference [nm]",
            title="Calibration error")



#There seems to be a parabolics tendency... Fix it!
coeff = np.polyfit(   peaks[:,0], wl_peaks, 2)

calLine = 0
for i in range(len(coeff)):
    calLine = calLine + peaks[:,0] ** i * coeff[len(coeff)-i-1]  

diff = wl_peaks - calLine

mf.plot(   (   [p[0] for p in peaks]   , diff, 'o', 'r'),
            xlabel="Column index", ylabel="Wavelength difference [nm]",
            title="Calibration error with a 2nd degree polynomial")



#Let's soar even higher!
coeff = np.polyfit(   peaks[:,0], wl_peaks, 3)

calLine = 0
for i in range(len(coeff)):
    calLine = calLine + peaks[:,0] ** i * coeff[len(coeff)-i-1]  

diff = wl_peaks - calLine

mf.plot(   (   [p[0] for p in peaks]   , diff, 'o', 'r'),
            xlabel="Column index", ylabel="Wavelength difference [nm]",
            title="Calibration error with a 3rd degree polynomial")








"""(34)_<<<<<<<<<<<<<<<<<<<<_FWHM OF THE PEAKS_>>>>>>>>>>>>>>>>>>>>>>>>_(34)"""
print("\n\n(34)_FWHM OF THE PEAKS_(34)")

wl=0
for i in range(len(coeff)):
    wl += j ** i * coeff[len(coeff)-1-i]
mf.plot(   (wl, I, 'o', 'red', {"label":str(i0)+". line"}),
            (wl, I, '--', 'blue', {"label":str(i0)+". line"}),
            xlabel="Column indices", ylabel="Intensity [r.u]",
            title="Spectrum of a Hg_Cd lamp as a function of wavelength!",
            legend=1, legLoc="upper right"   )


threePeaks = [435, 546, 643]
fwhmPeaks = []
for i in range(len(threePeaks)):
    fwhmPeaks.append(mf.FWHM(wl, I, x1=threePeaks[i]-3, x2=threePeaks[i]+3 ))








"""(35)_<<<<<<<<<<<<<<<<<<<<<<<<_NA SPECTRUM_>>>>>>>>>>>>>>>>>>>>>>>>>>_(35)"""
print("\n\n(35)_NA SPECTRUM_(35)")
#The file is originally from the university course Optics with Python II***.
img = plt.imread('Na_sp_TG.jpg')#***

fig, ax = plt.subplots()
ax.set_xlabel('Column index')
ax.set_ylabel('Line index')
ax.set_title('Na spectrum')
ax.imshow(img)



#This will be as a function fo wavelength... NOTE that this assumes a linear
#dependence of lambda on pixel count!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
fig, ax1 = plt.subplots()
ax1.set_xlabel('Wavelength [nm]')
ax1.set_ylabel('Line index')
ax1.set_title('Na spectrum')
ax1.imshow(
    img,
    extent=[
        wl[0],              #x starting point
        wl[-1],             #x end point
        img.shape[0],       #y starting point
        0                   #y end point
    ],
    aspect='auto'
)



im = np.dot(img, factors) 
I = im[i0,:]
ax2 = ax1.twinx()
ax2.plot(wl, I, 'r--', label = str(i0) + '. line')
ax2.set_ylabel('Intensity [r.u.]')
ax2.legend(loc='upper right')
#The discrepancy could be because the calibration is not linear, but the picture
#of the Na's spectrum assumes it to be so. A simple workaround is to keep using
#the pixels for the x axis:
fig, ax1 = plt.subplots()
ax1.set_xlabel('Column index')
ax1.set_ylabel('Line index')
ax1.set_title('Na spectrum')
ax1.imshow(img, aspect="auto")      #aspect="auto" is needed, otherwise when one
                                    #zooms into the picture, the quality deterio-
                                    #rates. Maybe without this we get a regular
                                    #zoom onto the screen, but with it, it fills
                                    #the screen with the actual pixels and their
                                    #coloured brightness values.



im = np.dot(img, factors) 
I = im[i0,:]
ax2 = ax1.twinx()
ax2.plot(j, I, 'r--', label = str(i0) + '. line', linewidth=0.5)
ax2.set_ylabel('Intensity [r.u.]')
ax2.legend(loc='upper right')



plt.figure()
plt.xlabel('Column index')
plt.ylabel("Line index")
plt.title("Gray toned spectrum of the Na lamp")
plt.imshow(im, cmap='gray')



ax=mf.plot(   (wl, I, 'o', 'r', {"label":str(i0)+". line"}),
               (wl, I, '--', 'b'),
            xlabel="Wavelength [nm]", ylabel="Intensity [r.u]",
            title = "Na spectrum", legend=1,legLoc="upper right",
            xlim1=580,xlim2=595)
ax.axhline(max(I)/2)


a=mf.maxList(wl,I,y1=60)[0][1]
print(f"The peak of the Na spectrum: {a:0.2f} nm.")
#There is supposed to be a doublette where the Na peak is, but we do not see it!
#Considering that the wavelength difference between the 2 peaks is 0.6 nms, and
#the smallest resolvable wavelength according to 2_OWP2_PYTHON_Spectrometer is
#1.96 nm, so there should be no surprise here.


































