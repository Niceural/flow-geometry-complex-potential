**************************
:mod:`flow_element` module
**************************

.. automodule:: flow_element

.. currentmodule:: flow_element

:class:`FlowElement` abstract parent class
##########################################

.. autoclass:: FlowElement

    .. automethod:: __init__
    
    .. automethod:: print_parameters
    
    .. automethod:: name
    
    .. automethod:: id

    .. automethod:: add_walls

    .. automethod:: z_initial

    .. automethod:: z_current

    .. automethod:: set_z

    .. automethod:: complex_potential

    .. automethod:: complex_potential_symmetric

    .. automethod:: derivative_complex_potential

    .. automethod:: derivative_complex_potential_symmetric

:class:`UniformStream` element
##############################

.. autoclass:: UniformStream

    .. automethod:: __init__
    
    .. automethod:: print_parameters
    
    .. automethod:: name
    
    .. automethod:: id

    .. automethod:: z_initial

    .. automethod:: z_current

    .. automethod:: set_z

    .. automethod:: complex_potential

    .. automethod:: derivative_complex_potential

:class:`Source` element
#######################

.. autoclass:: Source

    .. automethod:: __init__
    
    .. automethod:: print_parameters
    
    .. automethod:: name
    
    .. automethod:: id

    .. automethod:: add_walls

    .. automethod:: z_initial

    .. automethod:: z_current

    .. automethod:: set_z

    .. automethod:: complex_potential

    .. automethod:: complex_potential_symmetric

    .. automethod:: derivative_complex_potential

    .. automethod:: derivative_complex_potential_symmetric

:class:`Vortex` element
#######################

.. autoclass:: Vortex

    .. automethod:: __init__
    
    .. automethod:: print_parameters
    
    .. automethod:: name
    
    .. automethod:: id

    .. automethod:: add_walls

    .. automethod:: z_initial

    .. automethod:: z_current

    .. automethod:: set_z

    .. automethod:: complex_potential

    .. automethod:: complex_potential_symmetric

    .. automethod:: derivative_complex_potential

:class:`Cylinder` element
#########################

.. autoclass:: Cylinder

    .. automethod:: __init__
    
    .. automethod:: print_parameters
    
    .. automethod:: name
    
    .. automethod:: id

    .. automethod:: z_initial

    .. automethod:: z_current

    .. automethod:: set_z

    .. automethod:: complex_potential

    .. automethod:: derivative_complex_potential

:class:`JoukowskiElement` element
#################################

.. autoclass:: JoukowskiElement

    .. automethod:: __init__
    
    .. automethod:: print_parameters
    
    .. automethod:: name
    
    .. automethod:: id

    .. automethod:: z_initial

    .. automethod:: z_current

    .. automethod:: set_z

    .. automethod:: complex_potential

    .. automethod:: derivative_complex_potential

:class:`Flow` container class
#############################

.. autoclass:: Flow

    .. automethod:: __init__
    
    .. automethod:: print_parameters

    .. automethod:: empty

    .. automethod:: num_of_elements

    .. automethod:: add_element

    .. automethod:: remove_element
    
    .. automethod:: pop_element
    
    .. automethod:: complex_potential

    .. automethod:: derivative_complex_potential

:class:`Walls` class
####################

.. autoclass:: Walls

    .. automethod:: __init__

    .. automethod:: __find_symmetric

    .. automethod:: complex_potential

    .. automethod:: derivative_complex_potential