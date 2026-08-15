import numpy as np
import matplotlib.pyplot as plt








"""(1)_<<<<<<<<<<<<<<<<<<<<<<<<<<<<<_n_>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>_(1)"""
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









"""(2)_<<<<<<<<<<<<<<<<<<<<<<<<<<<<_plot_>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>_(2)"""
def plot(   *lines, title='', xlabel='', ylabel='', 
         xlim1 = None, xlim2 = None,
         ylim1 = None, ylim2 = None,
         fontsize=10, titlesize=15, 
         legend=0, legLoc='upper right'   ):
    """EXAMPLE: mf.plot(   (x, y, '-', 'red', {"label": "Spectrum", "lw": 2.5})   )
    
    for line in lines:
        
        
        if len(line)==4:
            x, y, style, color = line    
            kwargs={}
        
        
        elif len(line)==5:
            x, y, style, color, kwargs = line"""#for documentation.
    
    fig, ax = plt.subplots(figsize=(10,8))
    
    
    
    for line in lines:
    
        
        if len(line)==4:
            x, y, style, color = line    
            kwargs={}
        
        
        elif len(line)==5:
            x, y, style, color, kwargs = line
            
            
        else:
            raise ValueError("Each line must be either:\n"
                "(x, y, style, color)\n"
                "or\n"
                "(x, y, style, color, kwargs(=dict))"
            )
            
            
        ax.plot(x, y, style, color=color, **kwargs)
        
        
        
    if legend==1:
        ax.legend(loc=legLoc)
        
    ax.grid()
    ax.set_title(title, fontsize=titlesize, pad=25)
    ax.set_xlabel(xlabel, fontsize=fontsize, labelpad=25)
    ax.set_ylabel(ylabel, fontsize=fontsize, labelpad=25)
    fig.tight_layout(pad=4)

    
    
    xmargin = 0
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
        y1 = min(  np.min(  line[1][  np.argmin(  np.abs(line[0]-xlim1-xmargin)  )  :  np.argmin(  np.abs(line[0]-xlim2+xmargin)  )+1  ]  ) for line in lines  )

    if ylim2 is None:
        y2 = max(  np.max(  line[1][  np.argmin(  np.abs(line[0]-xlim1-xmargin)  )  :  np.argmin(  np.abs(line[0]-xlim2+xmargin)  )+1  ]  ) for line in lines  )
    
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
    
    
    #print("mf.plot(xlim): ", ax.get_xlim())
    #print("mf.plot(ylim): ", ax.get_ylim())
    return ax








"""(3)_<<<<<<<<<<<<<<<<<<<<<<<<<<<_FWHM_>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>_(3)"""
def FWHM(x, y, x1=None, x2=None, f=0.5):
    
    
    
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
    error=''
    
    
    
    if i_max == 0 or np.all(   y_max*f < y[:i_max]   ) == True:
        error = error + 'left'
        
    if i_max == len(y)-1 or np.all(   y_max*f < y[i_max:]   ) == True:
        error = error + 'right'
        
        
        
    if error =='leftright':
        raise ValueError("Could not find appropriate x_left and x_right values for y_max*f.")
    
    elif error=='left':
        raise ValueError("Could not find an appropriate x_left value for y_max*f.")
        
    elif error=='right':
        raise ValueError("Could not find an appropriate x_right value for y_max*f.")

    
    
    #The left side of the curve:
    for i in range(len(y)):
        a = y[i]
        
        if np.isclose(a, y_max * f, atol=1e-8):
            x_left = x[i]
            break
        
        elif a > y_max*f:
            x_left = (y_max*f-y[i-1]) / (y[i]-y[i-1]) * (x[i]-x[i-1])+x[i-1]
            break
      


    #The right side of the curve:
    for i in range(len(y)):
        j = len(y)-1-i
        a = y[j]
        
        if np.isclose(a, y_max * f, atol=1e-8):
            x_right = x[j]
            break
        
        elif a > y_max*f:
            x_right = (y_max*f-y[j+1]) / (y[j]-y[j+1]) * (x[j]-x[j+1])+x[j+1]
            break
        

      
    #Self-checking!
    print("x_left: ",x_left)
    print("y_right: ",x_right)
    print("y_max*f: ", y_max*f)
    print("Peak x: ", x[np.argmax(y)])
    print("Peak y: ", np.max(y))
    print("FWHM(f): ", (x_right - x_left))
    return x_right - x_left








"""(4)_<<<<<<<<<<<<<<<<<<<<<<<<<<_maxList_>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>_(4)"""
def maxList(x, y, x1=-np.inf, x2=np.inf, y1=-np.inf, y2=np.inf):
    """def maxList(x, y, x1=-np.inf, x2=np.inf, y1=-np.inf, y2=np.inf):
        
        maxList = []
        for i in range(1,len(x)-1):
            if x[i] >= x1 and x[i] <= x2:
                if y[i] >= y1 and y[i] <= y2:
                    if y[i-1] < y[i] > y[i+1]:
                        maxList.append([i, x[i], y[i]])
        return maxList"""#for documentation.
    
    maxList = []
    for i in range(1,len(x)-1):
        if x[i] >= x1 and x[i] <= x2:
            if y[i] >= y1 and y[i] <= y2:
                if y[i-1] < y[i] > y[i+1]:
                    maxList.append([i, x[i], y[i]])
    return maxList








"""(5)_<<<<<<<<<<<<<<<<<<<<<<<<<<<_calib_>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>_(5)"""
def calib(x):
    """wl, I_d = np.loadtxt('SPECTRUM0001.trt',
                       delimiter=';', skiprows = 8, unpack=True)#***
        
    
    h = 0.663               #aJ/fs, Planck-constant
    
    k = 1.381*10**(-5)      #aJ/K, Boltzmann-constant
    
    c = 299.792             #nm/fs, lightspeed in vacuum
    
    T = 2800                #°K, temperature (given by manufacturer)
    
    
    
    I = (8*np.pi*h*c**2/wl**5) * 1 / (np.exp(h*c/wl/k/T) - 1)
    
    K = I_d / I            
    K = K / np.max(K)
    
    return wl, x/K"""#for documentation.

    #The file is originally from the university course Optics with Python II***.
    wl, I_d = np.loadtxt('SPECTRUM0001.trt',
                       delimiter=';', skiprows = 8, unpack=True)#***
        
    
    h = 0.663               #aJ/fs, Planck-constant
    k = 1.381*10**(-5)      #aJ/K, Boltzmann-constant
    c = 299.792             #nm/fs, lightspeed in vacuum
    T = 2800                #°K, temperature (given by manufacturer)
    
    
    I = (8*np.pi*h*c**2/wl**5) * 1 / (np.exp(h*c/wl/k/T) - 1)
    
    K = I_d / I            
    K = K / np.max(K)
    
    return wl, x/K







'''
"""(6)_<<<<<<<<<<<<<<<<<<<<<<<<_sliderUpdate_>>>>>>>>>>>>>>>>>>>>>>>>>>>_(6)"""
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
"""needs to be worked on."""
'''















"""
...........################...........#################......................................
...........#################..........###############.....................................
...........###################.........##################.....................................
...........################............ ################.....................................
............###################..........###############.....................................
............################..............###################...................................
............###################............#################...................................
.............#################..............##################..................................
..............###################............###################..................................
...............##################............#################.................................
................##################............##################...................................................
..............................................................................
.....................................########.....................................
......................................#######......................................
........................................######......................................
........................................#######......................................
...................................#############.....................................
...............................................................................
...#########################.................................############################.................
.....#########################..............................###########################....................................
......#########################.........................#########################.........................................
........#########################...................##############################.............................................
............###############################################################...............................................................
.................#####################################################..................................................
.....................############################################.............................................
...........................##################################..................................
...............................................................................
........................................................#ZTprojects.......................
...............................................................................
"""




"""
.............................................................ccccccccccccc....................................
.ccccccccccccccccccccccccccccccccccccccccccccc.............cccccccccccccccccc..................ccccccccccccccccccccccccccccccccccccccccc.....................................
.......cccccccccccccccccccccccccccccccccccccccccccc.........cccccccccccccc............ccccccccccccccccccccccccccccccccccccccccccccccccccc
.ccccccccccccccccccccccccccccccccccccccccccc..................................ccccccccccccccccccccccccccccccccccccccccccc..................
.......ccccccccccccccccccccccccccc..............................................ccccccccccccccc.cccccccccccc.ccccccccccc
....cccccccccccccccccccccccccc..............................................ccccccccc....ccccccccccccccccccccccccccccc.............................
.ccccccccccccc...........................OOOOOOOOOOOOOOOOOO.................cc...cccccccccccccccccccccccccccc.......................
...ccccccccc.......................OOOOOOOOOOOOOOOOOOOOOOOOOOOO.............ccccccc......cccccccccccccccccc..........................
................................OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO...........................ccccccccc..............
..............................OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO............................
............................OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO...................................................................
...........................OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO..........................
..........................OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO......................................................................
..........................OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO.......................................................................
WWWWrrrrrrWWrrrrrrrrrrrrrrrrrrrrWWWWWrrrrrrrrrWWWWWWWWWWrrrrrrWWrrrrrrrrrrrrrrrrrrrrrrrWWWWWWWWWWW.................................................................................................
WWWWWWWWWWWWWWWWWWWWWrrrrrrrrrrrrWWWWWWWrrrrrrrWWWrrrWWrrrrrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWrrrrrrrrWWWWW
WWWWWWWWWWWWWrrrrrrrrrWWWWWWWWWWWWWrrrrrrrrrrrWWWWWrrrrrrrrrrrrrrrrrrrrrrrrrrrWWWWrrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWrrrrrrrrWWWWrrrrrWWWWWrrrrrrrrrWWWWWWWrrrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWrrrrrrWWWWWWWWWWWWWWrrrrrrrrrrWWWWWWWWWWWWrrrrrrrrrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWrrrrrrrrrrWWWWWWWWWWWWWWWWWWWrrrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWrrrrrrrrrrrrWWWWWWWWWWWrrrrWWWWWWWWrrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW.................................................................................................
WWWWWWWWWWWWWWWWWWWWWWWWWrWrWrWWWrWWWWWrWWWWWWWrrrrWWrWWWrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWrrrrrrrWWWrWWWWWWrrrrWrrrrrWWrrWWWWWrrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW.................................................................................................
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWrrrrrrrrrrrrrrrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWrrrrrrWWWWWrrrrrrrrWWWrrrrrrrWWWWWWWrrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWrrrrrrWWWrrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWrrrrrrWrrrrrrrrrrrWWrrrrrrrrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWrrrrrWWrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWrrrrWWWWrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWrrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWrWWWWWrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWrrrrWWWWrrrWWWrrrrrrWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
..wwwwwwwwwwwwwwwwwwwwwwwww.....wwwwwwwwwwwwwwwwwwwwwwww........WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW.........................................................
......WWWWWWWWWWWWWWWW.WWWWWWWWWWW.WW......WWW.........WWWW......WWWWWWWWWWWWWWWWWWW......WWWWWWWWWWWWWWWWWWWWWWW.........................
WWWWW.......WWWWWWWWWW............WWWWWWW..........WWWWWWWWWWWWWWWWWWWWW.....WW.....WWWWWWWWWWWWWW........
WWWWWWWW.........WWWWWWWWWWW.........WWWWWWWWWWWW.......WWWWWWWWWWWWWW.....................WWWWWWWWWWWW.........
...WWWWWW.................WWWWWWWW.......................................WWWWW........
...........WWWWW..............WWWW...........WWWWW...................................
.............WW..........WWWWWW.........................................WWWWWW................
.................WWWW..............................WWWWWWWWWWWW..........................
.................................................................................................
.................................................................................................
.................................................................................................
.................................................................................................
.................................................................................................
................................................................................................."""











