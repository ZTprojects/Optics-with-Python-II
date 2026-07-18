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



def plot(*lines, title='', xlabel='', ylabel='', legend=0, legLoc='upper right'):
    fig, ax = plt.subplots()
    for x, y, style, label in lines:    
        ax.plot(x, y, style, label=label)
        if legend==1:
            ax.legend(loc=legLoc)
        
    ax.grid()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    
    return ax






"""(19)_<<<<<<<<<<<<<<<<<<<<<<<<<_OPTICAL GRID_>>>>>>>>>>>>>>>>>>>>>>>>_(19)"""
#Huygens–Fresnel principle: Every point on a wavefront can be regarded as the 
#source of secondary spherical wavelets. The interference of these mutually 
#coherent secondary wavelets determines the light intensity (or optical field) 
#observed at any point in space. This theory is crucial for explaning the way
#an optical grid works. The criterion for the light path to obtain the maximum 
#amplification of the waves:
#delta = d * sin(beta) = m * wl
#Visual demo: 1_OWP2_INKSCAPE_OpticalGrid.pdf
#If we have 200 lines/mm, then d = 1 / 200 * 10**6 nm. If we shine a He-Ne la-
#ser on the grid, then wl = 632.8nm, and the angle of diffraction will be:
d = 1/200*10**6#nm
wl=632.8#nm
beta=np.asin(   1*wl/d   )
print(np.rad2deg(beta)) #1st order maximum



#Now let's have a look at higher orders:
m = np.ones(4)
for i in range(len(m)-1):
    m[i+1] = m[i] + 1
beta = np.asin(   m*wl/d   )

for i in range(len(m)):
    print(   'Angle of the {0:0d}th order maximum: {1:0.2f}°.'
          .format(int(m[i]), np.rad2deg(beta[i]))   )



#Now expand the range of the wavelength:
wl = np.arange(300,1000+1,50)
beta=np.asin(   1*wl/d   )
plot(   (wl, np.rad2deg(beta), 'ro', ''), 
     title='Diffraction on an optical grid',
     xlabel='Wavelength [nm]', ylabel='Angle of 1st order diffraction [°]'   )
#Looks pretty linear!






"""(20)_<<<<<<<<<<<_NUMERICAL DERIVATION USING A FIT FUNCTION_>>>>>>>>>_(20)"""
#Assuming we only discrete points of the function we desire to derivate, we can
#derivate point by point like we did in the previous repository/course, OR we 
#can fit a function to the points we know and derivate that analytical function!
#That is what we will be busy with in this section:

#numpy.polyfit(x, y, deg, rcond=None, full=False, w=None, cov=False)
#x, y: trivial
#deg: degree of the polynomial we wish to fit onto the points.
#The result will be an ndarray of the polynome factors, from highest to lowest 
#degree, of a fit polynomial.
fit = np.polyfit(wl, beta, deg=1)
beta_fit = fit[0]*wl+fit[1]
plot(   (wl, np.rad2deg(beta), 'ro','Theoretical'),
     (wl,np.rad2deg(beta_fit),'b--','Polynomial fit'),
     title='Polynomial fitting of the diffraction angle',
     xlabel='Wavelength [nm]', ylabel='Angle of diffraction [°]',
     legend=1, legLoc='lower right')
print(   'Theoretical slope: {0:0.5f} °/nm.'.format(np.rad2deg(1/d))   )
#beta = wl * (1/d). This equation assumes beta is small!
print(   'Slope of the fit: {0:0.5f} °/nm.'.format(np.rad2deg(fit[0]))   )
#As we can see, the difference is quite small.



#Calculate the difference between the values obtaiend via theory and the ones
#obtained via the polynomial fit and visualize it:
plot(   (wl, np.rad2deg(beta-beta_fit), 'ro',''),
     title='Discrepancy between fitting and theory',
     xlabel='Wavelength [nm]', ylabel='Discrepancy [°]'   )
#The difference is small, but we can observe a dominant second order discrepancy.
#Implement a correction:
fit2 = np.polyfit(wl, beta, deg=2)
beta_fit2 = np.zeros(len(wl))
for i in range(len(fit2)):
    beta_fit2 += fit2[i] * wl**(   (len(fit2)-1)-i   )
plot(   (wl, np.rad2deg(beta-beta_fit2), 'ro',''),
     title='Discrepancy between fitting and theory',
     xlabel='Wavelength [nm]', ylabel='Discrepancy [°]'   )



#There seems to be a dominat third order difference, so let's go higher!
fit3 = np.polyfit(wl, beta, deg=3)
beta_fit3 = np.zeros(len(wl))
for i in range(len(fit3)):
    beta_fit3 += fit3[i] * wl**(   (len(fit3)-1)-i   )
plot(   (wl, np.rad2deg(beta-beta_fit3), 'ro',''),
     title='Discrepancy between fitting and theory',
     xlabel='Wavelength [nm]', ylabel='Discrepancy [°]'   )
#Good enough! :)



#Let's have a look at angular dispersion with the fit and theoretical values!
#beta = asin(wl/d)
#asin'(x) = 1 / sqrt(1-x**2)
#d(beta) / d(wl) = 1 / (   d * sqrt(1-(wl/d)**2)   )
disp_th = 1 / (   d * np.sqrt(1 - (wl/d)**2)   )
disp_fit3 = np.gradient(   beta_fit3, wl   )



plot(   (wl, np.rad2deg(disp_th), 'ro','Analytical'),
     (wl, np.rad2deg(disp_fit3), 'b--', 'Numerical'),
     title='Discrepancy between fitting and theory of dispersion',
     xlabel='Wavelength [nm]', ylabel='Dispersion [°/nm]',
     legend=1, legLoc='upper left')
#As expected, np.gradient is less precise at the first and last points!



#Let's analytically derivate the polynomial!
disp_fit3 = np.zeros(len(wl))
for i in range(len(fit3)):
    if len(fit3)-1-i-1 >= 0:
        disp_fit3 += fit3[i] * wl**(   (len(fit3)-1)-i-1   ) * (  (len(fit3)-1)-i )
        
        
        
plot(   (wl, np.rad2deg(disp_th), 'ro','Analytical'),
     (wl, np.rad2deg(disp_fit3), 'b--', 'Numerical'),
     title='Angular dispersion',
     xlabel='Wavelength [nm]', ylabel='Dispersion [°/nm]',
     legend=1, legLoc='upper left')
#Much better!



#The difference:
plot(   (wl, np.rad2deg(disp_th-disp_fit3), 'ro',''),
     title='Discrepancy between fitting and theory of dispersion',
     xlabel='Wavelength [nm]', ylabel='Dispersion [°/nm]'   )



