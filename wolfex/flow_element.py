"""This module declares the :class:`flow_element.FlowElement` elements.
"""

import numpy as np
import cmath

class FlowElement:
    """This abstract class declares the methods a flow element should implement to be added to :class:`flow_element.Flow`.

    :raises NotImplementedError: This exception will be thrown if a child class has not overridden this class' methods prior to calling them.
    """

    def __init__(self):
        """Constructor method.

        :raises NotImplementedError: Thrown if this method is not overridden by the child class.
        """
        raise NotImplementedError

    #=========================================================
    #                                            general stuff
    #=========================================================
    def print_parameters(self):
        """Prints the flow element's parameters to console.

        :raises NotImplementedError: Thrown if this method is not overridden by the child class.
        """
        raise NotImplementedError

    def name(self):
        """Returns the name of the element (for plotting).

        :raises NotImplementedError: Thrown if this method is not overridden by the child class.
        """
        raise NotImplementedError

    def id(self):
        """Returns the id of the element (for plotting). An id corresponds to the line number the element is declared at in the `flow_elements.csv` file, starting from 1.

        :raises NotImplementedError: Thrown if this method is not overridden by the child class.
        """
        raise NotImplementedError

    def add_walls(self, slopes, intercepts):
        """This method adds one or two walls to the flow and has to be called on each flow elements.
        It will result in the addition of symmetric elements with respect to the walls with opposite circulation.
        The walls are defined by linear functions.
        See :class:`flow_element.Walls` for more information.

        :param slopes: Slopes of the linear functions describing the walls
        :type slopes: float
        :param intercepts: Intercepts of the linear functions describing the walls
        :type intercepts: float
        :raises NotImplementedError: Throws an exception if this method is called without being overridden.
        """
        raise NotImplementedError

    #=========================================================
    #                                                 position
    #=========================================================
    def z_initial(self):
        """Returns the initial position of the element.
        
        :raises NotImplementedError: Thrown if this method is not overridden by the child class.
        """
        raise NotImplementedError

    def z_current(self):
        """Returns the current position of the element.
        
        :raises NotImplementedError: Thrown if this method is not overridden by the child class.
        """
        raise NotImplementedError

    def set_z(self, z):
        """Sets the current position of the element.
        
        :param z: Current position of the element.
        :type z: complex
        :raises NotImplementedError: Thrown if this method is not overridden by the child class.
        """
        raise NotImplementedError

    #=========================================================
    #                                        complex potential
    #=========================================================
    def complex_potential(self, z):
        """Returns the complex potential :math:`w` of this element at point :math:`z`: :math:`w(z - z_{self}) = \phi + i \psi`, where :math:`\phi` is the velocity potential and :math:`\psi` is the stream function.
        
        :param z: Position where the complex potential :math:`w(z - z_{self})` is to be computed.
        :type z: complex
        :raises NotImplementedError: Thrown if this method is not overridden by the child class.
        """
        raise NotImplementedError

    def complex_potential_symmetric(self, z, z_symmetric):
        """Returns the complex potential :math:`w` of the images of self with respect to the walls.
        The symmetric elements will have a circulation of different sign to self element.
        
        :param z: Position where the complex potential :math:`w(z - z_{self})` is to be computed.
        :type z: complex
        :param z_symmetric: Position of the image of the element this method is being called on
        :type z_symmetric: complex
        :raises NotImplementedError: Thrown if this method is not overridden by the child class.
        """
        raise NotImplementedError

    #=========================================================
    #                             derivative complex potential
    #=========================================================
    def derivative_complex_potential(self, z):
        """Returns the derivative of the complex potential :math:`dw/dz` of this element at point :math:`z`: :math:`dw/dz = u - i v`, where :math:`u` and :math:`v` are the horizontal and vertical components of the velocity respectively.
        Please note that :math:`v` is given by :math:`- Im(dw/dz)`.

        :param z: Position where the derivative of the complex potential is to be computed, $dw/dz$
        :type z: complex
        :raises NotImplementedError: Thrown if this method is not overridden by the child class.
        """
        # !!! WATCH OUT FOR THE MINUS !!!
        raise NotImplementedError
    
    def derivative_complex_potential_symmetric(self, z, z_symmetric):
        """Returns the derivative of the complex potential :math:`dw/dz` of the images of self with respect to the walls.
        The symmetric elements will have a circulation of different sign to self element.

        :param z: Position where the derivative of the complex potential is to be computed
        :type z: complex
        :param z_symmetric: Position of the image of the element this method is being called on
        :type z_symmetric: complex
        :raises NotImplementedError: Thrown if this method is not overridden by the child class.
        """
        # !!! WATCH OUT FOR THE MINUS !!!
        raise NotImplementedError

class Walls():
    """This class adds walls to the flow.
    When called on a flow element, it adds flow elements of the same type (with opposite circulation) symmetric about the walls.
    A maximum of two walls can be added.
    Walls can only be added with :class:`flow_element.Source` and :class:`flow_element.Vortex`.
    """

    def __init__(self, slopes, intercepts):
        """Constructor methods
        To add a vertical wall, set the slope to inf and the intercept to the x coordinate.
        To add any other straight walls, enter the linear function defining the wall.

        :param slopes: Slopes of the linear functions defining the walls
        :type slopes: list
        :param intercepts: Intercepts of the linear functions defining the walls
        :type intercepts: list
        :raises ValueError: Throws an exception if more than two slopes are passed
        """
        if len(slopes) > 2 or len(intercepts) > 2:
            raise ValueError
        self.__slopes = slopes
        self.__intercepts = intercepts
        # slopes of the lines perpendicular to the walls
        self.__slopes_perpendicular = []
        for slope in self.__slopes:
            if (abs(slope) > 0.0001) and (slope != cmath.inf):
                self.__slopes_perpendicular.append(- 1. / slope)
    
    def __find_symmetric(self, z_element):
        """This private method computes the coordinates of the elements symmetric to z_element about the walls.

        :param z_element: Position of the element the symmetric are to be computed on.
        :type z_element: complex
        :return: List of positions of the symmetric elements
        :rtype: list of complex
        """
        x_el, y_el = z_element.real, z_element.imag
        z_images = []

        # find coordinates of symmetric points with respect to walls
        for i in range(len(self.__slopes)):
            # if the wall is vertical
            if self.__slopes[i] == cmath.inf:
                z_images.append(complex(2. * self.__intercepts[i] - x_el, y_el))
            # if the wall is horizontal
            elif abs(self.__slopes[i]) < 0.0001:
                z_images.append(complex(x_el, 2. * self.__intercepts[i] - y_el))
            else:
                # already have slopes of the lines perpendicular to the walls, now find the intercepts
                intercept_perpendicular = y_el - self.__slopes_perpendicular[i] * x_el
                # find coordinate of intersection point with wall and perpendicular line
                x_intersection = (intercept_perpendicular - self.__intercepts[i]) / (self.__slopes[i] - self.__slopes_perpendicular[i])
                y_intersection = self.__slopes[i] * x_intersection + self.__intercepts[i]
                # find coordinates of symmetric point wrt wall from midpoint formula
                z_images.append(complex(2. * x_intersection - x_el, 2. * y_intersection - y_el))

        # if 2 non parallel walls, there'll be a third image symmetric wrt point of intersection of the 2 walls
        if (len(self.__slopes) == 2) and (self.__slopes[0] != self.__slopes[1]):
            # if the wall is vertical
            if self.__slopes[0] == cmath.inf:
                x_intersection = self.__intercepts[0]
                y_intersection = self.__slopes[1] * x_intersection + self.__intercepts[1]
            elif self.slopes[1] == cmath.inf:
                x_intersection = self.__intercepts[1]
                y_intersection = self.__slopes[0] * x_intersection + self.__intercepts[0]
            else:
                # find the coordinates of the intersection point of the two walls
                x_intersection = (self.__intercepts[1] - self.__intercepts[0]) / (self.__slopes[0] - self.__slopes[1])
                y_intersection = self.__slopes[0] * x_intersection + self.__intercepts[0]
            # find the coordinates of symmetric wrt intersection point from midpoint formula
            z_images.append(complex(2. * x_intersection - x_el, 2. * y_intersection - y_el))

        return z_images


        
    def complex_potential(self, element, z):
        """Computes the complex potential of the walls (i.e. the symmetric of the element about the walls with opposite circulation) 
        of an element of type `element` at point `z`.

        :param element: Flow element instance to compute the complex potential on.
        :type element: class:`flow_element.FlowElement`
        :param z: Position where the complex potential is to be computed.
        :type z: complex
        :return: Complex potential of the walls
        :rtype: complex
        """
        result = np.zeros_like(z)
        if not self.__slopes:
            return result

        z_images = self.__find_symmetric(element.z_current())

        for z_image in z_images:
            result += element.complex_potential_symmetric(z, z_image)

        return result

    def derivative_complex_potential(self, element, z):
        """Computes the derivative of the complex potential of the walls (i.e. the symmetric of the element about the walls with opposite circulation) 
        of an element of type `element` at point `z`.

        :param element: Flow element instance to compute the derivative on
        :type element: class:`flow_element.FlowElement`
        :param z: Position where the derivative is to be computed.
        :type z: complex
        :return: Derivative of the complex potential of the walls
        :rtype: complex
        """
        result = np.zeros_like(z)
        if not self.__slopes:
            return result

        z_images = self.__find_symmetric(element.z_current())
        for z_image in z_images:
            result += element.derivative_complex_potential_symmetric(z, z_image)

        return result

        

class UniformStream(FlowElement):
    """This class replicates the behavior of a uniform stream.
    It inherits the :class:`FlowElement` abstract class.

    :param free_stream_velocity: Free stream velocity
    :type free_stream_velocity: float
    :param free_stream_incidence: Free stream incidence in radians
    :type free_stream_incidence: float
    :param id: Element id for user output
    :type id: int
    """

    def __init__(self, free_stream_velocity, free_stream_incidence, id):
        """Constructor method
        """
        self.__free_stream_velocity = free_stream_velocity
        self.__free_stream_incidence = free_stream_incidence
        self.__name = "Uniform Stream" # for plotting
        self.__id = id # for plotting

    def print_parameters(self):
        """Prints the element's parameters to console.
        """
        angle = self.__free_stream_incidence * 180 / cmath.pi # convert to degrees
        print(f"Flow element {self.__id}: {self.__name}")
        print(f"Free stream velocity:         {self.__free_stream_velocity} m/s,")
        print(f"Free stream angle of attack:  {angle} deg.")

    def name(self):
        """Returns the name of this element, i.e. "Uniform Stream"

        :return: Name of the element
        :rtype: str
        """
        return self.__name

    def id(self):
        """Returns element id (for plotting)

        :return: Element id
        :rtype: int
        """
        return self.__id

    #=========================================================
    #                                                 position
    #=========================================================
    def z_initial(self):
        """A uniform stream does not have a unique position on the complex plane so returns the origin.

        :return: Returns the origin, i.e. (0. 0)
        :rtype: complex
        """
        return complex(0.0, 0.0)

    def z_current(self):
        """A uniform stream does not have a unique position on the complex plane so returns the origin.

        :return: Returns the origin, i.e. (0. 0)
        :rtype: complex
        """
        return complex(0.0, 0.0)

    def set_z(self, z):
        """A uniform stream does not have a unique position on the complex planes. This method does nothing.

        :param z: Useless parameter
        :type z: complex
        """
        pass

    #=========================================================
    #                                        complex potential
    #=========================================================
    def complex_potential(self, z):
        """Returns the complex potential :math:`w` of this element at point :math:`z`: :math:`w(z - z_{self}) = \phi + i \psi`, where :math:`\phi` is the velocity potential and :math:`\psi` is the stream function.
        For a uniform stream: :math:`w(z - z_{self}) = U_{\\infty} e^{- i \\alpha} (z - z_{self})`.
        
        :param z: Position where the complex potential :math:`w(z - z_{self})` is to be computed.
        :type z: complex
        :return: Complex potential :math:`w(z - z_{self})`
        :rtype: complex
        """
        return self.__free_stream_velocity * cmath.exp(complex(0.0, - self.__free_stream_incidence)) * z

    #=========================================================
    #                             derivative complex potential
    #=========================================================
    def derivative_complex_potential(self, z):
        """Returns the derivative of the complex potential :math:`dw/dz` of this element at point :math:`z`: :math:`dw/dz = u - i v`, where :math:`u` and :math:`v` are the horizontal and vertical components of the velocity respectively.
        For a uniform stream:

        .. math::

            \\frac{dw}{dz} = U_{\\infty} e^{- i \\alpha}

        Please note that :math:`v` is given by :math:`- Im(dw/dz)`.

        :param z: Position where the derivative of the complex potential :math:`dw/dz` is to be computed
        :type z: complex
        :return: Derivative of the complex potential
        :rtype: complex
        """
        return np.ones_like(z) * self.__free_stream_velocity * cmath.exp(complex(0.0, - self.__free_stream_incidence))


class Source(FlowElement):
    """This class replicates the behavior of a source.
    It inherits the :class:`FlowElement` abstract class.

    :param strength: Strength of the source
    :type strength: float
    :param z_initial: Initial position of the source
    :type z_initial: complex
    :param id: Element id for user output
    :type id: int
    :param tolerance: If denominator is smaller than tolerance, skips the division and returns 0
    :type tolerance: float, optional
    """

    def __init__(self, strength, z_initial, id, tolerance=0.0001):
        """Constructor method
        """
        self.__strength = strength
        self.__z_initial = z_initial
        self.__z = self.__z_initial
        self.__tolerance = tolerance # for division by zero
        self.__name = "Source" # for plotting
        self.__id = id # for plotting
        self.__wall_slope = []
        self.__wall_intercept = []

    def print_parameters(self):
        """Prints the element's parameters to console.
        """
        print(f"Flow element {self.__id}: {self.__name}")
        print(f"Strength:                     {self.__strength},")
        print(f"Initial location:             ({self.__z_initial.real}, {self.__z_initial.imag}),")
        print(f"Current location:             ({self.__z.real}, {self.__z.imag}).")

    def name(self):
        """Returns the name of this element, i.e. "Source"

        :return: Name of the element
        :rtype: str
        """
        return self.__name

    def id(self):
        """Returns element id (for plotting)

        :return: Element id
        :rtype: int
        """
        return self.__id

    def add_walls(self, slopes, intercepts):
        """This method adds one or two walls to the flow. 

        :param slopes: Slope of the linear function describing the wall
        :type slopes: float
        :param intercepts: Intercept of the linear function describing the wall
        :type intercepts: float
        """
        self.__walls = Walls(slopes, intercepts)

    #=========================================================
    #                                                 position
    #=========================================================
    def z_initial(self):
        """Returns the initial position of the element

        :return: Initial position of the element
        :rtype: complex
        """
        return self.__z_initial

    def z_current(self):
        """Returns the current position of the element

        :return: Current position of the element
        :rtype: complex
        """
        return self.__z

    def set_z(self, z):
        """Sets the current position of the element

        :param z: Current position
        :type z: complex
        """
        self.__z = z

    #=========================================================
    #                                        complex potential
    #=========================================================
    def complex_potential(self, z):
        """Returns the complex potential :math:`w` of this element at point :math:`z`: :math:`w(z - z_{self}) = \phi + i \psi`, where :math:`\phi` is the velocity potential and :math:`\psi` is the stream function.
        For a source: 
        
        .. math::
        
            w(z - z_{self}) = \\frac{m}{2 \\pi} ln(z - z_{self})
        
        :param z: Position where the complex potential :math:`w(z - z_{self})` is to be computed.
        :type z: complex
        :return: Complex potential :math:`w(z - z_{self})`
        :rtype: complex
        """
        delta_z = z - self.__z
        res =  self.__strength * 0.5 / cmath.pi * np.log(delta_z)
        try:
            res_symmetry = self.__walls.complex_potential(self, z)
        except AttributeError:
            return res
        return res + res_symmetry

    def complex_potential_symmetric(self, z, z_symmetric):
        """Returns the complex potential :math:`w` of self element at point :math:`z`: :math:`w(z - z_{vortex}) = \phi + i \psi`, where :math:`\phi` is the velocity potential and :math:`\psi` is the stream function.
        This method can be called to add an another self element at position z_symmetric with opposite circulation.
        For instance, to add a wall, call this method with z_symmetric being the position of the symmetric of self about the wall.
        For a source: 
        
        .. math::
        
            w(z - z_{self}) = \\frac{- m}{2 \\pi} ln(z - z_{self})
        
        :param z: Position where the complex potential :math:`w(z - z_{vortex})` is to be computed.
        :type z: complex
        :param z_symmetric: Position of the symmetric element the complex potential is to be computed on
        :type z_symmetric: complex
        :return: Complex potential :math:`w(z - z_{vortex})`
        :rtype: complex
        """
        delta_z = z - z_symmetric
        return - self.__strength * 0.5 / cmath.pi * np.log(delta_z)


    #=========================================================
    #                             derivative complex potential
    #=========================================================
    def derivative_complex_potential(self, z):
        """Returns the derivative of the complex potential :math:`dw/dz` of this element at point :math:`z`: :math:`dw/dz = u - i v`, where :math:`u` and :math:`v` are the horizontal and vertical components of the velocity respectively.
        For a source:

        .. math::

            \\frac{dw}{dz} = \\frac{m}{2 \\pi (z - z_{self})}

        Please note that :math:`v` is given by :math:`- Im(dw/dz)`.

        :param z: Position where the derivative of the complex potential :math:`dw/dz` is to be computed
        :type z: complex
        :return: Derivative of the complex potential
        :rtype: complex
        """
        """Computes the derivative of the complex potential of this element at position :param:`z`
        For a source:
        dF/dz = m / (2 pi z)
        where dF/dz = u - i*v with u and v horizontal and vertical components of velocity respectively
        Returns zero if :param:`z` - (element position) is within the tolerance

        :param z: Position
        :type z: complex
        :return: Derivative of the complex potential
        :rtype: complex
        """
        delta_z = z - self.__z
        # get the indices for which dFdz can be computed
        indices = abs(delta_z) > self.__tolerance
        # initialize array of zeros for the result
        res = np.zeros_like(delta_z)
        # compute dFdz
        res[indices] = self.__strength * 0.5 / cmath.pi / delta_z[indices]
        try:
            res_symmetry = self.__walls.derivative_complex_potential(self, z)
        except AttributeError:
            return res
        return res + res_symmetry

    def derivative_complex_potential_symmetric(self, z, z_symmetric):
        """Returns the derivative of the complex potential :math:`dw/dz` of this element at point :math:`z`: :math:`dw/dz = u - i v`, where :math:`u` and :math:`v` are the horizontal and vertical components of the velocity respectively.
        This method can be called to add an another self element at position z_symmetric.
        For instance, to add a wall, call this method with z_symmetric being the position of the symmetric of self about the wall.
        For a source:

        .. math::

            \\frac{dw}{dz} = \\frac{- m}{2 \\pi (z - z_{self})}

        Please note that :math:`v` is given by :math:`- Im(dw/dz)`.

        :param z: Position where the derivative of the complex potential :math:`dw/dz` is to be computed
        :type z: complex
        :param z_symmetric: Position of the symmetric element the derivative of the complex potential is to be computed on
        :type z_symmetric: complex
        :return: Derivative of the complex potential
        :rtype: complex
        """
        delta_z = z - z_symmetric
        # get the indices for which dFdz can be computed
        indices = abs(delta_z) > self.__tolerance
        # initialize array of zeros for the result
        res = np.zeros_like(delta_z)
        # compute dFdz
        res[indices] = - self.__strength * 0.5 / cmath.pi / delta_z[indices]
        return res


class Vortex(FlowElement):
    """This class replicates the behavior of a vortex.
    It inherits the :class:`FlowElement` abstract class.

    :param circulation: Circulation of the vortex
    :type circulation: float
    :param z_initial: Initial position of the vortex
    :type z_initial: complex
    :param id: Element id for user output
    :type id: int
    :param tolerance: If denominator smaller than tolerance, skips the division
    :type tolerance: float, optional
    """

    def __init__(self, circulation, z_initial, id, tolerance=0.0001):
        """Constructor method
        """
        self.__circulation = circulation
        self.__z_initial = z_initial
        self.__id = id # for plotting
        self.__tolerance = tolerance # for division by zero
        self.__z = self.__z_initial # current position
        self.__name = "Vortex" # for plotting

    def print_parameters(self):
        """Prints element's parameters to console.
        """
        print(f"Flow element {self.__id}: {self.__name}")
        print(f"Circulation:                  {self.__circulation},")
        print(f"Initial location:             ({self.__z_initial.real}, {self.__z_initial.imag}),")
        print(f"Current location:             ({self.__z.real}, {self.__z.imag}).")

    def name(self):
        """Returns the name of this element, i.e. "Vortex"

        :return: Name of the element
        :rtype: str
        """
        return self.__name

    def id(self):
        """Returns element id (for plotting)

        :return: Element id
        :rtype: int
        """
        return self.__id

    def add_walls(self, slopes, intercepts):
        """This method adds one or two walls to the flow. 

        :param slope: Slope of the linear function describing the wall
        :type slope: float
        :param intercept: Intercept of the linear function describing the wall
        :type intercept: float
        """
        self.__walls = Walls(slopes, intercepts)

    #=========================================================
    #                                                 position
    #=========================================================
    def z_initial(self):
        """Returns the initial position of the element

        :return: Initial position of the element
        :rtype: complex
        """
        return self.__z_initial

    def z_current(self):
        """Returns the current position of the element

        :return: Current position of the element
        :rtype: complex
        """
        return self.__z

    def set_z(self, z):
        """Sets the current position of the element

        :param z: Current position
        :type z: complex
        """
        self.__z = z

    #=========================================================
    #                                        complex potential
    #=========================================================
    def complex_potential(self, z):
        """Returns the complex potential :math:`w` of this element at point :math:`z`: :math:`w(z - z_{self}) = \phi + i \psi`, where :math:`\phi` is the velocity potential and :math:`\psi` is the stream function.
        For a vortex:
        
        .. math::
        
            w(z - z_{self}) = \\frac{- i \\Gamma}{2 \\pi} ln(z - z_{self})
        
        :param z: Position where the complex potential :math:`w(z - z_{self})` is to be computed.
        :type z: complex
        :return: Complex potential :math:`w(z - z_{self})`
        :rtype: complex
        """
        delta_z = z - self.__z
        res = - complex(0.0, self.__circulation * 0.5 / cmath.pi) * np.log(delta_z)
        try:
            res_symmetry = self.__walls.complex_potential(self, z)
        except AttributeError:
            return res
        return res + res_symmetry

    def complex_potential_symmetric(self, z, z_symmetric):
        """Returns the complex potential :math:`w` of self element at point :math:`z`: :math:`w(z - z_{vortex}) = \phi + i \psi`, where :math:`\phi` is the velocity potential and :math:`\psi` is the stream function.
        This method can be called to add an another self element at position z_symmetric.
        For instance, to add a wall, call this method with z_symmetric being the position of the symmetric of self about the wall.
        For a vortex:
        
        .. math::
        
            w(z - z_{vortex}) = \\frac{i \\Gamma}{2 \\pi} ln(z - z_{vortex})
        
        :param z: Position where the complex potential :math:`w(z - z_{vortex})` is to be computed.
        :type z: complex
        :param z_symmetric: Position of the symmetric element the complex potential is to be computed on
        :type z_symmetric: complex
        :return: Complex potential :math:`w(z - z_{vortex})`
        :rtype: complex
        """
        delta_z = z - z_symmetric
        return complex(0.0, self.__circulation * 0.5 / cmath.pi) * np.log(delta_z) # got rid of the minus !!!

    #=========================================================
    #                             derivative complex potential
    #=========================================================
    def derivative_complex_potential(self, z):
        """Returns the derivative of the complex potential :math:`dw/dz` of this element at point :math:`z`: :math:`dw/dz = u - i v`, where :math:`u` and :math:`v` are the horizontal and vertical components of the velocity respectively.
        For a vortex:

        .. math::

            \\frac{dw}{dz} = \\frac{- i \\Gamma}{2 \\pi (z - z_{self})}

        Please note that :math:`v` is given by :math:`- Im(dw/dz)`.

        :param z: Position where the derivative of the complex potential :math:`dw/dz` is to be computed
        :type z: complex
        :return: Derivative of the complex potential
        :rtype: complex
        """
        delta_z = z - self.__z
        # get the indices for which dFdz can be computed
        indices = abs(delta_z) > self.__tolerance
        # initialize array of zeros for the result
        res = np.zeros_like(delta_z)
        # compute dFdz
        res[indices] = - complex(0.0, self.__circulation * 0.5 / cmath.pi) / delta_z[indices]
        try:
            res_symmetry = self.__walls.derivative_complex_potential(self, z)
        except AttributeError:
            return res
        return res + res_symmetry

    def derivative_complex_potential_symmetric(self, z, z_symmetric):
        """Returns the derivative of the complex potential :math:`dw/dz` of this element at point :math:`z`: :math:`dw/dz = u - i v`, where :math:`u` and :math:`v` are the horizontal and vertical components of the velocity respectively.
        This method can be called to add an another self element at position z_symmetric.
        For instance, to add a wall, call this method with z_symmetric being the position of the symmetric of self about the wall.
        For a vortex:

        .. math::

            \\frac{dw}{dz} = \\frac{i \\Gamma}{2 \\pi (z - z_{self})}

        Please note that :math:`v` is given by :math:`- Im(dw/dz)`.

        :param z: Position where the derivative of the complex potential :math:`dw/dz` is to be computed
        :type z: complex
        :param z_symmetric: Position of the symmetric element the derivative of the complex potential is to be computed on
        :type z_symmetric: complex
        :return: Derivative of the complex potential
        :rtype: complex
        """
        delta_z = z - z_symmetric
        # get the indices for which dFdz can be computed
        indices = abs(delta_z) > self.__tolerance
        # initialize array of zeros for the result
        res = np.zeros_like(delta_z)
        # compute dFdz
        res[indices] = complex(0.0, self.__circulation * 0.5 / cmath.pi) / delta_z[indices] # got rid of the minus !!!
        return res

class Cylinder(FlowElement):
    """This class replicates the behavior of a circular cylinder.
    It inherits the :class:`FlowElement` abstract class.

    :param radius: Radius of the cylinder
    :type radius: float
    :param z_initial: Initial position of the cylinder
    :type z_initial: complex
    :param circulation: Circulation of the cylinder
    :type circulation: float
    :param fsv: Free stream velocity
    :type fsv: float
    :param fsi: Free stream angle of incidence in radians
    :type fsi: float
    :param id: Element id for user output
    :type id: int
    :param tolerance: If denominator smaller than tolerance, skips the division and returns zero
    :type tolerance: float, optional
    """

    def __init__(self, radius, z_initial, circulation, fsv, fsi, id, tolerance=0.0001):
        """Constructor method
        """
        self.__radius = radius
        self.__z_initial = z_initial
        self.__circulation = circulation
        self.__free_stream_velocity = fsv
        self.__free_stream_incidence = fsi
        self.__id = id # for plotting
        self.__tolerance = tolerance # for division by zero
        self.__z = self.__z_initial # current position
        self.__name = "Cylinder" # for plotting

    def print_parameters(self):
        """Prints element's parameters to console.
        """
        print(f"Flow element {self.__id}: {self.__name}")
        print(f"    Radius:                 {self.__radius},")
        print(f"    Initial position:       ({self.__z_initial.real}, {self.__z_initial.imag}),")
        print(f"    Circulation:            {self.__circulation},")
        print(f"    Free stream velocity:   {self.__free_stream_velocity},")
        print(f"    Free stream incidence:  {self.__free_stream_incidence},")
        print(f"    Current position:       ({self.__z.real}, {self.__z.imag}).")

    def name(self):
        """Returns the name of this element, i.e. "Cylinder"

        :return: Name of the element
        :rtype: str
        """
        return self.__name

    def id(self):
        """Returns element id (for plotting)

        :return: Element id
        :rtype: int
        """
        return self.__id

    #=========================================================
    #                                                 position
    #=========================================================
    def z_initial(self):
        """Returns the initial position of the element

        :return: Initial position of the element
        :rtype: complex
        """
        return self.__z_initial

    def z_current(self):
        """Returns the current position of the element

        :return: Current position of the element
        :rtype: complex
        """
        return self.__z

    def set_z(self, z):
        """Sets the current position of the element

        :param z: Current position
        :type z: complex
        """
        self.__z = z

    #=========================================================
    #                                        complex potential
    #=========================================================
    def complex_potential(self, z):
        """Returns the complex potential :math:`w` of this element at point :math:`z`: :math:`w(z - z_{self}) = \phi + i \psi`, where :math:`\phi` is the velocity potential and :math:`\psi` is the stream function.
        For a circular cylinder:
        
        .. math::
        
            w(z - z_{self}) = U_{\\infty} ((z - z_{self}) e^{-i \\alpha} + \\frac{R^2 e^{i \\alpha}}{(z - z_{self})}) - \\frac{i \\Gamma}{2 \\pi} ln(z - z_{self})
        
        :param z: Position where the complex potential :math:`w(z - z_{self})` is to be computed.
        :type z: complex
        :return: Complex potential :math:`w(z - z_{self})`
        :rtype: complex
        """

        delta_z = z - self.__z
        # get the indices for which F(z) can be computed
        indices = abs(delta_z) > self.__tolerance
        # initializes array of zeros for result
        res = np.zeros_like(delta_z)
        # compute F(z)
        res += delta_z * cmath.exp(complex(0.0, -self.__free_stream_incidence))
        res[indices] += self.__radius * self.__radius * cmath.exp(complex(0.0, self.__free_stream_incidence)) / delta_z[indices]
        res *= self.__free_stream_velocity
        res -= complex(0.0, self.__circulation * 0.5 / cmath.pi) * np.log(delta_z)
        return res

    #=========================================================
    #                             derivative complex potential
    #=========================================================
    def derivative_complex_potential(self, z):
        """Returns the derivative of the complex potential :math:`dw/dz` of this element at point :math:`z`: :math:`dw/dz = u - i v`, where :math:`u` and :math:`v` are the horizontal and vertical components of the velocity respectively.
        For a circular cylinder:

        .. math::

            \\frac{dw}{dz} = U_{\\infty} (e^{-i \\alpha} - \\frac{R^2 e^{i \\alpha}}{(z - z_{self})^2}) - \\frac{i \\Gamma}{2 \\pi (z - z_{self})}

        Please note that :math:`v` is given by :math:`- Im(dw/dz)`.

        :param z: Position where the derivative of the complex potential :math:`dw/dz` is to be computed
        :type z: complex
        :return: Derivative of the complex potential
        :rtype: complex
        """
        delta_z = z - self.__z
        # get the indices for which F(z) can be computed
        indices = abs(delta_z) > self.__tolerance
        # initialize array of zeros 
        res = np.zeros_like(delta_z)
        # computes dFdz
        res += cmath.exp(complex(0.0, -self.__free_stream_incidence))
        res[indices] -= self.__radius * self.__radius * cmath.exp(complex(0.0, self.__free_stream_incidence)) / delta_z[indices] / delta_z[indices]
        res *= self.__free_stream_velocity 
        res[indices] -= complex(0.0, self.__circulation * 0.5 / cmath.pi) / delta_z[indices]
        return res

class JoukowskiElement(FlowElement):
    """This class replicates the behavior of an element after the Joukowski transform.
    It inherits the :class:`FlowElement` abstract class.

    :param radius: Radius
    :type radius: float
    :param z_initial: Initial position
    :type z_initial: complex
    :param circulation: Circulation
    :type circulation: float
    :param fsv: Free stream velocity
    :type fsv: float
    :param fsi: Free stream angle of incidence in radians
    :type fsi: float
    :param a: Joukowski transform constant
    :type a: float
    :param id: Element id for user output
    :type id: int
    :param tolerance: If denominator smaller than tolerance, skips the division and returns zero
    :type tolerance: float, optional
    """

    def __init__(self, z_initial, circulation, radius, fsv, fsi, a, id, tolerance=0.0001):
        """Constructor method
        """
        self.__radius = radius
        self.__z_initial = z_initial
        self.__circulation = circulation
        self.__free_stream_velocity = fsv
        self.__free_stream_incidence = fsi
        self.__a = a
        self.__id = id # for plotting
        self.__tolerance = tolerance # for division by zero
        self.__z = self.__z_initial # current position
        self.__name = "Joukowski" # for plotting

    def print_parameters(self):
        """Prints element's parameters to console.
        """
        print(f"Flow element {self.__id}: {self.__name}")
        print(f"    Radius:                 {self.__radius},")
        print(f"    Initial position:       ({self.__z_initial.real}, {self.__z_initial.imag}),")
        print(f"    Circulation:            {self.__circulation},")
        print(f"    Free stream velocity:   {self.__free_stream_velocity},")
        print(f"    Free stream incidence:  {self.__free_stream_incidence},")
        print(f"    Joukowski constant:     {self.__a},")
        print(f"    Current position:       ({self.__z.real}, {self.__z.imag}).")

    def name(self):
        """Returns the name of this element, i.e. "Cylinder"

        :return: Name of the element
        :rtype: str
        """
        return self.__name

    def id(self):
        """Returns element id (for plotting)

        :return: Element id
        :rtype: int
        """
        return self.__id

    #=========================================================
    #                                                 position
    #=========================================================
    def z_initial(self):
        """Returns the initial position of the element

        :return: Initial position of the element
        :rtype: complex
        """
        return self.__z_initial

    def z_current(self):
        """Returns the current position of the element

        :return: Current position of the element
        :rtype: complex
        """
        return self.__z

    def set_z(self, z):
        """Sets the current position of the element

        :param z: Current position
        :type z: complex
        """
        self.__z = z

    def __joukowski_transform(self, z):
        return z +  self.__a * self.__a / z
    def __derivative_joukowski_transform(self, z):
        return 1 - self.__a * self.__a / z / z

    #=========================================================
    #                                        complex potential
    #=========================================================
    def complex_potential(self, z):
        """Returns the complex potential :math:`w` of this element at point :math:`z`: :math:`w(z - z_{self}) = \phi + i \psi`, where :math:`\phi` is the velocity potential and :math:`\psi` is the stream function.
        For a circular cylinder:
        
        .. math::
        
            w(z - z_{self}) = U_{\\infty} ((z - z_{self}) e^{-i \\alpha} + \\frac{R^2 e^{i \\alpha}}{(z - z_{self})}) - \\frac{i \\Gamma}{2 \\pi} ln(z - z_{self})
        
        :param z: Position where the complex potential :math:`w(z - z_{self})` is to be computed.
        :type z: complex
        :return: Complex potential :math:`w(z - z_{self})`
        :rtype: complex
        """

        z_plane = z - self.__z
        delta_z = self.__joukowski_transform(z_plane)
        # get the indices for which F(z) can be computed
        indices = abs(delta_z) > self.__tolerance
        # initializes array of zeros for result
        res = np.zeros_like(delta_z)
        # compute F(z)
        res += delta_z * cmath.exp(complex(0.0, -self.__free_stream_incidence))
        res[indices] += self.__radius * self.__radius * cmath.exp(complex(0.0, self.__free_stream_incidence)) / delta_z[indices]
        res *= self.__free_stream_velocity
        res -= complex(0.0, self.__circulation * 0.5 / cmath.pi) * np.log(delta_z)
        return res

    #=========================================================
    #                             derivative complex potential
    #=========================================================
    def derivative_complex_potential(self, z):
        """Returns the derivative of the complex potential :math:`dw/dz` of this element at point :math:`z`: :math:`dw/dz = u - i v`, where :math:`u` and :math:`v` are the horizontal and vertical components of the velocity respectively.
        For a circular cylinder:

        .. math::

            \\frac{dw}{dz} = U_{\\infty} (e^{-i \\alpha} - \\frac{R^2 e^{i \\alpha}}{(z - z_{self})^2}) - \\frac{i \\Gamma}{2 \\pi (z - z_{self})}

        Please note that :math:`v` is given by :math:`- Im(dw/dz)`.

        :param z: Position where the derivative of the complex potential :math:`dw/dz` is to be computed
        :type z: complex
        :return: Derivative of the complex potential
        :rtype: complex
        """
        # delta_z = z - self.__z
        z_plane = z - self.__z
        delta_z = self.__joukowski_transform(z_plane)
        # get the indices for which F(z) can be computed
        indices = abs(delta_z) > self.__tolerance
        # initialize array of zeros 
        res = np.zeros_like(delta_z)
        # computes dFdz
        res += cmath.exp(complex(0.0, -self.__free_stream_incidence))
        res[indices] -= self.__radius * self.__radius * cmath.exp(complex(0.0, self.__free_stream_incidence)) / delta_z[indices] / delta_z[indices]
        res *= self.__free_stream_velocity 
        res[indices] -= complex(0.0, self.__circulation * 0.5 / cmath.pi) / delta_z[indices]

        mapped = self.__derivative_joukowski_transform(delta_z)
        res /= mapped
        return res

class Flow(FlowElement):
    """This iterable class stores all the flow elements in a list. 
    This list is iterated over to compute the complex potential and its derivative.
    This class inherits the :class:`FlowElement` abstract class and overrides its methods.
    """

    def __init__(self):
        """Constructor method.
        Initializes an empty list and a variable to track the size of the list.
        """
        self.__flow_elements = []
        self.__num_elements = 0

    def print_parameters(self):
        """Prints the parameters of each flow elements to console.
        """
        for el in self.__flow_elements:
            el.print_parameters()

    def empty(self):
        """Returns true if there are no elements in the flow.

        :return: True if the list of flow elements is empty.
        :rtype: bool
        """
        return self.__flow_elements == []

    def num_of_elements(self):
        """Returns the number of elements in the flow

        :return: Number of elements in the flow
        :rtype: int
        """
        return self.__num_elements

    #=========================================================
    #                                                accessors
    #=========================================================
    def __iter__(self):
        """Iterator to iterate through the flow elements.

        :return: Flow elements iterator
        :rtype: :class:`FlowIterator`
        """
        return FlowIterator(self.__flow_elements)

    def add_element(self, element):
        """Appends element to the list of flow elements.

        :param element: Flow element to be added
        :type element: :class:`FlowElement` 
        """
        if self.__num_elements >= 0:
            self.__num_elements += 1
            self.__flow_elements.append(element)

    def remove_element(self, id):
        """Removes the element at position `id` from the list of flow elements.
        This method has not been tested and should not be used.

        :param id: Index of the flow element to be removed in the flow elements list
        :type id: int
        """
        if self.__num_elements > 0 and self.__num_elements > id:
            self.__flow_elements[id] = self.__flow_elements.pop()

    def pop_element(self):
        """Pops the last element off the flow elements list.
        """
        if self.__num_elements > 0:
            self.__flow_elements.pop()

    #=========================================================
    #                                        complex potential
    #=========================================================
    def complex_potential(self, z):
        """Returns the complex potential :math:`w` of all the flow elements at point :math:`z`: :math:`w(z - z_{self}) = \phi + i \psi`, where :math:`\phi` is the velocity potential and :math:`\psi` is the stream function.
        This methods iterates over all the elements in the list of flow elements and returns the sum of the `complex_potential(z)` method calls.
        
        :param z: Position where the complex potential :math:`w(z - z_{self})` is to be computed.
        :type z: complex
        :return: Complex potential :math:`w(z - z_{self})`
        :rtype: complex
        """
        F = complex(0.0, 0.0)
        for el in self.__flow_elements:
            F += el.complex_potential(z)
        return F

    #=========================================================
    #                             derivative complex potential
    #=========================================================
    def derivative_complex_potential(self, z):
        """Returns the derivative of the complex potential :math:`dw/dz` of this element at point :math:`z`: :math:`dw/dz = u - i v`, where :math:`u` and :math:`v` are the horizontal and vertical components of the velocity respectively.
        This methods iterates over all the elements in the list of flow elements and returns the sum of the `derivative_complex_potential(z)` method calls.
        Please note that :math:`v` is given by :math:`- Im(dw/dz)`.

        :param z: Position where the derivative of the complex potential :math:`dw/dz` is to be computed
        :type z: complex
        :return: Derivative of the complex potential
        :rtype: complex
        """
        dFdz = np.zeros_like(z)
        for el in self.__flow_elements:
            dFdz += el.derivative_complex_potential(z)
        return dFdz

class FlowIterator:
    # Class to iterate through all the flow elements in Flow
    def __init__(self, flow_elements):
        self.__elements = flow_elements
        self.__num_elements = len(self.__elements)
        self.__current_index = 0
        
    def __iter__(self):
        return self

    def __next__(self):
        if self.__current_index < self.__num_elements:
            element = self.__elements[self.__current_index]
            self.__current_index += 1
            return element
        raise StopIteration
