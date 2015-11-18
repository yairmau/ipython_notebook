import matplotlib
matplotlib.use('AGG')
import numpy as np
import matplotlib.pyplot as plt
import os

# https://bentrubewriter.wordpress.com/2012/04/26/fractals-you-can-draw-the-hilbert-curve-or-what-the-labyrinth-really-looked-like/
# http://mathforum.org/advanced/robertd/lsys2d.html

def apply_rules(s):
    s=s.replace("a","-Bf+AfA+fB-")
    s=s.replace("b","+Af-BfB-fA+")
    return s.lower()

axiom = "a"
n=6
rescale=1.0+0*2.0**(-n)
# displacements, ordered in a counter-clockwise direction
dxdy = np.array([[ 1, 0],
                 [ 0, 1],
                 [-1, 0],
                 [ 0,-1] ])
length = 2**n-1
margin = 0.05*length
domain = [0-margin,length+margin,0-margin,length+margin]
# m = np.round(rot(np.pi/2),1)
s = axiom
for i in np.arange(n):
    s = apply_rules(s)
# print s

make_movie=True
plt.ion()
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
ax.axis('off')
ax.axis(domain)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title(r"$n = {:d}$".format(n))
plt.show()
p = [0,0]
frame_names = []
counter=0
s=s.replace("a","")
s=s.replace("b","")
counter=0
p = np.array([[0.0,0.0]])
frac_plot, = plt.plot(p[:,0],p[:,1],color="black")
for i,c in enumerate(s):
    print("{:d}/{:d}".format(i,len(s)))
    if c == '+': dxdy = np.roll(dxdy,+1,axis=0)
    if c == '-': dxdy = np.roll(dxdy,-1,axis=0)
    if c == 'f':
        p = np.vstack([p, 
                       [p[-1,0]+dxdy[0,0],p[-1,1]+dxdy[0,1]] ])
        frac_plot.set_data(p[:,0],p[:,1])
        fig.canvas.draw()
        if make_movie:
            fname = "_tmp{:05d}.png".format(counter)
            frame_names.append(fname)
            fig.savefig(fname,bbox_inches='tight',resolution=300)
        counter += 1
# plt.show()
# fig.savefig("h.png")
if make_movie:
    frames = "_tmp%5d.png"
    movie_command = "mencoder mf://*.png -mf fps=24:type=png --ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -o hil{:d}.avi".format(n)
    
    # we might have other .png figures in the directory
    # in this case, use the code below
    f = open("png_list.txt", "w")
    for i in frame_names:
        f.write(i+"\n")
    f.close()
    movie_command = "mencoder mf://@png_list.txt -mf fps=24:type=png -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -o hil{:d}.avi".format(n)
    
    err=os.system(movie_command)
    if err!=0:
        raise RuntimeError("Couldn't run mencoder.  Data in tmp*.png files")
    for fname in frame_names:
        os.remove(fname)

