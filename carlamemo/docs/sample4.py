import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import sample3 as s3

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
max_speed = 100.0
pid = s3.PID(0.05, 0, 0)
speeds = []
speed = 0
throttle = 0.0
for time in range(0, 1000):
    pid.update_speed_error(speed, max_speed)
    throttle = pid.total_error()
    speed = speed + throttle
    speeds.append(speed)

plt.axhline(max_speed, color="b", linestyle="--")  
plt.ylim(0, max_speed + 10)
l, = plt.plot(speeds, lw=2, color='red')

axcolor = 'lightgoldenrodyellow'
axKp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
axKi = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axKd = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)

sKp = Slider(axKp, 'Kp', 0.0001, 10.0, valinit=0.05)
sKi = Slider(axKi, 'Ki', 0.0001, 10.0, valinit=0)
sKd = Slider(axKd, 'Kd', 0.0001, 10.0, valinit=0)


def update(val):
    kp = sKp.val
    ki = sKi.val
    kd = sKd.val
    
    pid = s3.PID(kp, ki, kd)

    speeds = []
    speed = 0
    throttle = 0.0
    old_speed = 0
    for time in range(0, 1000):
        pid.update_speed_error(speed, max_speed)
        throttle = pid.total_error()
        print("throttle = {} speed = {}".format(throttle, speed))
        speed = speed + throttle
        speeds.append(speed)
        if old_speed < speed:
            old_speed = speed

        if old_speed > max_speed:
            plt.ylim(0, old_speed + 10)
        else:
            plt.ylim(0, max_speed + 10)

    l.set_ydata(speeds)
    fig.canvas.draw_idle()
sKp.on_changed(update)
sKi.on_changed(update)
sKd.on_changed(update)

#resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
#button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


#def reset(event):
#    sfreq.reset()
#    samp.reset()
#button.on_clicked(reset)

#rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
#radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)


#def colorfunc(label):
#    l.set_color(label)
#    fig.canvas.draw_idle()
#radio.on_clicked(colorfunc)

plt.show()