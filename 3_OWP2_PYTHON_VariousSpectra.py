import numpy as np
import matplotlib.pyplot as plt
import myfuncs as mf
plt.close('all')






"""(23)_<<<<<<<<<<<<<<<<_ENERGY EFFICIENT LIGHT BULB_>>>>>>>>>>>>>>>>>>_(23)"""
#Let's take a look at the aparent spectrum of an energy-efficient light-bulb!
#The file is originally from the university course Optics with Python II***.
print("\n\n(23)_ENERGY EFFICIENT LIGHT BULB_(23)")
I_d_ee = np.loadtxt('ENERGT_sp.trt', delimiter=';', skiprows=8,
                           unpack=True)[1]#***

wl, I_ee = mf.calib(I_d_ee)

mf.plot(   (wl, I_ee, '-','red'),
        xlabel='Wavelength [nm]', ylabel='Intensity [r.u.]',
        title="Energy-efficient light bulb's real spectrum",
        xlim2 = 700)

#Now check the peaks!
max_ee = mf.maxList(   wl, I_ee, x1=np.min(wl), x2=700, y1=6460)




for i in range(len(max_ee)):
    print('Index = {0:0d}, λ = {1:0.2f}nm, I = {2:0.2f}'.format(max_ee[i][0],
                                                                    max_ee[i][1],
                                                                    max_ee[i][2]))
    
    
    
#The results are similar to the spectrum of the Hg-Cd lamp, so compare them!
#The file is originally from the university course Optics with Python II***.
I_hgcd = np.loadtxt('HGCD_sp.trt', delimiter=';', skiprows=8, unpack=True)[1]#***
I_hgcd = mf.calib(I_hgcd)[1]



mf.plot(   (wl, I_ee, '-', 'red', {"label":'Energy-efficient light bulb', "lw":2}),
        (wl, I_hgcd, '--', 'blue', {"label":'Hg-Cd lamp', "lw":1}),
        legend=1, legLoc='upper left',
        xlabel='Wavelength [nm]', ylabel='Intensity [r.u.]',
        title="EE vs Hg-Cd lamp",
        xlim2 = 700   )
#Here we can see that some speaks are at identical wavelengths, from which we 
#can infer that the energy efficient lamp might have elements in common with
#the Hg-Cd lamp, and Hg (mercury) is poisonous! 








"""(24)_<<<<<<<<<<<<<<<<<<<<<<<<<<_NA LAMP_>>>>>>>>>>>>>>>>>>>>>>>>>>>>_(24)"""
#The file is originally from the university course Optics with Python II***.
I_na = np.loadtxt('NA_sp.trt', delimiter=';', skiprows=8, unpack=True)[1]#***
I_na = mf.calib(I_na)[1]
print('\n\n(24)_NA LAMP_(24)')



mf.plot(   (wl, I_na, '-', 'red'),
        xlabel='Wavelength [nm]', ylabel='Intensity [r.u.]',
        title="Na lamp",
        xlim2 = 700   )
#There is suposed to be a doublette at λ = 589.3nm with Δλ = 0.6nm, try zooming
#in! ...there is no sign of a doublette :(
#By taking the previously calculated resolution into consideration, we can see
#that our spectrometer's resolution is too low:
R = 300.68
dwl = 589.3 / R
print('Smallest resolvable wavelength: {0:0.2f}nm.'.format(dwl))








"""(25)_<<<<<<<<<<<<<<<<<<<<<<<<<<_RED LED_>>>>>>>>>>>>>>>>>>>>>>>>>>>>_(25)"""
#Now we shall look at the spectrum fo a red LED:
#The file is originally from the university course Optics with Python II***.
I_rled = np.loadtxt(   'RLED_sp.trt', delimiter=';', skiprows=8,
                      unpack=True   )[1]#***
I_rled = mf.calib(I_rled)[1]



mf.plot(   (wl, I_rled, '-', 'red'),
        xlabel='Wavelength [nm]', ylabel='Intensity [r.u.]',
        title="Red LED", xlim1=550, xlim2=750   )



print('\n\n(25)_RED LED_(25)')
mf.FWHM(   wl, I_rled, x1=550, x2=750   )








"""(26)_<<<<<<<<<<<<<<<<<<<<<<<<<_WHITE LED_>>>>>>>>>>>>>>>>>>>>>>>>>>>_(26)"""
#The file is originally from the university course Optics with Python II***.
I_wled=np.loadtxt(   'WLED_sp.trt',delimiter=';',skiprows=8,
                  unpack=True   )[1]#***
I_wled = mf.calib(I_wled)[1]



mf.plot(   (wl, I_wled, '-', 'red'),
        xlabel='Wavelength [nm]', ylabel='Intensity [r.u.]',
        title="White LED", xlim1=360, xlim2=800   )



print('\n\n(26)_WHITE LED_(26)')

mf.FWHM(wl, I_wled, x1=400, x2=500, f=0.1)
#mf.FWHM(wl, I_wled, x1=500, x2=800, f=0.1)     #ERROR!!! CHECK THE FUNCTION!!!
#Note that the right peak's y_max*f value is lower than the intensity values on
#on the left shoulder of the peak. If there were no error cases inside the func-
#tion, then instaad of interpolation, we would be extrapolating, and then we
#would get 
#x_left:  541.1828275837187         #Check the plot, this is nonsense!
#y_right:  681.666093439191         
#y_max*f:  2039.330410951912        



#The extrapolation:
x1=500
x2=800
f=0.1
y = I_wled[np.argmin(np.abs(wl-x1)):np.argmin(np.abs(wl-x2))]
x = wl[np.argmin(np.abs(wl-x1)):np.argmin(np.abs(wl-x2))]
i_max = np.argmax(y)
y_left = y[:i_max]
y_max = np.amax(y)
i = np.argmin(np.abs(y_max*f-y_left))
x_left = (y_max*f-y_left[i-1]) / (y_left[i]-y_left[i-1]) * (x[i]-x[i-1])+x[i-1]



#Let's plot the error!
m = (y_left[i] - y_left[i-1]) / (x[i] - x[i-1])
b = y_left[i] - m*x[i]
x = x[np.argmin(np.abs(x-500)):np.argmin(np.abs(x-580))]
y_error = m*x+b
ax = mf.plot(   (wl, I_wled, '-', 'red', {'label':'White LED'}),
        (x, y_error, '--', 'blue', {"label":"Extrapolative error"}),
        xlabel='Wavelength [nm]', ylabel='Intensity [r.u.]',
        title="The source of the error", xlim1=500, xlim2=580,
        legend=1, legLoc = "upper left")
ax.axhline(y_max*f)
#Zoom in on the left shoulder where the error line is equal to the spectrum's
#curve on 2 points! That is the source of the extrapolation.








"""(27)_<<<<<<<<<<<<<<<<<<_UNIVERSITY RED DIODE LASER_>>>>>>>>>>>>>>>>>>>_(27)"""
#The file is originally from the university course Optics with Python II***.
I_urdl = np.loadtxt('RDLH_sp.trt',skiprows=8,delimiter=';',
                   unpack=True)[1]#***
#To be precise, this laser was "homemade" by the university.
I_urdl = mf.calib(I_urdl)[1]
#Notice how confined the laser spectrums are to a small interval of wavelengths!



mf.plot(   (wl, I_urdl, '-', 'red'),
        xlabel='Wavelength [nm]', ylabel='Intensity [r.u]', 
        title='University Red diode laser', xlim1 = 600, xlim2=680   )



print("\n\n(27)_UNIVERSITY RED DIODE LASER_(27)")
mf.FWHM(   wl, I_urdl, x1=600, x2=680)








"""(28)_<<<<<<<<<<<<<<<<<_THORLABS RED DIODE LASER_>>>>>>>>>>>>>>>>>>>>_(28)"""
print('\n\n(28)_THORLABS RED DIODE LASER_(28)')
#The file is originally from the university course Optics with Python II***.
I_trdl=np.loadtxt('RDLT_sp.trt', delimiter=';',skiprows=8,
                  unpack=True)[1]#***
I_trdl=mf.calib(I_trdl)[1]



mf.plot(   (wl, I_trdl, '-', 'red'),
        xlabel='Wavelength [nm]', ylabel='Intensity [r.u]', 
        title='Thorlabs red diode laser', xlim1 = 630, xlim2=660   )

mf.FWHM(wl, I_trdl, x1=630, x2=660)








"""(29)_<<<<<<<<<<<<<<<<<<<<<<_HE-NE GAS LASER_>>>>>>>>>>>>>>>>>>>>>>>>_(29)"""
print('\n\n(28)_HE-NE GAS LASER_(28)')
#The file is originally from the university course Optics with Python II***.
I_hene=np.loadtxt('HENE_sp.trt', delimiter=';',skiprows=8,
                  unpack=True)[1]#***
I_hene=mf.calib(I_hene)[1]



mf.plot(   (wl, I_hene, '-', 'red'),
        xlabel='Wavelength [nm]', ylabel='Intensity [r.u]', 
        title='He-Ne gas laser', xlim1 = 625, xlim2=650   )

mf.FWHM(wl, I_hene, x1=625, x2=650)



mf.plot(   (wl, I_trdl, '-', 'red', {"label":"Thorlabs RDL"}),
        (wl, I_urdl, '-', 'blue', {"label":"URDL"}),
        (wl, I_rled, '-', 'green', {"label":"RLED"}),
        (wl, I_hene, '-', 'orange', {"label":"He-Ne"}),
        xlabel='Wavelength [nm]', ylabel='Intensity [r.u]', 
        title="Red lasers", xlim1 = 620, xlim2=720,
        legend=1, legLoc="upper right"   )








"""(30)_<<<<<<<<<<<<<<<<<<<<<<<_THORLABS GDL_>>>>>>>>>>>>>>>>>>>>>>>>>>_(30)"""
print('\n\n(28)_THORLABS GDL_(28)')
#The file is originally from the university course Optics with Python II***.
I_tgdl=np.loadtxt('GDL_sp.trt', delimiter=';',skiprows=8,
                  unpack=True)[1]#***
I_tgdl=mf.calib(I_tgdl)[1]



mf.plot(   (wl, I_tgdl, '-', 'green'),
        xlabel='Wavelength [nm]', ylabel='Intensity [r.u]', 
        title='Thorlabs green diode laser', xlim1 = 510, xlim2=525   )

mf.FWHM(wl, I_tgdl, x1=510, x2=525)

























