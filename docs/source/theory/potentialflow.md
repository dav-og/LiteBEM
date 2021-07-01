# Linear Potential Flow Theory

1.  [Fundamentals and main assumptions](#orgcb32f72)
2.  [Summary of boundary conditions](#org9f60e73)
3.  [Solving for hydrodynamic forces](#orgfbb77fd)

<!-- <script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    TeX: { equationNumbers: { autoNumber: "AMS" } }
  });
</script>

<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script> 
 -->
 
 <script type="text/javascript"
        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS_CHTML"></script>

`DISCLAIMER 1:` John von Neumann referred to potential flow theory as the study of
dry water.

`DISCLAIMER 2:` Richard Feynman stated that potential flow theory had nothing to
do with real fluids and that it was more to do with solving beautiful mathematical
problems

Despite the simplications, potential flow theory is incredibly important to WEC
numerical modelling - enabling the modelling of a wide range of operating
conditions in a fraction of the time of higher-fidelity approaches such as CFD
and SPH.

BEM codes based on linear potential flow theory are well-established in the
hydrodynamics field, and are the foundation of most time-domain solvers (e.g.
WEC-Sim).

## Fundamentals and main assumptions

-   In order to model fluid motion, we essentially need to be able to determine
    the velocity vector $\vec{v}(x, y, z, t)$ of a fluid particle at any point
    within the flow:
    
	$$
	\begin{equation}
    \vec{v} = \frac{d\vec{x}}{dt} = \begin{bmatrix}
      u \\
      v \\
      w
      \end{bmatrix}
    \end{equation}
	$$

-   However, there are other fluid properties which may also vary throughout the
    flow, over time. To simplify the model, we can assume these remain
    constant.

-   If we assume the fluid to be incompressible, then its density must remain
    constant:
    
	$$
    \begin{equation}
    \rho = const.
    \end{equation}
	$$

-   This assumption means the divergence of the flow's velocity must be zero,
    hence the continuity (conservation of mass) equation is:
    
	$$
    \begin{equation}
    \frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} +
    \frac{\partial w}{\partial z} = 0
    \end{equation}
    $$
	
	$$
    \begin{equation}
    \nabla \cdot \vec{v} = 0
    \end{equation}
	$$

-   Potential flow theory also assumes that the the flow is inviscid (i.e. the
    fluid cannot experience any shear stresses) from $t=0s$, and therefore the
    vorticity must be zero everywhere - hence the fluid is irrotational:
    
	$$
    \begin{equation}
    \label{eq:irrotational}
      \nabla \times \vec{v} = 0
    \end{equation}
	$$

-   Under these simplifictions, the velocity vector, $\vec{v}(x, y, z, t)$ may
    be replaced with a mathematical abstraction: the gradient of a scalar
    potential, $\phi(x, y, z, t)$:
    
	$$
    \begin{equation}
    \label{eq:scalar_potential}
    \vec{v} = \nabla\phi = \begin{bmatrix}
      \frac{\partial \phi}{\partial x} \\
      \frac{\partial \phi}{\partial y} \\
      \frac{\partial \phi}{\partial z}
      \end{bmatrix}
    \end{equation}
	$$

-   In this approach, instead of computing 3 unknown velocity vector components,
    only 1 unknown scalar quantity needs to be determined, from which all three
    velocity components can be derived.

-   Inserting Equation \ref{eq:scalar_potential} into
    Equation \ref{eq:irrotational} gives the Laplace equation:
    
	$$
    \begin{equation}
    \label{eq:laplace}
    \nabla^2 \phi = 0
    \end{equation}
	$$


## Summary of boundary conditions

-   The free surface cannot withstand pressure differences, this is applied via
    Bernoulli's equation:
    
	$$
    \begin{equation}
    \label{eq:Bernoulli}
    \frac{\partial \phi}{\partial t} + \frac{1}{2}(\nabla \phi)^2 +
    \frac{p_0}{\rho} + g\eta = C 
    \end{equation}
    $$
	
    -   Where the constant, $C = \frac{p_0}{\rho}$. By assuming that the
        wavelength is much larger than the wave amplitude, the second order term
        in Equation \ref{eq:Bernoulli} can be assumed to be small, hence the
        boundary condition becomes:
    
	$$
    \begin{equation}
    \label{eq:BernoulliLinear}
    \frac{\partial\phi}{\partial t} + g\eta = 0
    \end{equation}
	$$

-   The free surface is also impermeable, hence the fluid velocity normal to the
    surface must be equal to the surface velocity:
    
	$$
    \begin{equation}
    \label{eq:fsImpermeable}
    \frac{\partial \eta}{\partial t}
    + \frac{\partial \phi}{\partial x}\frac{\partial \eta}{\partial x}
    + \frac{\partial \phi}{\partial y}\frac{\partial \eta}{\partial y}
    + \frac{\partial \phi}{\partial z} = 0
    \end{equation}
	$$
    
    -   Again, by assuming that the wavelength is much larger than the wave
        amplitude, the second order terms in Equation \ref{eq:fsImpermeable} can
        be assumed to be small, hence the boundary condition becomes:
    
	$$
    \begin{equation}
    \label{eq:fsImpermeableLinear}
    \frac{\partial \eta}{\partial t} + \frac{\partial \phi}{\partial z} = 0
    \end{equation}
	$$

-   By introducing Equation \ref{eq:fsImpermeableLinear} into the
    time-derivative of Equation \ref{eq:BernoulliLinear}, the generalized form
    of the free surface boundary condition is: 
    
	$$
    \begin{equation}
    \label{eq:fsBoundaryCondition}
    \frac{\partial^2 \phi}{\partial t^2} - g \frac{\partial \phi}{\partial z} = 0
    \end{equation}
	$$

-   Assuming the seabed is flat and impermeable, there must be no vertical
    velocity component:
    
	$$
    \begin{equation}
    \frac{\partial \phi}{\partial z} = 0
    \end{equation}
	$$

-   Similarly, the wetted surface of the body in the fluid is impermeable, hence
    the fluid velocity normal to the body surface, $u_n$ must be equal to the
    body velocity in the direction normal to its surface:
    
	$$
    \begin{equation}
    \frac{\partial \phi}{\partial n} = u_n
    \end{equation}
	$$

-   The final condition is that radiated waves must decay with increasing
    distance from the body:
    
	$$
    \begin{equation}
    \phi \propto (kr)^{\frac{1}{2}}e^{ikr}
    \end{equation}
    $$
	
    As $r \rightarrow \infty$, where $r$ is the radial distance and $k$ is the
    wave number:
    
	$$
    \begin{equation}
    \frac{\omega^2}{g} = ktanh(kh)
    \end{equation}
	$$


## Solving for hydrodynamic forces

-   To obtain the hydrodynamic forces experienced by a body in the flow, we
    essentially need to integrate the dynamic pressure exerted on the (mean)
    wetted body surface, $S_b$:
    
	$$
    \begin{equation}
    \label{eq:potentialHydrodynamics}
    \vec{f}_{hd} = \rho \int_{S_b}\frac{\partial \phi}{\partial t} n dS_b
    \end{equation}
	$$
    
    Where $n$ is the unit vector normal to the body surface.

-   Under the linearity assumption, the velocity potential can be decomposed
    into 2 components describing the diffracted and radiated wave fields:
    
	$$
    \begin{equation}
    \phi = \phi_D + \phi_{rad}
    \end{equation}
	$$

-   Where the diffracted wave potential is:
    
	$$
    \begin{equation}
    \phi_D = \phi_0 + \phi_s
    \end{equation}
	$$
    
    $\phi_0$ represents the incident wave potential and $\phi_s$ represents
    the scattered wave potential.

-   Hence, Equation \ref{eq:potentialHydrodynamics} can be expressed in terms of
    the complex vectors of the excitation and radiation components:
    
	$$
    \begin{equation}
    \hat{f}_{hd} = \hat{f}_{ex} + \hat{f}_{rad}
    \end{equation}
	$$

-   $f_{ex}$ has two components: the Froude-Krylov force, $f_{FK}$ - associated
    with the undisturbed incident wave. And the scatter force, $f_s$, which
    results from waves interacting with the body and diffracting/scattering
    across the free surface<sup><a id="fnr.1" class="footref" href="#fn.1">1</a></sup>. In
    the frequency-domain:
    
	$$
    \begin{equation}
    \hat{f}_{FK}(\omega) = i\omega\rho \int_{S_b} \hat{\phi}_0 n dS_b
    \end{equation}
    $$
	
	$$
    \begin{equation}
    \hat{f}_{s}(\omega) = i\omega\rho \int_{S_b} \hat{\phi}_s n dS_b
    \end{equation}
	$$

-   As a body oscillates in a fluid, it radiates waves - which results in a
    damping force experienced by the body, $f_{rad}$. There is also an added
    mass effect due the body forcing the motion of some fluid in its vicinity.
    The analogy of electrical impedance (resistance and reactance) is commonly
    used (denoted by $Z(\omega)$):
    
	$$
    \begin{equation}
    \hat{f}_{rad}(\omega) = -i \omega Z(\omega) \hat{\vec{s}}(\omega)
    \end{equation}
    $$
	
	$$
    \begin{equation}
    Z(\omega) = -i\omega\rho \int_{S_b} \phi_{rad} n dS_b = \mathbf{B}(\omega) +
    i\omega\mathbf{A}(\omega) 
    \end{equation}
    $$
	
    (Where $\mathbf{B}(\omega)$ is radiation damping and $\mathbf{A}(\omega)$ is
    added mass).