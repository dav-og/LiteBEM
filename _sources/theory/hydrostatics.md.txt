# Hydrostatics

## Linear Hydrostatics

A body immersed in a fluid (either fully or partially) will experience a buoyant
force equal and opposite to the weight of the displaced fluid:

$$
\begin{equation}
  \vec{W} = -m\vec{g} = -\rho_{body}V\vec{g}
\end{equation}
$$

$$
\begin{equation}
  \vec{f}_{b} = \rho_{water} \vec{g} \nabla
\end{equation}
$$

Where $V$ is the total volume of the body and $\nabla$ is the body's submerged
volume. If a floating body is displaced from its equilibrium position, it will
also experience a 'restoring' hydrostatic force (i.e. the difference between the
buoyancy and weight forces). For small displacements this can be modelled as a
linear force:

$$
\begin{equation}
  \vec{f}_{hs} = \mathbf{K_{hs}} \Delta\vec{s}
\end{equation}
$$

Where $\mathbf{K_{hs}}$ is the matrix of hydrostatic restoring coefficients and
$\Delta\vec{s}$ represents the change in position (relative to equilibrium). For
1 floating body:

$$
\begin{equation}
  \mathbf{K_{hs}} = \begin{bmatrix}
                     0 & 0 & 0 & 0 & 0 & 0 \\
                     0 & 0 & 0 & 0 & 0 & 0 \\
                     0 & 0 & K_{33} & K_{34} & K_{35} & 0 \\
                     0 & 0 & K_{43} & K_{44} & K_{45} & 0 \\
                     0 & 0 & K_{53} & K_{54} & K_{55} & 0 \\
                     0 & 0 & 0 & 0 & 0 & 0
                   \end{bmatrix}
\end{equation}
$$

The geometry of the body affects it's hydrostatic stiffness properties, hence the
hydrostatic stiffness coefficients can be derived from the second moments of the
waterplane area, $S$:

$$
{
\begin{align}
  K_{33}   &  =  \rho g S_{0} \\
  K_{34}   &  =  \rho g \int \int_{S_0} y   dS \\
  K_{35}   &  = -\rho g \int \int_{S_0} x   dS \\
  K_{44}   &  =  \rho g \int \int_{S_0} y^2 dS - m g z_g + \rho g V z_b \\
  K_{45}   &  =  \rho g \int \int_{S_0} xy  dS \\
  K_{55}   &  =  \rho g \int \int_{S_0} x^2 dS - m g z_g + \rho g V z_b 
\end{align}
}
$$

Where $S_0$ is the waterplane area in the static condition. If the planes $xOz$
and $yOz$ are planes of symmetry, then $\mathbf{K}_{hs}$ is diagonal and $K_{34}
= K_{35} = K_{45} = 0$.
