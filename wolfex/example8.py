"""
Example 8: Joukowski Aerofoil
#############################

In this example we will visualize a Joukowski aerofoil
Please note that the :class:`flow_element.JoukowskiElement` has not been checked for correctness.
To run this example enter the following command in your terminal in the project root: 

.. code-block:: console

    $ make example8

"""

import os.path
import utils
import plot
from flow_element import Flow, FlowIterator

# config variables
log = True # set to True to print values to console
initialPlot = True # set to True to make the initial plots
trajectoryPlot = True # set to True to make the trajectory plots
output_folder = "./data/example8/" # folder where the plots and results will be saved
flow_elements_file = "./data/example8/flow_elements.csv" # file declaring the flow elements

print("\nExample 8: Joukowski aerofoil...\n")

# read the flow elements file and create the elements
flow = utils.read_flow_elements_file(flow_elements_file, log)

# plot initial flow condition
if initialPlot:
    if log: print("\nPlotting initial velocity stream lines...")
    plot.velocity_stream_lines(flow, file_name=os.path.join(output_folder, "initial_velocity_stream_lines.jpg"), plot_title="Initial Velocity Stream Lines")
    if log: print("Plotting initial velocity color plot...")
    plot.velocity_colorplot(flow, file_name=os.path.join(output_folder, "initial_velocity_colorplot.jpg"), plot_title="Initial Velocity Color Plot")
    if log: print("Plotting initial velocity potential...")
    plot.velocity_potential(flow, file_name=os.path.join(output_folder, "initial_velocity_potential.jpg"), plot_title="Initial Velocity Potential")
    if log: print("Plotting initial stream function...")
    plot.stream_function(flow, file_name=os.path.join(output_folder, "initial_stream_function.jpg"), plot_title="Initial Stream Function")

# solve flow equations
# print("\nSolving flow equations...")
# out = utils.solve_velocity_ode(flow, video_folder=os.path.join(output_folder, "video/"))
# print("done")

# # plot trajectory
# if trajectoryPlot:
#     if log: print("\nPlotting trajectory line plot...")
#     plot.trajectory(flow, out.y, file_name=os.path.join(output_folder, "trajectory.jpg"))
#     if log: print("\nPlotting animated trajectory line plot...")
#     plot.animated_trajectory(flow, out.y, file_name=os.path.join(output_folder, "animated_trajectory.gif"))
#     if log: print("\nCreating animation video...")
#     plot.from_dir_to_video(os.path.join(output_folder, "video/"), os.path.join(output_folder, "video.mp4"))