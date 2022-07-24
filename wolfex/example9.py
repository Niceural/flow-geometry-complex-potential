"""
Example 9: Pair of Counter Rotating Vortices with Vertical Wall
###############################################################

In this example we will simulate a pair of counter-rotating vortices with a vertical wall at :math:`x = 5`.
The parameters are presented in the table below.
To run this example enter the following command in your terminal in the project root: 

.. code-block:: console

    $ make example9

+-----------+-------------+-------------+--------------+
|           | x position  | y position  | Circulation  |
+===========+=============+=============+==============+
| Vortex 1  | 0.0         | 0.5         | 6.3          |
+-----------+-------------+-------------+--------------+
| Vortex 2  | 0.0         | -0.5        | -6.3         |
+-----------+-------------+-------------+--------------+

"""

import os.path
import utils
import plot

# config variables
log = True # set to True to print values to console
initialPlot = True # set to True to make the initial plots
trajectoryPlot = True # set to True to make the trajectory plots
output_folder = "./data/example9/" # folder where the plots and results will be saved
flow_elements_file = "./data/example9/flow_elements.csv" # file declaring the flow elements

print("\nExample 9: Pair of counter-rotating vortices with vertical wall...\n")

# read the flow elements file and create the elements
flow = utils.read_flow_elements_file(flow_elements_file, log)

# plot initial flow condition
if initialPlot:
    if log: print("\nPlotting initial velocity stream lines...")
    plot.velocity_stream_lines(flow, file_name=os.path.join(output_folder, "initial_velocity_stream_lines.jpg"), plot_title="Initial Velocity Stream Lines", x_lim=[-2, 15], y_lim=[-4, 4])
    if log: print("Plotting initial velocity color plot...")
    plot.velocity_colorplot(flow, file_name=os.path.join(output_folder, "initial_velocity_colorplot.jpg"), plot_title="Initial Velocity Color Plot", x_lim=[-2, 15], y_lim=[-4, 4])
    if log: print("Plotting initial velocity potential...")
    plot.velocity_potential(flow, file_name=os.path.join(output_folder, "initial_velocity_potential.jpg"), plot_title="Initial Velocity Potential", x_lim=[-2, 15], y_lim=[-4, 4])
    if log: print("Plotting initial stream function...")
    plot.stream_function(flow, file_name=os.path.join(output_folder, "initial_stream_function.jpg"), plot_title="Initial Stream Function", x_lim=[-2, 15], y_lim=[-4, 4])

# solve flow equations
print("\nSolving flow equations...")
out = utils.solve_velocity_ode(flow)
print("done")

# plot trajectory
if trajectoryPlot:
    if log: print("\nPlotting trajectory line plot...")
    plot.trajectory(flow, out.y, file_name=os.path.join(output_folder, "trajectory.jpg"))
    if log: print("\nPlotting animated trajectory line plot...")
    plot.animated_trajectory(flow, out.y, file_name=os.path.join(output_folder, "animated_trajectory.gif"))