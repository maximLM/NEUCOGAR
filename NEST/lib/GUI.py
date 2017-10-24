import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets
import matplotlib
import matplotlib.colors as colors
import matplotlib.patches as patches
import matplotlib.mathtext as mathtext
import matplotlib.pyplot as plt
import matplotlib.artist as artist
import matplotlib.image as image
import numpy as np
import os
import pathlib
import re

from matplotlib.transforms import Bbox

current_name = 'NONE'
plt.ion()

class ItemProperties(object):
    def __init__(self, fontsize=14, labelcolor='black', bgcolor='yellow',
                 alpha=1.0):
        self.fontsize = fontsize
        self.labelcolor = labelcolor
        self.bgcolor = bgcolor
        self.alpha = alpha

        self.labelcolor_rgb = colors.to_rgba(labelcolor)[:3]
        self.bgcolor_rgb = colors.to_rgba(bgcolor)[:3]


class MenuItem(artist.Artist):
    parser = mathtext.MathTextParser("Bitmap")
    padx = 5
    pady = 5

    def __init__(self, fig, labelstr, props=None, hoverprops=None,
                 on_select=None):
        artist.Artist.__init__(self)

        self.set_figure(fig)
        self.labelstr = labelstr

        if props is None:
            props = ItemProperties()

        if hoverprops is None:
            hoverprops = ItemProperties()

        self.props = props
        self.hoverprops = hoverprops

        self.on_select = on_select

        x, self.depth = self.parser.to_mask(
            labelstr, fontsize=props.fontsize, dpi=fig.dpi)

        if props.fontsize != hoverprops.fontsize:
            raise NotImplementedError(
                'support for different font sizes not implemented')

        self.labelwidth = x.shape[1]
        self.labelheight = x.shape[0]

        self.labelArray = np.zeros((x.shape[0], x.shape[1], 4))
        self.labelArray[:, :, -1] = x/255.

        self.label = image.FigureImage(fig, origin='upper')
        self.label.set_array(self.labelArray)

        # we'll update these later
        self.rect = patches.Rectangle((0, 0), 1, 1)

        self.set_hover_props(False)

        fig.canvas.mpl_connect('button_release_event', self.check_select)

    def check_select(self, event):
        over, junk = self.rect.contains(event)
        if not over:
            return

        if self.on_select is not None:
            self.on_select(self)

    def set_extent(self, x, y, w, h):
        print(x, y, w, h)
        self.rect.set_x(x)
        self.rect.set_y(y)
        self.rect.set_width(w)
        self.rect.set_height(h)

        self.label.ox = x + self.padx
        self.label.oy = y - self.depth + self.pady/2.

        self.rect._update_patch_transform()
        self.hover = False

    def draw(self, renderer):
        self.rect.draw(renderer)
        self.label.draw(renderer)

    def set_hover_props(self, b):
        if b:
            props = self.hoverprops
        else:
            props = self.props

        r, g, b = props.labelcolor_rgb
        self.labelArray[:, :, 0] = r
        self.labelArray[:, :, 1] = g
        self.labelArray[:, :, 2] = b
        self.label.set_array(self.labelArray)
        self.rect.set(facecolor=props.bgcolor, alpha=props.alpha)

    def set_hover(self, event):
        'check the hover status of event and return true if status is changed'
        b, junk = self.rect.contains(event)

        changed = (b != self.hover)

        if changed:
            self.set_hover_props(b)

        self.hover = b
        return changed


class Menu(object):
    def __init__(self, fig, menuitems):
        self.figure = fig
        fig.suppressComposite = True

        self.menuitems = menuitems
        self.numitems = len(menuitems)

        maxw = max([item.labelwidth for item in menuitems])
        maxh = max([item.labelheight for item in menuitems])

        totalh = self.numitems*maxh + (self.numitems + 1)*2*MenuItem.pady

        x0 = 30
        y0 = 400

        width = maxw + 2*MenuItem.padx
        height = maxh + MenuItem.pady

        for item in menuitems:
            left = x0
            bottom = y0 - maxh - MenuItem.pady

            item.set_extent(left, bottom, width, height)

            fig.artists.append(item)
            y0 -= maxh + MenuItem.pady

        fig.canvas.mpl_connect('motion_notify_event', self.on_move)

    def on_move(self, event):
        draw = False
        for item in self.menuitems:
            draw = item.set_hover(event)
            if draw:
                self.figure.canvas.draw()
                break


fig = plt.figure()
fig.subplots_adjust(left=0.3)
props = ItemProperties(labelcolor='black', bgcolor='yellow',
                       fontsize=15, alpha=0.2)
hoverprops = ItemProperties(labelcolor='white', bgcolor='blue',
                            fontsize=15, alpha=0.2)
save_label = "Save Plots"

def full_extent(ax, pad=0.0):
    """Get the full extent of an axes, including axes labels, tick labels, and
    titles."""
    # For text objects, we need to draw the figure first, otherwise the extents
    # are undefined.
    ax.figure.canvas.draw()
    items = ax.get_xticklabels() + ax.get_yticklabels()
#    items += [ax, ax.title, ax.xaxis.label, ax.yaxis.label]
    items += [ax, ax.title]
    bbox = Bbox.union([item.get_window_extent() for item in items])

    return bbox.expanded(1.0 + pad, 1.0 + pad)

def save_ax(ax, dir_path, name):
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    print("THIS SHIT IS = " + str(extent))

    plt.savefig("{0}/{1}.png".format(dir_path, name), dpi=120, format='png', bbox_inches=extent)


def create_menu(items):
    menuitems = []

    for label in (items):
        def on_select(item):

            print('you selected %s' % item.labelstr)
            if item.labelstr == save_label:

                dir_path = os.path.dirname(os.path.realpath(__file__))
                dir_path += "/SavedPhoto"
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)

                # lower_ax.savefig("{0}/{1}.png".format(dir_path, current_name + "membrane_potential" ), dpi=120, format='png')
                # mid_ax.savefig("{0}/{1}.png".format(dir_path,   current_name + "rate"               ), dpi=120, format='png')
                # upper_ax.savefig("{0}/{1}.png".format(dir_path, current_name + "spikes"             ), dpi=120, format='png')
                save_ax(lower_ax, dir_path, current_name + "membrane_potential" );
                save_ax(mid_ax, dir_path, current_name + "rate"               );
                save_ax(upper_ax, dir_path, current_name + "spikes"             );

            else:
                change_plot(item.labelstr)

        item = MenuItem(fig, label, props=props, hoverprops=hoverprops,
                        on_select=on_select)
        menuitems.append(item)
    # menuitems.append(MenuItem(fig, save_label, props=props, hoverprops=hoverprops,
    #                     on_select=on_select))
    return Menu(fig, menuitems)



dir_path = os.path.dirname(os.path.realpath(__file__))

from os import listdir
from os.path import isfile, join
input_files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
names = set()
for name in input_files:
    if name.endswith('.gdf') or name.endswith('.dat'):
        arr = name.split('-')
        names.add(arr[0])

menu = create_menu(names)
MAX_LEN = 3
def change_plot(name_key):
    # print('changed to ' + file_name)
    global current_name
    current_name = name_key
    spike_time = dict()
    for file_name in [f for f in input_files if f.startswith(name_key) and f.endswith('.gdf')]:
        file = open(file_name, 'r')

        for s in file.readlines():
            ns = re.sub(r'(( +)|(\t+))', ' ', s)
            if ns == ' ' or ns == '': continue
            id, tim = ns.split()
            id = int(id)
            tim = float(tim)
            if not spike_time.__contains__(id):
                spike_time[id] = []
            spike_time[id].append(tim)
        file.close()
    potentials = dict()
    for file_name in [f for f in input_files if f.startswith(name_key) and f.endswith('.dat')]:
        file = open(file_name, 'r')
        for s in file.readlines():
            s = re.sub(r'(( +)|(\t+))', ' ', s)
            if s == ' ' or s == '':
                continue
            # print('s = ' + s)
            try :
                id, tim, vol = s.split()
            except ValueError:
                continue
            id = int(id)
            tim = float(tim)
            vol = float(vol)
            if potentials.__contains__(id):
                potentials[id].append([tim, vol])
            else:
                if len(potentials) < MAX_LEN:
                    potentials[id] = []
                    potentials[id].append([tim, vol])
        file.close()
    redraw(spike_time, potentials, name_key)

def redraw(spike_time, potentials, name):
    upper_ax.clear()
    upper_ax.set(title=name)
    merged = []
    rate_cnt = dict()
    for id in spike_time:
        for tim in sorted(spike_time[id]):
            merged.append([tim, id])
            if rate_cnt.__contains__(tim):
                rate_cnt[tim] += 1
            else:
                rate_cnt[tim] = 1
    merged = list(sorted(merged))
    x_data = [item[0] for item in merged]
    y_data = [item[1] for item in merged]
    upper_ax.scatter(x_data, y_data)

    lower_ax.clear()
    for id in potentials:
        timeline = potentials[id]
        timeline.sort(key=lambda x: x[0])
        lower_ax.plot([timeline[i][0] for i in range(len(timeline))], [timeline[i][1] for i in range(len(timeline))])

    mid_ax.clear()

    hist_binwidth = 3
    ptr = 0
    discrete_x = list(np.arange(np.amin(x_data) - 3 * hist_binwidth, np.amax(x_data) + 3 * hist_binwidth, hist_binwidth))
    discrete_y = [0 for i in discrete_x]
    # print("len = " + str(len(x_data)))
    n = len(discrete_x)
    for real_time in x_data:
        while real_time >= discrete_x[ptr + 1]:
            ptr += 1
            assert(ptr != n)
        discrete_y[ptr] += 1

    # print(discrete_x)
    mid_ax.grid(True)
    mid_ax.bar(discrete_x, discrete_y, width=hist_binwidth, color="blue", edgecolor="black")

    # if len(t_bins) == 0:
    #     plt.close()
    #     return "t_bins for {0} is empty".format(name)
    # n, bins = mid_ax.histogram(x_data, bins=t_bins)
    # num_neurons = len(np.unique(y_data))
    # heights = (1000 * n / (hist_binwidth * num_neurons))
    # mid_ax.bar(t_bins[:-1], heights, width=hist_binwidth, color="blue", edgecolor="black")
    # mid_ax.yticks([int(a) for a in np.linspace(0.0, int(max(heights) * 1.1) + 5, 4)])
    # mid_ax.grid(True)
    # mid_ax.draw()


    # mid_ax.bar([item[0] for item in xy_data], [item[1] for item in xy_data], width=0.5, color="blue", edgecolor="black")
    # mid_ax.bart([item[0] for item in xy_data], [item[1] for item in xy_data])
    upper_ax.set(ylabel="Neuron ID", title=name)
    mid_ax.set(ylabel='Rate(Hz)')
    lower_ax.set(xlabel="Time(ms)", ylabel="Membrane Potential")

    render()

# plt.show()
# quit()
def render():
    plt.pause(30)



lower_ax = fig.add_axes([0.5, 0.05, 0.4, 0.3])
mid_ax = fig.add_axes([0.5, 0.4, 0.4, 0.15], sharex=lower_ax)
upper_ax = fig.add_axes([0.5, 0.6, 0.4, 0.3], sharex=lower_ax)

render()
import time

while True:
    time.sleep(30)
    # render()
