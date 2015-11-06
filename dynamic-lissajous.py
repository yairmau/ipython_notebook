import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import warnings

warnings.filterwarnings(category=RuntimeWarning, action="ignore")

# configure plotting preferences

# http://wiki.scipy.org/Cookbook/Matplotlib/LaTeX_Examples
pts_per_inch=72.27       # this is a latex constant, don't change it.
text_width_in_pts=300.0  # write "\the\textwidth" (or "\showthe\columnwidth" for a 2 collumn text)
                         # inside a figure environment in latex, the result will be on the dvi/pdf next to the figure. See url above.
text_width_in_inches=text_width_in_pts/pts_per_inch
golden_ratio=0.618       # make rectangles with a nice proportion
inverse_latex_scale=2    # figure.png or figure.eps will be intentionally larger, because it is prettier
                         # when compiling latex code, use \includegraphics[scale=(1/inverse_latex_scale)]{figure}
fig_proportion = (1.0) # we want the figure to occupy 2/3 (for example) of the text width
csize=inverse_latex_scale*fig_proportion*text_width_in_inches
fig_ratio = 1.0
fig_size=(1.0*csize,fig_ratio*csize)  # always 1.0 on the first argument
fig=plt.figure(1,figsize=fig_size)     # figsize accepts only inches. if you rather think in cm, change the code yourself.
fig.clf()

class Positions:
    pass
pos = Positions()
pos.top    = 0.97
pos.bottom = 0.10
pos.left   = 0.13
pos.right  = 0.98
pos.hspace = 0.00
pos.wspace = 0.02
fig.subplots_adjust(top=pos.top,bottom=pos.bottom,left=pos.left,right=pos.right,hspace=0.00,wspace=0.03)
ax=fig.add_subplot(111)

text_size=inverse_latex_scale*12  # find out the fontsize of your latex text, and put it here
tick_size=inverse_latex_scale*8
# learn how to configure: http://matplotlib.sourceforge.net/users/customizing.html
params = {'backend': 'ps',
          'axes.labelsize': text_size,
          #'axes.linewidth' : 0,
          'text.fontsize': text_size,
          'legend.fontsize': text_size,
          'legend.handlelength': 2.5,
          'legend.borderaxespad': 0,
          'xtick.labelsize': tick_size,
          'ytick.labelsize': tick_size,
          'font.family':'serif',
          'font.size': text_size,
          'font.serif':['Times'], # Times, Palatino, New Century Schoolbook, Bookman, Computer Modern Roman
          'ps.usedistiller': 'xpdf',
          #'text.latex.preamble' : [ '\usepackage{mathptmx}'], # include here any neede package for latex; times roman fonts for math
          'text.latex.preamble' : [r'\usepackage{amsmath}'],
          #'mathtext.fontset': 'stixsans',
          'text.usetex': True,
          'figure.figsize': fig_size}
plt.rcParams.update(params)

plt.hold('on')

# define functions

def beta_func(a, b):
    e1 = scipy.special.gamma(a)
    e2 = scipy.special.gamma(b)
    e3 = scipy.special.gamma(a + b)
    return (e1*e2)/e3

beta_dist = lambda x,a,b: (1.0/beta_func(a,b)) * x**(a-1.0) * (1-x)**(b-1.0)

def lissajous(t,a,b):
    x = 1.0 * np.sin(a*t + delta)
    y = 1.0 * np.sin(b*t)
    return np.array([x,y])

periods = 1.0
x = np.linspace(0,1,101)
t = np.linspace(0,2.0*np.pi*periods,101)
delta = 0.0
# Gamma = np.linspace(0,3.9,101) 
# ax.plot(Gamma,np.ones(len(Gamma)),color='black',ls='-',lw=2)
# ax.plot(Gamma,Gamma+1,color='black',ls='--',lw=2)

ax.set_xlabel(r"$a$")
ax.set_ylabel(r"$b$")

pos.x_min = 0.0
pos.x_max = 4.0
pos.y_min = 0.0
pos.y_max = 4.
pos.x_scaling = 0.5
pos.y_scaling = 0.5
ax.axis([pos.x_min,pos.x_max,pos.y_min,pos.y_max])

ax.set_xticks(np.arange(0,4.5,0.5))
ax.set_yticks(np.arange(0,4.5,0.5))

class MouseBeta(object):
    def __init__(self, ax, **kwargs):
        self.ax = ax
        self.x = np.linspace(0,1,101)
        self.t = np.linspace(0,2.0*np.pi*periods,101)
        # self.curve = lambda a,b: beta_dist(self.x,a+1.0,b)
        self.curve = lambda a,b: lissajous(self.t,a,b)
        # self.scaling = [pos.x_scaling,pos.y_scaling]
        self.line, = self.ax.plot(self.x*pos.x_scaling,
                                  self.curve(0,0)*pos.y_scaling,
                                  visible=False, **kwargs)
    def shape(self,a,b):
        return a*self.x + b*self.x**2
    def show_beta(self, event):
        if event.inaxes == self.ax:
            self.line.set_data(event.xdata+(self.x-0.5)*pos.x_scaling, 
                               event.ydata+(self.curve(event.xdata,event.ydata)-0.5)*pos.y_scaling)
            self.line.set_visible(True)
        else:
            self.line.set_visible(False)
        plt.draw()

def insert_window(ax,pos,pair,x):
    Ystretch = 2.5
    sizeX = pos.x_scaling
    sizeY = pos.y_scaling
    sizeY_stretched = sizeY*Ystretch
    ax2sizeX = (sizeX/(pos.x_max-pos.x_min)) * (pos.right-pos.left)
    ax2sizeY = (sizeY_stretched/(pos.y_max-pos.y_min)) * (pos.top-pos.bottom)
    pos_x_window = ((pair[0]-pos.x_min)/(pos.x_max-pos.x_min)) * (pos.right-pos.left) + pos.left - ax2sizeX/2.0
    pos_y_window = ((pair[1]-pos.y_min)/(pos.y_max-pos.y_min)) * (pos.top-pos.bottom) + pos.bottom - ax2sizeY/fig_ratio/2.0/Ystretch
    ax2 = fig.add_axes([pos_x_window, pos_y_window, ax2sizeX, ax2sizeY/fig_ratio],frameon=False)
    curve = beta_dist(x,pair[0]+1.0, pair[1])
    ax2.axis([0,1,0,Ystretch])
    ax2.fill_between(x, curve, y2=0, edgecolor='None', color='blue',alpha=0.3)
    ax2.set_xticks([])
    ax2.set_yticks([])
    return ax2

pos.pt_x = 1.0
pos.pt_y = 1.0

pairs = []
ax.grid(True)

pos.ax_number = 0
pos.ax_vector = []

# Function to be called when mouse is clicked
def on_click(event):
    if event.xdata<pos.x_max and event.xdata>pos.x_min and \
       event.ydata<pos.y_max and event.ydata>pos.y_min:
        pos.ax_number += 1
        pos.ax_vector.append(insert_window(ax,pos,(event.xdata,event.ydata),x))
        fig.canvas.draw()

def erase_axis(event):
    if pos.ax_number > 0:
        # print('you pressed', event.key, event.xdata, event.ydata)
        if event.key == ' ':
            fig.delaxes(pos.ax_vector[pos.ax_number-1])
            pos.ax_vector = pos.ax_vector[:-1]
            pos.ax_number -= 1
        if event.key == 'a':
            while pos.ax_number > 0:
                fig.delaxes(pos.ax_vector[pos.ax_number-1])
                pos.ax_vector = pos.ax_vector[:-1]
                pos.ax_number -= 1
        plt.draw()

def dynamic_shape(event):
    if event.xdata<pos.x_max and event.xdata>pos.x_min and \
       event.ydata<pos.y_max and event.ydata>pos.y_min:
        plt.title("x={:f}, y={:f}".format(event.xdata,event.ydata))
        fig.canvas.draw()
        
# click on the figure to draw insets
# press spacebar to erase last inset
# press 'a' to erase all insets

# Connect the click function to the button press event
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('key_press_event', erase_axis)
betashape = MouseBeta(ax, color='blue', lw=3)
fig.canvas.mpl_connect('motion_notify_event', betashape.show_beta)
# fig.canvas.mpl_connect('motion_notify_event', dynamic_shape)

plt.show()