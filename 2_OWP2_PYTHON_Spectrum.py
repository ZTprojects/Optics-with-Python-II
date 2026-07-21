import numpy as np
import matplotlib.pyplot as plt
plt.close('all')



def n(x, n_type):
    x = x/1000
    if n_type=='n_BK7' and np.all(0.3<=x) and np.all(x<=2.5):
        return (1+1.03961212/(1-0.00600069867/x**2)+0.231792344/
            (1-0.0200179144/x**2)+1.01046945/(1-103.560653/x**2))**.5
    #Conditions: 
    #Temperature = 293 °K
    #Wavelength range: 0.3um - 2.5um
    
    elif n_type=='n_FS' and np.all(0.21<=x) and np.all(x<=6.7):
        return (1+0.6961663/(1-(0.0684043/x)**2)+0.4079426/
        (1-(0.1162414/x)**2)+0.8974794/(1-(9.896161/x)**2))**.5
    #Conditions: 
    #Temperature = 293 °K
    #Wavelength range: 0.21um - 6.7um
    
    else:
        return 'Invalid input'



def plot(   *lines, title='', xlabel='', ylabel='', 
         xlim1 = None, xlim2 = None,
         ylim1 = None, ylim2 = None,
         fontsize=13, titlesize=15, legend=0, legLoc='upper right'   ):
    
    fig, ax = plt.subplots()
    
    for x, y, style, color, label in lines:    
        ax.plot(x, y, style, color=color,label=label)
    if legend==1:
        ax.legend(loc=legLoc)
        
    ax.grid()
    ax.set_title(title, fontsize=titlesize)
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    fig.tight_layout()
    
    
    
    if xlim1 is None:
        x1 = min(np.min(line[0]) for line in lines)

    if xlim2 is None:
        x2 = max(np.max(line[0]) for line in lines)
    
    if xlim2 is None and xlim1 is None:
        xmargin = (x2 - x1)*0.05
        xlim1 = x1-xmargin
        xlim2 = x2+xmargin
    
    if xlim1 is None and xlim2 is not None:
        xmargin = (xlim2 - x1)*0.05
        xlim1 = x1-xmargin

    if xlim2 is None and xlim1 is not None:
        xmargin = (x2 - xlim1)*0.05
        xlim2 = x2+xmargin
    
    ax.set_xlim(xlim1, xlim2)
    
    
    
    if ylim1 is None:
        y1 = min(np.min(line[1]) for line in lines)

    if ylim2 is None:
        y2 = max(np.max(line[1]) for line in lines)
    
    if ylim2 is None and ylim1 is None:
        ymargin = (y2 - y1)*0.05
        ylim1 = y1-ymargin
        ylim2 = y2+ymargin
    
    if ylim1 is None and ylim2 is not None:
        ymargin = (ylim2 - y1)*0.05
        ylim1 = y1-ymargin

    if ylim2 is None and ylim1 is not None:
        ymargin = (y2 - ylim1)*0.05
        ylim2 = y2+ymargin
    
    ax.set_ylim(ylim1, ylim2)
    
    
    
    return ax






"""(21)_<<<<<<<<<<<<<<<<<<<<<<<<_SPECTRUM_>>>>>>>>>>>>>>>>>>>>>>>>>>>>>_(21)"""
#Spectrum: A graphical representation of the relative intensities of the mono-
#chromatic spectral components of a light beam as a function of wavelength. The
#x-axis corresponds to the wavelength, and the y-axis corresponds to the spec-
#tral line intensity.

#Due to diffraction, spectrum lines have a y = (sin(x)/x)**2 shape. In the case
#of every spectrum line, there is a characteristic quantity called FWHM - Full
#Width at Half Maximum, which we use to describe the width of a spectral line.
#Visual demo: 2_OWP2_INKSCAPE_SincSquared.pdf.
x = np.arange(-15,15.1,0.1)
I_x = np.sinc(x/np.pi)**2   #np.sin(x)**2 / x**2 --> 0/0 is nan in python!
                            #np.sinc(x) = np.sin(x*np.pi)/x/np.pi
plot(   (x, I_x, '-', 'red',''), title = r'$sin(x)^2/x^2$ function',
     xlabel='x', ylabel=r'$I_x$')
#First (and higher order) minimums on the left and right sides: sin(x) = 0, 
#therefore x = m*Pi, where m >= 1 (there is a maximum at m=0).



#Now let's try determining the FWHM (dx):
#numpy.amax(a, axis=None, out=None, keepdims=<no value>, initial=<no value>,
#where=<no value>)
#Basically, this gives back the maximum value of a vector 'a'.

#numpy.argmax(a, axis=None, out=None)
#Similar to np.amax, but this gives back the index of the aformentioned value.

#np.amin and np.argmin: same, but these ones search for the minimums.



def FWHM(x, y, x1=None, x2=None):
    
    
    if x1 is not None and x2 is not None:
        y = y[np.argmin(np.abs(x-x1)):np.argmin(np.abs(x-x2))]
        x = x[np.argmin(np.abs(x-x1)):np.argmin(np.abs(x-x2))]
        
    elif x1 is not None and x2 is None:
        y = y[np.argmin(np.abs(x-x1)):]
        x = x[np.argmin(np.abs(x-x1)):]
        
    elif x1 is None and x2 is not None:
        y = y[:np.argmin(np.abs(x-x2))]
        x = x[:np.argmin(np.abs(x-x2))]

        
    y_max = np.amax(y)
    i_max = np.argmax(y)
    
    y_left = y[:i_max]
    y_right = y[i_max:]
    
    
    
    #The left side of the curve:
    i = np.argmin(np.abs(y_max/2-y_left))
    
    if np.isclose(y_left[i], y_max / 2, atol=1e-8):
        x_left = x[i]
    #a = 0.1 + 0.2
    #b = 0.3
    #print(a == b) -> (could be) False, because 'a' and 'b' are floats                      (because information technology is just modern day black magic),
    #thereore 0.1+0.2 could be 0.3000000000000004. The 'atol' argument deter-
    #mines the maximum absolute tolerance.
        
    elif y_left[i] > y_max / 2:
        x_left = (y_max/2-y_left[i-1]) / (y_left[i]-y_left[i-1]) * (x[i]-x[i-1])+x[i-1]
        
    elif y_left[i] < y_max / 2:
        i = i+1
        x_left = (y_max/2-y_left[i-1]) / (y_left[i]-y_left[i-1]) * (x[i]-x[i-1])+x[i-1]



    #The right side of the curve:
    i = np.argmin(np.abs(y_max/2-y_right))
    extra = i_max
    
    if np.isclose(y_right[i], y_max / 2, atol=1e-8):
        x_right = x[i+extra]
        
    elif y_right[i] > y_max / 2:
        x_right = (y_max/2-y_right[i-1]) / (y_right[i]-y_right[i-1]) * (x[i+extra]-x[i-1+extra])+x[i-1+extra]
        
    elif y_right[i] < y_max / 2:
        i = i+1
        x_right = (y_max/2-y_right[i-1]) / (y_right[i]-y_right[i-1]) * (x[i+extra]-x[i-1+extra])+x[i-1+extra]
    #Another way to write these:
    #x_l = x[:i_max]
    #x_r = x[i_max:]
    #This way we dont have to use the 'extra' variable!
    #if y_right[i] == y_max / 2:
    #    x_right = x_r[i]

    print("Peak wavelength:", x[np.argmax(y)])
    print("Peak intensity :", np.max(y))
    return x_right - x_left
#Note that in python, only the first true statement's actions will be completed
#in an individual if-elif-else chain. 


dx = FWHM(x, I_x)
print('dx:')
print(dx)   #You can use the cursor on the plots, and it will show you the x
            #and y values. One can use this to graphically check the validity
            #of the value obtained via the FWHM function.






"""(21)_<<<<<<<<<<<<<<<<<<<<<<_SPECTROMETER_>>>>>>>>>>>>>>>>>>>>>>>>>>>_(21)"""
#One type of instrument used to produce a spectrum is a spectrometer, in which 
#the incident light beam is dispersed by an optical dispersive element, such as
# a diffraction grating or a prism. We  will be discussing the former now.

#In the case of a reflective diffraction grating, the 0th order diffraction's
#angle will be the angle of incidence (this does not depend on the wavelength).

#Next to the 0th order, we canb see the 1st and -1st orders, which do depend on
#the wavelength of the incident light!
#Visual demo: 2_OWP2_INKSCAPE_DiffractionGrating.pdf.

#Usable spectral range: for example, the human eye's usable spectral range is
#between 400nm - 700nm, approximately. Depends on the detector and its sensi-
#tivity.

#Free Spectral Range: The wavelength interval within which wavelengths are dis-
#tinguishable unambiguously. In the case of prisms, it can be equal to the total
#spectral range. In the case of diffraction gratings this interval is limited
#by the overlapping of the different orders of the different wavelengths. For
#example, the 2nd order of a 400nm monochromatic light is where the 1st order 
#maximum is in the case of a 800nm monochromatic light.

#Reciprocal Linear Dispersion (kappa): describes the wavelength difference bet-
#ween 2 pixels on a detector. Its dimension is nm/pixel. Basically, the device
#and its pixels do not know what wavelength of light reaches a given pixel. All
#it sees are the 'counts' (basically photons eject an electron via the photo-
#electric effect. A higher amount of electrons ejected will result in a higher 
#analogue signal, which will be converted into integers using an ADC converter). 
#The device knows which pixel corresponds to which wavelength because it was 
#calibrated beforehand. This calibration depends on the parameters of the opti-
#cal elements a spectrometer uses and their positions.

#Rayleigh criterion: Two diffraction principal maxima corresponding to differ-
#ent wavelengths, λ1 and λ2, are considered resolvable if they are separated by
# at least one first-order minimum.
#Visual demo: 2_OWP2_INKSCAPE_RayleighCriterion.pdf.



I_x2 = np.sinc(   (x-np.pi)/np.pi   )**2

plot(   (x, I_x, '--', 'orange',''),
     (x, I_x2, '--', 'blue',''),
     (x, I_x + I_x2, '-', 'red',''),
     xlabel = 'x', ylabel='I(x)', title ='Rayleigh Criterion'   )



#It can be shown that the full width at half maximum (FWHM), expressed in wave-
#length units (δλ), of a spectral line produced by monochromatic light provides
#a good approximation to the wavelength difference Δλ given by the Rayleigh 
#criterion.

#Spectral transfer: The light source's spectrum changes on each optical 
#element of the spectrometer. tau_i(λ) is the transmissive/reflective factor of an
#optical element in terms of intensity, in which case the amplitude spectral
#transfer functions is: K(λ) = tau_1 * ... * tau_i * ... * tau_N * S(λ), where
#S(λ) is the sensitivity of the spectrometer's detector. The detected spectrum:
#I_d(λ) = K(λ) * I(λ) and therefore the actual spectrum can be calculated if we
#measure the spectrum (I_d) and if we know the amplitude transfer function:
#I = I_d / K. K can be determined by using a known spectrum, such as a black 
#body radiation.



#We are going to use the spectrum of a halogen lamp, which can be assumed to be
#emitting black body radiation. The file is originally from the univeristy 
#♀course Optics with Python II***.
wl, I_d = np.loadtxt('SPECTRUM0001.trt',
                   delimiter=';', skiprows = 8, unpack=True)#***

plot(   (wl, I_d, '-', 'red', ''),
     title="Halogen lamp's (7 W) apparent spectrum",
     xlabel='Wavelength [nm]', ylabel='Intensity [relative units]')



#Usable spectral range:
print(   'Usable spectral range interval: {0:0.1f}nm - {1:0.1f}nm.'.format(wl[0],
    wl[-1])   )



#Reciprocal linear dispersion at wl = 400nm, 600nm, 800nm.
i = [np.argmin(np.abs(400-wl)), np.argmin(np.abs(600-wl)),
     np.argmin(np.abs(800-wl))]
"""i_400 = np.argmin(   np.abs(400-wl)   )
i_600 = np.argmin(   np.abs(600-wl)   )
i_800 = np.argmin(   np.abs(800-wl)   )"""
k_400 = wl[i[0]+1]- wl[i[0]]
print(k_400)
k_600 = wl[i[1]+1]- wl[i[1]]
print(k_600)
k_800 = wl[i[2]+1]- wl[i[2]]
print(k_800)



#We have I_d, now let's calculate I!
h = 0.663               #aJ/fs, Planck-constant
k = 1.381*10**(-5)      #aJ/K, Boltzmann-constant
c = 299.792             #nm/fs, lightspeed in vacuum
T = 2800                #°K, temperature (given by manufacturer)


I = (8*np.pi*h*c**2/wl**5) * 1 / (np.exp(h*c/wl/k/T) - 1)
plot( (wl, I, '-', 'red',''),
     title="Ideal black body radiation at T = 2800°K",
     xlabel='Wavelength [nm]', ylabel='Intensity [W/$nm^3$]')
#There is a quite large discrepancy in where the maximum intensity can be
#found. This is because of the sensitivity of the detector.

#Note that the theory gives a dimension of W/nm**3, whereas the spectrometer
#gives relative units. There is a difference in dimensions.
K = I_d / I             #Not dimensionless! Count / (W/nm**3), shows us how 
                        #counts a device makes per intensity. This alone is a 
                        #sensible device parameter!
K = K / np.max(K)
#There, we get rid of the difference in dimensions, BUT! This way we lose in-
#formation about amplification! For example, if 1 kW makes 50000 counts or 25000
#counts, we will not be able to discover it from K alone. What information re-
#mains is about the shape of the transfer function! The shape shows on which 
#wavelengths the device is more sensitive, where it works well and where it does
#not. 

#The count value also depends on a lot of things, such as integration time, gain,
#the ADC converter, the coupling of the optical fiber, etc, and as such, it is a
#fickle thing! For example, if we increase the integration time from 10 ms to
#20 ms, the count value will also double, but our K value will not, so it is 
#(somewhat) independent from such parameters.



plot(   (wl, K, '-', 'red', ''),
     title="Transfer function",
     xlabel='Wavelength [nm]', ylabel='Transfer function [-]'   )







"""(22)_<<<<<<<<<<<<<<<<<<<<<_Hg-Cd SPECTRUM_>>>>>>>>>>>>>>>>>>>>>>>>>>_(22)"""
#Now let's capture the spectrum of a Hg-Cd lamp!
#The file is originally from the univeristy course Optics with Python II***.
wl_hgcd, I_d_hgcd = np.loadtxt('HGCD_sp.trt',
                   delimiter=';', skiprows = 8, unpack=True)#***

plot(   (wl_hgcd, I_d_hgcd, '-', 'red', ''),
     title="Hg-Cd lamp's apparent spectrum",
     xlabel='Wavelength [nm]', ylabel='Intensity [r.u.]'   )



#Now let's use the amplitude transfer function of the spectrometer to obtain 
#the actual spectrum!
I_hgcd = I_d_hgcd / K
plot(   (wl_hgcd, I_hgcd, '-', 'red', ''),
     xlim1=350, xlim2 = 700,
     ylim1=min(I_hgcd[:np.argmin(np.abs(wl_hgcd-700))])*0.95,
     ylim2=max(I_hgcd[:np.argmin(np.abs(wl_hgcd-700))])*1.05,
     title="Hg-Cd lamp's spectrum",
     xlabel='Wavelength [nm]', ylabel='Intensity [r.u.]'   )
#Note: there are divisions by 0! Because K is close to 0/is 0 in some indices,
#we get false peaks at some indices after the division!

#Search all the peaks between 360-700nm!
def max(x, y, x1=-np.inf, x2=np.inf, y1=-np.inf, y2=np.inf):
    maxList = []
    for i in range(1,len(x)-1):
        if x[i] >= x1 and x[i] <= x2:
            if y[i] >= y1 and y[i] <= y2:
                if y[i-1] < y[i] > y[i+1]:
                    maxList.append([i, x[i], y[i]])
    return maxList


maxes = max(wl_hgcd, I_hgcd, x1=360, x2=700, y1=4000)
for i in range(len(maxes)):
    print('Index = {0:0d}, λ = {1:0.2f}nm, I = {2:0.2f}'.format(maxes[i][0],
                                                                maxes[i][1],
                                                                maxes[i][2]))



#Let's check out the highest peak's FWHM at λ = 546.56nm!
print('FWHM = {0:0.2f}nm.'.format(FWHM(wl_hgcd, I_hgcd, x1 = 540, x2 = 555 )))

#Now calculate the resolution!
R = 546.56 / FWHM(wl_hgcd, I_hgcd, x1 = 540, x2 = 555 )
print('Resolution = {0:0.2f}'.format(R))

#There is a visible doublette at:
'''    Index = 652, λ = 577.54nm, I = 12770.87
       Index = 658, λ = 579.51nm, I = 13027.02'''
#The central λ is approximately 578nm. Using the previously calculated resolu-
#tion value, we can determine the smallest resolvable wavelength difference:
d_wl = 578 / R
print('Δλ = {0:0.2f}nm.'.format(d_wl))

#Can this resolve the doublette?
d_doublette = 579.51 - 577.54
print('Doublette width = {0:0.2f}nm.'.format(d_doublette))
#d_doublette >= d_wl => Yes, it can!
















