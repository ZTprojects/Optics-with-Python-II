import numpy as np
import matplotlib.pyplot as plt
import myfuncs as mf
plt.close('all')








#This python text file is similar to the previous one, but it is with a spectro-
#meter that ahs a reflexive grating instead of a transmissive one. Note that N
#here is approximately 3 times greater!
"""(36)_<<<<<<<<<<<<<<<_SPECTROMETER: REFLEXIVE GRATING_>>>>>>>>>>>>>>>_(36)"""
print("\n\n(36)_SPECTROMETER: REFLEXIVE GRATING_(36)")
#Similar to the spectrometer with a transmissive grating.
N = 650 / 10**6 #line/nm
alpha0 = 20#°
alpha0 = np.deg2rad(alpha0)
wl = np.arange(545,595,0.1)
#d*(sinalpha0 - sinbeta) = m*lambda, where d = 1/N. Let m be -1:
beta = np.arcsin(   np.sin(alpha0) + wl*N   )



mf.plot(   (wl, np.rad2deg(beta), '-', 'r'),
            xlabel="Wavelength [nm]", ylabel="Angle of diffraction [°]",
            title = "β(λ)")
#Notice how the angular interval is smaller than 4°-s! f*delta beta = n_C*p is 
#therefore a "functioning" approximation.
#The nagular dispersion:
ad = N / np.sqrt(   1 - (   np.sin(alpha0)+N*wl   )**2   )
ad_avg = ad[   np.argmin(   np.abs(wl-570)   )  ]
print(f"Angular dispersion at 570 nm: {ad_avg*1000:0.4f} mrad/nm.")



p = 6 * 10**3 #nm, an individual pixel's size
n_c = 640#count of horizontal pixels
f = 58 * 10**6 #focal length of the objective lense.
usr = n_c*p  /  (   f * ad_avg   )
print(f"The usable spectral range is: {usr:0.2f} nm.")



#The reciprocal linear dispersion in nm/pixel units:
k = usr / n_c
print(f"The reciprocal linear dispersion: {k:0.2f} nm/pixel.")



#The Hg_Cd lamp's spectrum on this spectrometer:
#The file is originally from the university course Optics with Python II***.
img = plt.imread("HgCd_sp_RG.jpg")#***
print(f"Size of the image: ", img.shape)
lines = img.shape[0]
columns = img.shape[1]

factors = [0.299, 0.587, 0.114]
im = np.dot(   img, factors)
i0 = 290
I = im[i0,:]


fig, ax = plt.subplots()
ax.set_xlabel("Column index")
ax.set_ylabel("Line index")
ax.set_title("Hg_Cd spectrum")
ax.imshow(img, aspect='auto')



fig, ax = plt.subplots()
ax.set_xlabel("Column index")
ax.set_ylabel("Line index")
ax.set_title("Hg_Cd spectrum")
ax.imshow(img, aspect='auto')

j=np.arange(0, columns, 1   )

ax2 = ax.twinx()
ax2.plot(   j, I, 'r--', label=str(i0)+". line",
         linewidth=0.6)
ax2.legend(loc="upper right")
ax2.set_ylabel("Intensity [r.u]")



hgcd_peaks = mf.maxList(j, I, y1 = 50)
hgcd_peaks = np.array(hgcd_peaks)
for i in range(len(hgcd_peaks)):
    print(f"Index: {hgcd_peaks[i][0]} \t\tIntensity: {hgcd_peaks[i][2]}")



#Using an external database, the wavelengths of these peaks are as follows:
hgcd_peaks_db = np.array([546.075, 576.961, 579.067])
coeff = np.polyfit(   hgcd_peaks[:,0], hgcd_peaks_db, deg = 1)

wl = 0
for i in range(len(coeff)):
    wl += hgcd_peaks[:,0]**i * coeff[len(coeff)-1-i]



mf.plot(   (hgcd_peaks[:,0], hgcd_peaks_db, 'o', 'red', {"label":"Database"}),
            (hgcd_peaks[:,0], wl, '--', 'blue', {"label":"Calibrated"}),
            xlabel="Column indices", ylabel="Wavelength [nm]",
            title="Calibration",
            legend=1, legLoc="lower right"   )


print("\nValues from the fitting:")
print(f"Reciprocal linear dispersion: {coeff[0]:0.4f} nm/pixel.")
print(f"Smallest wavelength (a0): {coeff[1]:0.2f} nm.")
print(f"Usable spectral range: {coeff[0]*columns:0.2f} nm.\n")



#The difference between the calibrated line and "reality":
diff = -wl + hgcd_peaks_db
mf.plot(   (hgcd_peaks[:,0], diff, 'o', 'red'),
            xlabel="Column indices", ylabel="Wavelength [nm]",
            title="Calibration",
            )   #There are only 3 points, so its hard to whether we need a higher
                #degree polynomial or not, but this will suffice.



wl=0
for i in range(len(coeff)):
    wl += j ** i * coeff[len(coeff)-1-i]
    
ax = mf.plot(   (wl, I, 'o', 'red', {"label":"Measurement"}),
             (wl, I, '--', 'blue'),
             xlabel="Wavelength [nm]", ylabel="Intensity [r.u.]",
             title="FWHM",
             xlim1 = 578, xlim2=580,
             legend=1, legLoc="upper left"   )

i1 = np.argmin(np.abs(wl-578))
i2 = np.argmin(np.abs(wl-580))
ax.axhline(np.max(I[i1:i2])/2, color = "green", label=r"$\frac{I_{max}}{2}$")
ax.legend()



fwhm = mf.FWHM(   wl, I, x1 = 578, x2 = 580)
print(f"FWHM: {fwhm:0.2f} nm.")
#The resolution then:
wl_579 = wl[np.argmin(np.abs(I-max(I[i1:i2])))]
R = wl_579 / fwhm
print(f"Resolution at 579.1 nm-s: {R:0.2f}.")








"""(37)_<<<<<<<<<<<<<<<<_RG SPECTROMETER: NA SPECTRUM_>>>>>>>>>>>>>>>>>_(37)"""
print("\n\n\n(37)_RG SPECTROMETER: NA SPECTRUM_(37)")
#The file is originally from the university course Optics with Python II***.
img_na = plt.imread("Na_sp_RG.jpg")#***
im_na = np.dot(   img_na, factors   )
I = im_na[i0,:]
columns = np.arange(img_na.shape[1])

fig, ax = plt.subplots()
ax.set_xlabel("Column index")
ax.set_ylabel("Line index")
ax.set_title("Na spectrum")
ax.imshow(img_na, aspect='auto')

fig, ax = plt.subplots()
ax.set_xlabel("Column index")
ax.set_ylabel("Line index")
ax.set_title("Na spectrum")
ax.imshow(img_na, aspect='auto')

ax2 = ax.twinx()
ax2.plot(columns, I, 'r--', linewidth=0.5, label=str(i0) +". line")
ax2.legend(loc="upper left")
#This spectrometer could clearly dissolve the doublette!



fig, ax = plt.subplots()
ax.set_xlabel("Column index")
ax.set_ylabel("Line index")
ax.set_title("Na spectrum: gray-toned")
ax.imshow(im_na, cmap='gray', aspect='auto')



mf.plot(   (wl, I, '-', 'red'),
             xlabel="Wavelength [nm]", ylabel="Intensity [r.u.]",
             title="Na spectrum")



na_peaks = mf.maxList(   wl, I,   y1 = 100)
for i in range(len(na_peaks)):
    print(f"Wavelength: {na_peaks[i][1]:0.2f} \t\tIntensity: {na_peaks[i][2]:0.2f}")

d_wl_peaks = na_peaks[1][1] - na_peaks[0][1]
wl_peaks = (na_peaks[1][1] + na_peaks[0][1]) / 2
d_wl_min = wl_peaks / R
print(f"The smallest dissolvable wavelength: {d_wl_min:0.2f} nm.")
print(f"The wavelength difference between the doublettes: {d_wl_peaks:0.2f} nm.")
#Mission accomplished. B)




























