# Meshes

---

## Calculating Panel Properties

### Panel Geometry

![](./images/panelGeometry.png)

The panels of the mesh will either be triangles or quadrangles. The difference
being that triangle panels only define three unique coordinates while 
quadrangles define four unique coordinates.

### Unit Normal Vectors

The unit normal vectors of the two different panel shapes are calculated
using the following cross product equations and dividing by their respective lengths.

$$ 
Triangle:  \frac{\vec{01}\times\vec{02}}{|\vec{01}\times\vec{02}|}
$$

$$ 
Quadrangle:  \frac{\vec{02}\times\vec{13}}{|\vec{02}\times\vec{13}|} 
$$


### Areas

The area of a triangle is equal to the magnitude of the cross product of two
vectors that make up the triangle, divide by two. This can be seen in the
following equation:

$$ Area = \frac{|\vec{01}\times\vec{02}|}{2} $$

Quadrangles can simply be divided, along the diagonal, into two triangles:

![](./images/panelArea.png)

Making the area equal to the following equation:

$$ 
Area = \frac{|\vec{01}\times\vec{02}|}{2} + \frac{|\vec{03}\times\vec{02}|}{2} 
$$


### Centers

The centroid of a triangle is found by taking the average of the three 
vertices.

$$
Center = (\frac{x_{0}+x_{1}+x_{2}}{3},\frac{y_{0}+y_{1}+y_{2}}{3},
          \frac{z_{0}+z_{1}+z_{2}}{3})
$$

For the centroid of a quadrangle it must once again be split into two triangles.
Determine the centroids(c1, c2) and areas(A1, A2) of the two triangles using the
methods above, then use the following equation.

$$
Center = \frac{\vec{c_{1}}*A_{1} + \vec{c_{2}}*A_{2}}{A_{1}+A_{2}}
$$


### Radii

The radii of either a triangle or a quadrangle is defined as the largest distance
between the panel's centroid and one of its vertices. One must calculate the
distance between the centroid and all of the panels vertices and then determine 
which is largest.

---

## Calculating Mesh Properties

### Waterplane Polygons

Waterplane polygon simply refers to the shape created by all vertices on the cut waterplane, ordered either clockwise or anticlockwise. 
This polygon or list of ordered vertices is constructed by taking advantage of the way the panels on the waterplane are constructed.
These panels typically have two vertices on the waterplane, both of which are shared by another panel. This is shown in the image below. 
Starting with an arbitrary panel, both vertices are appended to a list in the preferred order. Left to right for anticlockwise. 
Next, the panel that shares the right vertices is found and its right vertices is appended to the list. This step is repeated until the polygon
is completed.

![](./images/waterplanePolygon.png)

### Waterplane Area

The waterplane area is calculated using the "shoelace method" shown in the equation below. This method finds the area of any polygon and only requires the list of
ordered vertices that constructs the polygon. 

$$
Area = \frac{1}{2}|(\sum_{i=1}^{n-1}{x_{i}y_{i+1}}) + x_{n}y_{1}
        - (\sum_{i=1}^{n-1}{x_{i+1}y_{i}}) + x_{1}y_{n}|
$$

### Moments of the Waterplane Area

#### First Moment of Area

The first moments of the waterplane area with respect to the x and y axis are used to determine $K_{34}$ and $K_{35}$ (see hydrostatics section). The equation for both of these moments is as follows:

$$
S_{x} = \int \int_{S_0} y   dS = \frac{1}{6} \sum_{i=1}^{n-1} (y_{i}+y_{i+1})(x_{i}y_{i+1} - x_{i+1}y_{i}) \\

S_{y} = \int \int_{S_0} x   dS = \frac{1}{6} \sum_{i=1}^{n-1} (x_{i}+x_{i+1})(x_{i}y_{i+1} - x_{i+1}y_{i})
$$

Where $ S_{0} $ is the waterplane area.

#### Second Moment of Area

The second moments of the waterplane area with respect to the x and y axis are used to determine $K_{44}$ and $K_{55}$ (see hydrostatics section). The equation for both of these moments is as follows:

$$
I_{x} = \int \int_{S_0} y^{2} dS = \frac{1}{12} \sum_{i=1}^{n-1} (y_{i}^{2}+y_{i}y_{i+1}+y_{i+1}^{2})(x_{i}y_{i+1} - x_{i+1}y_{i}) \\

I_{y} = \int \int_{S_0} x^{2} dS = \frac{1}{12} \sum_{i=1}^{n-1} (x_{i}^{2}+x_{i}x_{i+1}+x_{i+1}^{2})(x_{i}y_{i+1} - x_{i+1}y_{i})
$$

#### Product Moment of Area

Lastly, the product moment of the waterplane area is used to determine $K_{45}$ (see hydrostatics section). The equation for this moment is as follows:

$$
I_{xy} = \int \int_{S_0} xy dS = \frac{1}{24} \sum_{i=1}^{n-1} (x_{i}y_{i+1} + 2x_{i}y_{i} + 2x_{i+1}y_{i+1} + x_{i+1}y_{i})(x_{i}y_{i+1} - x_{i+1}y_{i})
$$

> **Note** that equations for the waterplane area and moments of the waterplane area require the area in question be a simple polygon. That is a polygon without holes and self intersections.

### Volume

The driving principle behind calculating the total volume, is breaking up the mesh into many tetrahedrons, all with a common point at the origin. Triangular panels create one tetrahedron while quadrangle panels create two tetrahedrons. The total volume is simply the sum of the volumes of each tetrahedron. This concept can be seen in the image below:

![](./images/meshTetrahedron.png)

The volume of each individual tetrahedron is calculated using the following equation:

$$
Volume = \frac{|\vec{A}\cdot{(\vec{B}\times{\vec{C}})}|}{6}
$$

The numerator $|a\cdot{(b\times{c})}|$, is the triple scalar product of those three vectors. The triple scalar product can also be calculated by finding the determinant of a matrix whose rows are the three vectors:

$$
Volume = \frac{1}{6} \det{\begin{vmatrix}\vec{A}\\\vec{B}\\\vec{C}\end{vmatrix}}
$$

> **Note** that the vertices A, B, and C are also vectors from the origin if the origin is [0,0,0]

### Center of Buoyancy

Determining the center of buoyancy for the mesh is a two step process. First, the centroid of each tetrahedron is found by taking the average of all four points that construct the tetrahedron:

$$
Centroid = \frac{\vec{A}+\vec{B}+\vec{C}+Origin}{4}
$$

Next, the method of composite parts is used to find the "z" component of the center of buoyancy of the mesh:

$$
z_{b} = \frac{\sum{(\rho_{w}V_{i})\overline{z_{i}}}}{\rho_{w}V_{total}}
$$

Where $\rho_{w}V_{i}$ is the mass of each individual tetrahedron, and 
$\overline{z_{i}}$ is the "z" component of the centroid for each tetrahedron.

> **Note** that each tetrahedron has a uniform density, so the centroid is equivalent to the center of gravity. Given that the mesh only includes sections below the water line, and that the density of water is used, the method of composite parts does in fact compute the center of buoyancy.


