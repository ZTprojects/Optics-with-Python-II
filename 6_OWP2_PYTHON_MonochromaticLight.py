import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as wdt
import myfuncs as mf
plt.close('all')








"""(38)_<<<<<<<<<<<<<<<<<<<_MONOCHROMATIC LIGHT_>>>>>>>>>>>>>>>>>>>>>>>_(38)"""
print("\n\n\n(38)_MONOCHROMATIC LIGHT_(38)")
#Assume we are using a He-Ne laser, so wl = 632.8, then:
c = 299.792458 #nm/fs
wl = 632.8
k = 2*np.pi/wl
om = 2*np.pi*c/wl
T = 2*np.pi/om
E0 = 1
phi0 = 0#rad
t0 = 0
z  = np.arange(   -1000, 1001, 1   )#nm
#n = 1
#E(z, t0) = E0*cos(om*t-k*n*z+phi0)
E = E0*np.cos(om*t0-k*z+phi0)



ax=mf.plot(   (z, E, '-', 'red', {"label":"$t_0$ = 0.0 fs"}),
            xlabel="z [nm]", ylabel="Electric field strength", 
            title="Monochromatic light along axis z", legend=1)

t0 = 0.5#fs
E = E0*np.cos(om*t0-k*z+phi0)
ax.plot(z, E, 'r--', label="$t_0$ = 0.5 fs")
ax.legend()



x = y = z
fig, ax = plt.subplots()
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(x, y)
Z = E0*np.cos(om*t0-k*z+phi0) +0*Y
ax.plot_surface(X,Y,Z, cmap='Reds',  rcount=50, ccount=50)
ax.set_xlabel("z [nm]")
ax.set_ylabel("y [nm]")
ax.set_zlabel("E [r.u.]")
ax.set_title("EFS")



#Now we will be changing the time instead of the z parameter!
t = np.arange(   -4, 4.01, 0.01   )#fs
z0 = 0
E = E0*np.cos(om*t-k*z0+phi0)


ax=mf.plot(   (t, E, '-', 'red', {"label":"$z_0$ = 0.0 nm"}),
            xlabel="t [fs]", ylabel="Electric field strength", 
            title="Monochromatic light along the time axis")

z0 = 150#nm
E = E0*np.cos(om*t-k*z0+phi0)
ax.plot(t, E, 'r--', label="$z_0$ = 150 nm")
ax.legend()

dz=z0
dt = dz / c
print(f"dt = {dt:0.1f} fs.")



z0=0
fig, ax = plt.subplots()            #Let's make it with a slider!
plt.subplots_adjust(bottom=0.25)    #This creates more space at the bottom for 
                                    #the slider.
curves = ax.plot(t, E, 'r-')
ax_slider1 = plt.axes(   [0.2, 0.1, 0.6, 0.01]   )
                                    #This is a new 'axes' object! The numbers:
                                    #distance from left, bottom. Width, height.
slider1 = wdt.Slider(   ax_slider1, "$E_0$", -1, 1, valinit=E0   )#Here we make 
                                    #use of the created object, define its label,
                                    #set start and end values for its interval
                                    #and a starting value.
ax_slider2 = plt.axes(   [0.2, 0.05, 0.6, 0.01]   )
slider2 = wdt.Slider(   ax_slider2, "$\phi_0$", 0, 8*np.pi, valinit=phi0   )



def mono(   E0, phi0   ):
    efs = E0*np.cos(om*t-k*z0+phi0)
    return efs



def sliderUpdate(   value, lineName, *sliderNames   ):
    currentValue1 = sliderNames[0].val
    currentValue2 = sliderNames[1].val
    lineName.set_ydata(   mono(   currentValue1, currentValue2   )   )
    fig.canvas.draw_idle()  #This alone is sometimes enough, e.g. in Jupyter
    #Notebook, but in Python, we must use it in conjunction with 
    #slider.on_changed(sliderUpdate)
    #Notice how "value" is not used.
slider1.on_changed(   lambda currentVal: sliderUpdate(   currentVal, curves[0], slider1, slider2   )   )
slider2.on_changed(   lambda currentVal: sliderUpdate(   currentVal, curves[0], slider1, slider2   )   )
    #We need the "value" argument here. It checks the value of the slider and
    #inserts it into the first possible argument inside the sliderUpdate function.
    #This way, this command changes the value of "value", which does nothing!
    #Nothing goes wrong :)
    
    #Basically, the slider1.on_changed(function) gives a value to the internal
    #function, and changes its very first argument to that, so it ahs to be able
    #to accept that argument.
    #The lambda function makes it such that this value is given to the lambda 
    #function's currentVal parameter, which it passes on to the function given
    #after the ":". There, at sliderUpdate, only the first variable will be changed.
    #If the sliderUpdate function required only 1 argument, then this would be 
    #unnecessary.








"""(39)_<<<<<<<<<<<<<<<<<<<<<<<_POYNTING VECTOR_>>>>>>>>>>>>>>>>>>>>>>>_(39)"""
print("\n\n\n(39)_POYNTING VECTOR_(39)")
#Here we assume some constants to be equal to 1.
E = E0 * np.cos(om*t-k*z0)
S = E**2



ax = mf.plot(   (t, E, '-', 'blue', {"label":"E"}),
                 xlabel="Time [fs]", ylabel="EFS [r.u.]", title="E vs. S",
                 legend=1, legLoc="upper left")
ax.tick_params('y', colors='blue')



ax2 = ax.twinx()
ax2.plot(   t, S, '-', color='red',  label="S"   )
ax2.set_ylabel("Poynting vector [r.u$.^2$]", color='red')
ax2.tick_params('y', colors='red')
ax2.legend()
#Notice how the frequency doubles for the Poynting vector!
#In the case of visible light, the period time ranges in the femtoseconds!
#Detectors are not thata fast, so basically, they gather information over a time
#that is much larger than period time of the oscillation. The signal is averaged
#out over time.










