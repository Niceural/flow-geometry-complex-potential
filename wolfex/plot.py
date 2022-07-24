"""This module declares the functions used by this project to create plots.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.colors as colors
import os
from moviepy.editor import ImageClip, ImageSequenceClip

def velocity_stream_lines(flow, x_lim=None, y_lim=None, x_num_points=50, y_num_points=50,
        fig_num=1, fig_size=(6, 6), file_name="", plot_title="Velocity stream lines", show=True, iterative=False):
    """This function creates a `matplotlib.pyplot.streamplot <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.streamplot.html#matplotlib-pyplot-streamplot>`_ of the velocity of the flow.
    The velocity corresponds to the real and imaginary parts of the derivative of the complex potential of the flow.

    :param flow: Instance of :class:`flow_element.Flow` containing the flow elements
    :type flow: :class:`flow_element.Flow`
    :param x_lim: plotting limit of x axis [x min, x max]
    :type x_lim: list, optional
    :param y_lim: plotting limit of y axis [y min, y max]
    :type y_lim: list, optional
    :param x_num_points: Number of points in the meshgrid
    :type x_num_points: int, optional
    :param y_num_points: Number of points in the meshgrid
    :type y_num_points: int, optional
    :param fig_num: Figure number
    :type fig_num: int, optional
    :param fig_size: Figure size
    :type fig_size: tuple, optional
    :param file_name: If the string is not empty the figure is saved in that file
    :type file_name: str, optional
    :param plot_title: Custom plot title
    :type plot_title: str, optional
    :param show: If set to False doesn't show the plot
    :type show: bool, optional
    :param iterative: If set to true, clears the plot to update
    :type iterative: bool, optional
    """

    # plotting limits and number of points
    if x_lim is None:
        x_lim = plotting_limit(flow, False)
    if y_lim is None:
        y_lim = plotting_limit(flow, True)

    # getting the grid
    x_range = np.linspace(x_lim[0], x_lim[1], x_num_points)
    y_range = np.linspace(y_lim[0], y_lim[1], y_num_points)
    x, y = np.meshgrid(x_range, y_range)

    # getting the velocity values
    z = x + 1j * y
    dFdz = flow.derivative_complex_potential(z)
    u, v = dFdz.real, -dFdz.imag

    # declares figure
    fig = plt.figure(fig_num, figsize=fig_size)

    # plot the velocity stream lines
    plt.grid(True, zorder=1)
    plt.streamplot(x, y, u, v, density=1.5, linewidth=1, color='k', zorder=2)

    # plot the elements positions
    for el in flow:
        pos = el.z_current()
        plt.scatter(pos.real, pos.imag, label=f"{el.id()}: {el.name()}", zorder=3, marker='+', s=50)
    
    # plot format
    plt.legend(loc=1)
    plt.axis("scaled")
    plt.xlabel("Re(z)")
    plt.ylabel("Im(z)")
    plt.title(plot_title)

    if file_name != "":
        plt.savefig(file_name)
    if show:
        plt.show()
    if iterative:
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()

def velocity_colorplot(flow, x_lim=None, y_lim=None, x_num_points=100, y_num_points=100,
        fig_num=2, fig_size=(6, 6), file_name="", plot_title="Velocity color plot", show=True, iterative=False):
    """This function creates a `matplotlib.pyplot.imshow <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html#matplotlib-pyplot-imshow>`_ plot of the magnitude of the velocity of the flow.
    The magnitude of the velocity is obtained by taking the modulus of the derivative of the complex potential.

    :param flow: Instance of :class:`flow_element.Flow` containing the flow elements
    :type flow: :class:`flow_element.Flow`
    :param x_lim: plotting limit of x axis [x min, x max]
    :type x_lim: list, optional
    :param y_lim: plotting limit of y axis [y min, y max]
    :type y_lim: list, optional
    :param x_num_points: Number of points in the meshgrid
    :type x_num_points: int, optional
    :param y_num_points: Number of points in the meshgrid
    :type y_num_points: int, optional
    :param fig_num: Figure number
    :type fig_num: int, optional
    :param fig_size: Figure size
    :type fig_size: tuple, optional
    :param file_name: If the string is not empty the figure is saved in that file
    :type file_name: str, optional
    :param plot_title: Custom plot title
    :type plot_title: str, optional
    :param show: If set to False doesn't show the plot
    :type show: bool, optional
    :param iterative: If set to true, clears the plot to update
    :type iterative: bool, optional
    """

    # plotting limits and number of points
    if x_lim is None:
        x_lim = plotting_limit(flow, False)
    if y_lim is None:
        y_lim = plotting_limit(flow, True)

    # getting the grid
    x_range = np.linspace(x_lim[0], x_lim[1], x_num_points)
    y_range = np.linspace(y_lim[0], y_lim[1], y_num_points)
    x, y = np.meshgrid(x_range, y_range)

    # getting the velocity values
    z = x + 1j * y
    dFdz = flow.derivative_complex_potential(z)
    U_mag = abs(dFdz)

    # declares figure
    fig = plt.figure(fig_num, figsize=fig_size)

    # plot the velocity color plot
    grey_stuff = plt.imshow(U_mag, origin="lower", extent=(x_lim[0], x_lim[1], y_lim[0], y_lim[1]), cmap="gray", norm=colors.LogNorm())
    plt.colorbar(grey_stuff)
    # x_step, y_step = int(x_num_points / 13), int(y_num_points / 13)
    # quiv = plt.quiver(x[5::x_step, 5::y_step ], y[5::x_step, 5::y_step ], u[5::x_step, 5::y_step ], v[5::x_step, 5::y_step ], pivot="middle", color='c')
    # plt.quiverkey(quiv, 0.95, 1.04, 1, "1 m/s") # for scale at the top

    # plot the elements positions
    for el in flow:
        pos = el.z_current()
        plt.scatter(pos.real, pos.imag, label=f"{el.id()}: {el.name()}", zorder=3, marker='+', s=50)

    # plot format
    plt.legend(loc=1)
    plt.axis("scaled")
    plt.xlabel("Re(z)")
    plt.ylabel("Im(z)")
    plt.title(plot_title)

    if file_name != "":
        plt.savefig(file_name)
    if show:
        plt.show()
    if iterative:
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()

def velocity_potential(flow, x_lim=None, y_lim=None, x_num_points=50, y_num_points=50, 
                    file_name="", plot_title="Velocity potential", show=True, fig_size=(6, 6), fig_num=3, iterative=False):
    """This function creates a `matplotlib.pyplot.contour <https://matplotlib.org/3.5.0/api/_as_gen/matplotlib.pyplot.contour.html#matplotlib.pyplot.contour>`_ plot of the velocity potential.
    The velocity potential is obtained by taking the real part of the complex potential of the flow.

    :param flow: Instance of :class:`flow_element.Flow` containing the flow elements
    :type flow: :class:`flow_element.Flow` 
    :param x_lim: plotting limit of x axis [x min, x max]
    :type x_lim: list, optional
    :param y_lim: plotting limit of y axis [y min, y max]
    :type y_lim: list, optional
    :param x_num_points: Number of points in the meshgrid
    :type x_num_points: int, optional
    :param y_num_points: Number of points in the meshgrid
    :type y_num_points: int, optional
    :param fig_num: Figure number
    :type fig_num: int, optional
    :param fig_size: Figure size
    :type fig_size: tuple, optional
    :param file_name: If the string is not empty the figure is saved in that file
    :type file_name: str, optional
    :param plot_title: Custom plot title
    :type plot_title: str, optional
    :param show: If set to False doesn't show the plot
    :type show: bool, optional
    :param iterative: If set to true, clears the plot to update
    :type iterative: bool, optional
    """

    # plotting limits and number of points
    if x_lim is None:
        x_lim = plotting_limit(flow, False)
    if y_lim is None:
        y_lim = plotting_limit(flow, True)

    # getting the grid
    x_range = np.linspace(x_lim[0], x_lim[1], x_num_points)
    y_range = np.linspace(y_lim[0], y_lim[1], y_num_points)
    x, y = np.meshgrid(x_range, y_range)

    # getting phi
    z = x + 1j * y
    Fz = flow.complex_potential(z)
    phi = Fz.real

    # declares figure
    fig = plt.figure(fig_num, figsize=fig_size)

    # plot the velocity potential
    plt.grid(True, zorder=1)
    levels = np.linspace(np.amin(phi), np.amax(phi), 20)
    phi_contour = plt.contour(x, y, phi, zorder=2, levels=levels)
    fig.colorbar(phi_contour)

    # plot the elements positions
    for el in flow:
        pos = el.z_current()
        plt.scatter(pos.real, pos.imag, label=f"{el.id()}: {el.name()}", zorder=3, marker='+', s=50)

    # plot format
    plt.legend(loc=1)
    plt.axis("scaled")
    plt.xlabel("Re(z)")
    plt.ylabel("Im(z)")
    plt.title(plot_title)

    if file_name != "":
        plt.savefig(file_name)
    if show:
        plt.show()
    if iterative:
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()

def stream_function(flow, x_lim=None, y_lim=None, x_num_points=50, y_num_points=50, 
                    file_name="", plot_title="Stream function", show=True, fig_size=(6, 6), fig_num=3, iterative=False):
    """This function creates a `matplotlib.pyplot.contour <https://matplotlib.org/3.5.0/api/_as_gen/matplotlib.pyplot.contour.html#matplotlib.pyplot.contour>`_ plot of the stream function of the flow.
    The stream function is obtained by taking the imaginary part of the complex potential of the flow.

    :param flow: Instance of :class:`flow_element.Flow` containing the flow elements
    :type flow: :class:`flow_element.Flow`
    :param x_lim: plotting limit of x axis [x min, x max]
    :type x_lim: list, optional
    :param y_lim: plotting limit of y axis [y min, y max]
    :type y_lim: list, optional
    :param x_num_points: Number of points in the meshgrid
    :type x_num_points: int, optional
    :param y_num_points: Number of points in the meshgrid
    :type y_num_points: int, optional
    :param fig_num: Figure number
    :type fig_num: int, optional
    :param fig_size: Figure size
    :type fig_size: tuple, optional
    :param file_name: If the string is not empty the figure is saved in that file
    :type file_name: str, optional
    :param plot_title: Custom plot title
    :type plot_title: str, optional
    :param show: If set to False doesn't show the plot
    :type show: bool, optional
    :param iterative: If set to true, clears the plot to update
    :type iterative: bool, optional
    """

    # plotting limits and number of points
    if x_lim is None:
        x_lim = plotting_limit(flow, False)
    if y_lim is None:
        y_lim = plotting_limit(flow, True)

    # getting the grid
    x_range = np.linspace(x_lim[0], x_lim[1], x_num_points)
    y_range = np.linspace(y_lim[0], y_lim[1], y_num_points)
    x, y = np.meshgrid(x_range, y_range)

    # getting phi
    z = x + 1j * y
    Fz = flow.complex_potential(z)
    phi = Fz.imag

    # declares figure
    fig = plt.figure(fig_num, figsize=fig_size)

    # plot the stream function
    plt.grid(True, zorder=1)
    levels = np.arange(np.amin(phi), np.amax(phi), (np.amax(phi) - np.amin(phi)) / 20)
    phi_contour = plt.contour(x, y, phi, zorder=2, levels=levels)
    fig.colorbar(phi_contour)

    # plot the elements positions
    for el in flow:
        pos = el.z_current()
        plt.scatter(pos.real, pos.imag, label=f"{el.id()}: {el.name()}", zorder=3, marker='+', s=50)

    # plot format
    plt.legend(loc=1)
    plt.axis("scaled")
    plt.xlabel("Re(z)")
    plt.ylabel("Im(z)")
    plt.title(plot_title)

    if file_name != "":
        plt.savefig(file_name)
    if show:
        plt.show()
    if iterative:
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()

def trajectory(flow, out, x_lim=None, y_lim=None,
                file_name="", plot_title="Trajectory", show=True, fig_size=(6, 6)):
    """This function creates a `matplotlib.pyplot.plot <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot>`_ plot of the trajectory of the flow elements.
    The positions of the flow elements are obtained from the solution of the ODEs returned by :func:`utils.solve_velocity_ode`.
    
    :param flow: Instance of :class:`flow_element.Flow` containing the flow element
    :type flow: :class:`flow_element.Flow`
    :param out: Result of the the numerical analysis
    :type out: numpy.array
    :param x_lim: plotting limit of x axis [x min, x max]
    :type x_lim: list, optional
    :param y_lim: plotting limit of y axis [y min, y max]
    :type y_lim: list, optional
    :param file_name: If the string is not empty the figure is saved in that file
    :type file_name: str, optional
    :param plot_title: Custom plot title
    :type plot_title: str, optional
    :param show: If set to False doesn't show the plot
    :type show: bool, optional
    :param fig_size: Figure size
    :type fig_size: tuple, optional
    """

    # plotting limits
    if x_lim is None:
        x_lim = [np.amin(out[::2][:]) - 2., np.amax(out[::2][:]) + 2.]
    if y_lim is None:
        y_lim = [np.amin(out[1::2, :]) - 2., np.amax(out[1::2, :]) + 2.]

    # creating the plot
    fig = plt.figure(figsize=fig_size)
    axes = plt.axes()
    axes.set_xlim(int(x_lim[0]), int(x_lim[1]))
    axes.set_ylim(int(y_lim[0]), int(y_lim[1]))

    # plots the trajectory
    elid = 0
    for el in flow:
        axes.plot(out[elid, :], out[elid+1, :], label=f"{el.id()}: {el.name()}", zorder=2)
        axes.scatter([el.z_initial().real, el.z_current().real], [el.z_initial().imag, el.z_current().imag], zorder=3)
        elid += 2

    # plot format
    plt.grid(True, zorder=1)
    #plt.axis("scaled")
    plt.legend(loc=1)
    plt.xlabel("Re(z)")
    plt.ylabel("Im(z)")
    plt.title(plot_title)

    if file_name != "":
        plt.savefig(file_name)
    if show:
        plt.show()

def animated_trajectory(flow, out, x_lim=None, y_lim=None,
                        file_name="", plot_title="Animated trajectory", show=True, fig_size=(6, 6)):
    """This function creates a `matplotlib.animation <https://matplotlib.org/stable/api/animation_api.html#module-matplotlib.animation>`_ plot of the trajectory of the flow elements.
    The positions of the flow elements are obtained from the solution of the ODEs returned by :func:`utils.solve_velocity_ode`.
    
    :param flow: Instance of :class:`flow_element.Flow` containing the flow element
    :type flow: :class:`flow_element.Flow`
    :param out: Result of the the numerical analysis
    :type out: np.array
    :param x_lim: plotting limit of x axis [x min, x max]
    :type x_lim: list, optional
    :param y_lim: plotting limit of y axis [y min, y max]
    :type y_lim: list, optional
    :param file_name: If the string is not empty the figure is saved in that file
    :type file_name: str, optional
    :param plot_title: Custom plot title
    :type plot_title: str, optional
    :param show: If set to False doesn't show the plot
    :type show: bool, optional
    :param fig_size: Figure size
    :type fig_size: tuple, optional
    """
    # https://stackoverflow.com/questions/48013749/matplotlib-animation-of-streamplot-of-bifurcation

    # work out plot limits
    if x_lim is None:
        x_lim = [np.amin(out[::2, :]) - 2., np.amax(out[::2, :]) + 2.]
    if y_lim is None:
        y_lim = [np.amin(out[1::2, :]) - 2., np.amax(out[1::2, :]) + 2.]

    # https://stackoverflow.com/questions/23049762/matplotlib-multiple-animate-multiple-lines
    fig = plt.figure()
    ax1 = plt.axes(xlim=(x_lim[0], x_lim[1]), ylim=(y_lim[0], y_lim[1]))
    # line, = ax1.plot([], [], lw=2)
    plt.xlabel("Re(z)")
    plt.ylabel("Im(z)")
    plt.title(plot_title)
    plt.grid(True, zorder=1)
    #plt.axis("scaled")

    temp, number_of_iterations = out.shape
    lines = []
    for el in flow:
        lobj = ax1.plot([], [], lw=2, label=f"{el.id()}: {el.name()}")[0]
        lines.append(lobj)

    def init():
        for (el, line) in zip(flow, lines):
            line.set_data([], [])
            line.set(label=f"{el.id()}: {el.name()}")
        return lines

    x = np.zeros(shape=(flow.num_of_elements(), number_of_iterations))
    y = np.zeros(shape=(flow.num_of_elements(), number_of_iterations))

    def animate(i):
        elid = 0
        for (el, line) in zip(flow, lines):
            x[elid, i] = out[elid*2, i]
            y[elid, i] = out[elid*2+1, i]
            line.set_data(x[elid, 0:i], y[elid, 0:i])
            line.set(label=f"{el.id()}: {el.name()}")
            elid += 1
        return lines

    anim = FuncAnimation(fig, animate, init_func=init, frames=number_of_iterations, interval=50, blit=True)
    plt.legend(loc=1)
    plt.show()
    writergif = PillowWriter(fps=20)
    anim.save(file_name, writer=writergif)


def from_dir_to_video(dir_with_imgs, output_video):
    """This function takes a directory containing images and creates a video from the images.

    :param dir_with_imgs: Path to directory containing images
    :type dir_with_imgs: str
    :param output_video: Path the video should be saved at
    :type output_video: str
    """
    # https://youtu.be/m6chqKlhpPo?t=2147
    
    directory = {}
    for root, dirs, files in os.walk(dir_with_imgs):
        for fname in files: 
            filepath = os.path.join(root, fname)
            try: 
                key = float(fname.replace (".jpg", ""))
            except: 
                key = None
            if key != None:
                directory[key] = filepath

    new_paths = []
    for k in sorted(directory.keys()):
        filepath = directory[k]
        new_paths.append(filepath)

    my_clips = []
    for path in list(new_paths):
        frame = ImageClip(path)
        my_clips.append(frame.img)

    clip = ImageSequenceClip(my_clips, fps=10)
    clip.write_videofile(output_video)

def plotting_limit(flow, isY, margin=2.0):
    """Work out the plot limits

    :param flow: Instance of :class:`flow_element.Flow` containing the flow element
    :type flow: class:`flow_element.Flow`
    :param isY: Works out y plot limits if set to true, x plot limits if false
    :type isY: bool
    :param margin: Value to add/substract to max/min values, defaults to 2.0
    :type margin: float, optional
    :return: [max, min] plot limits
    :rtype: list
    """

    out = [0.0, 0.0]
    for el in flow:
        if isY:
            coord = el.z_current().imag
        else:
            coord = el.z_current().real
        if coord < out[0]:
            out[0] = coord
        elif out[1] < coord:
            out[1] = coord

    out[0] -= margin
    out[1] += margin

    return out
