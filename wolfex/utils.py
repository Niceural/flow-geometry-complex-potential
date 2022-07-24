"""This module declares two miscellaneous functions.
"""

import os.path
import csv
import cmath
from scipy.integrate import solve_ivp
from flow_element import *
import plot
import numpy as np

def read_flow_elements_file(path, log):
    """This function reads a formatted file declaring the flow elements.
    It parses the file and instantiates a :class:`flow_element.Flow` object containing the flow elements
    
    :param path: Path to the file containing the elements parameters.
    :type path: str
    :param log: Prints the flow elements' parameters to console if set to true.
    :type log: bool
    :return: Instance of :class:`flow_element.Flow` containing the flow elements.
    :rtype: class:`flow_element.Flow`
    """

    if log: print(f"Reading \"{path}\"...")
    flow = Flow()

    # checking that the file exists
    if not os.path.isfile(path):
        print(f"ERROR: File \"{path}\" does not exist.")
        return

    # reading file
    try:
        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            i = 0
            wall_slopes = []
            wall_intercepts = []
            for row in csv_reader:
                i += 1
                # creates flow element instances and pushes them onto flow's list
                if row[0] == 'u':
                    angle = float(row[2]) * cmath.pi / 180
                    el = UniformStream(float(row[1]), angle, i)
                    flow.add_element(el)
                elif row[0] == 's':
                    el = Source(float(row[1]), complex(float(row[2]), float(row[3])), i)
                    flow.add_element(el)
                elif row[0] == 'v':
                    el = Vortex(float(row[3]), complex(float(row[1]), float(row[2])), i)
                    flow.add_element(el)
                elif row[0] == 'c':
                    angle = float(row[6]) * cmath.pi / 180
                    el = Cylinder(float(row[4]), complex(float(row[1]), float(row[2])), float(row[3]), float(row[5]), angle, i)
                    flow.add_element(el)
                elif row[0] == 'j':
                    angle = float(row[6]) * cmath.pi / 180
                    el = JoukowskiElement(complex(float(row[1]), float(row[2])), float(row[3]), float(row[4]), float(row[5]), angle, float(row[7]), i)
                    flow.add_element(el)
                elif row[0] == 'w':
                    wall_slopes.append(float(row[1]))
                    wall_intercepts.append(float(row[2]))
                else:
                    raise ValueError
            file.close()
            if wall_slopes:
                for el in flow:
                    el.add_walls(wall_slopes, wall_intercepts) # works
    except ValueError:
        print(f"ERROR: Invalid flow element type in \"{path}\".")
    except: 
        print(f"ERROR: Failed to read file \"{path}\". Please check that the file exists and check the format.")

    if log: flow.print_parameters()
    return flow



def solve_velocity_ode(flow, t_span=(0., 10.), video_folder=""):
    """This function calls `scipy.integrate.solve_ivp <https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html#scipy.integrate.solve_ivp>`_ to solve the system of ODEs of the flow.
    The ODEs are given by the derivative of the complex potential of the flow.

    :param flow: instance of :class:`flow_element.Flow` containing the flow elements
    :type flow: class:`flow_element.Flow`
    :param log: Prints to console if set to true
    :type log: bool
    :param t_span: Initial and final time limits, defaults to (0, 10)
    :type t_span: tuple, optional
    :param video_folder: If a folder path is given, the :func:`plot.velocity_stream_lines` function will be called and a plot will be saved at each iteration, defaults to ""
    :type video_folder: str, optional
    :return: Object returned by `scipy.integrate.solve_ivp <https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html#scipy.integrate.solve_ivp>`_
    :rtype: Bunch object
    """

    def velocity_ode(t, xy, flow, folder_path):
        if folder_path != "":
            file_name = os.path.join(folder_path, f"{t*1000}.jpg")
            plot.velocity_stream_lines(flow, file_name=file_name, show=False, iterative=True, x_lim=[-2, 12], y_lim=[-2, 2])

        # initialization
        dxydt = np.zeros_like(xy)
        z = 1j * xy[1::2]
        z += xy[::2]

        # updating the location of the elements
        i = 0
        for el in flow:
            el.set_z(complex(xy[i], xy[i+1]))
            i+=2

        # compute derivative complex potential
        dFdz = flow.derivative_complex_potential(z)
        dxydt[::2] = dFdz.real
        dxydt[1::2] = -dFdz.imag

        return dxydt

    # initial conditions
    xy0 = np.zeros(flow.num_of_elements() * 2)
    elid = 0
    for el in flow:
        pos = el.z_initial()
        xy0[elid] = pos.real
        elid += 1
        xy0[elid] = pos.imag
        elid += 1

    # solve ode
    y = solve_ivp(velocity_ode, t_span, xy0, t_eval=np.linspace(t_span[0], t_span[1], 100), max_step=0.1, args=(flow, video_folder))
    
    return y
