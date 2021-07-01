# Meshes

## Sections
- [The Nemoh mesh format](##the-nemoh-mesh-format)
- [Calculating panel properties](##calculating-panel-properties)

## The Nemoh mesh format
Function that takes in a path to a nemoh mesh file and returns headers, vertices
and panel vectors.

![](./images/nemohMesh.png)

An example of a nemoh mesh file read by this function is shown above. The first 
half of the file contains the panel vertices (index x y z). The second half of 
the file indicates what vertices make up each panel, each column designates one 
panel. **Note** that the vertices and panel data is separated by a line of 0's.

This function essentially generates a vector of vertices, and a vector
containing the panel definitions, that will be used to establish attributes when
defining a new mesh object. An example of this is seen in the following section
of code:

```Python
meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
```

get_triangle_quad_ids(): Method that is called by the `__init__()` method of the
mesh class in order to define two new mesh attributes: `self.trianglesIDs` and
`self.quadranglesIDs`. These attributes are vectors that contain indexes the
triangular and quadrangular panels respectively.

This method accomplishes this by identifying whether the panel definitions from
the `read_nemoh_mesh()` method contain three or four unique vertices. This is
highlighted by the image below: 

![](./images/panelIDs.png)

### Panel Geometry

![](./images/panelGeometry.png)

The panels of the mesh will either be triangles or quadrangles. The difference
being that triangle panels only define three unique coordinates while 
quadrangles define four unique coordinates.

---

## Calculating panel properties

\_\_init__():
Method that initializes the class attributes `self.vertices`, `self.panels`,
and `self.npanels`. Also, calls the `get_triangle_quad_ids()` method to 
define two more class attributes discussesd below. Lastly, calls the 
`compute_panel_properies()` method to define the last class attributes: 
`self.panelAreas`, `self.panelCenters`, `self.panelRadii`, and 
`self.panelUnitNormals`. These initializations occur in the following lines
of code:
```py
self.vertices = vertices
self.panels = panels
self.nPanels = len(panels)
self.get_triangle_quad_ids()
self.compute_panel_properties()
```
---


### Normals

The normal vectors of the two different panel shapes are calculated
using the following cross product equations.
$$ Triangle:  \vec{01}\times\vec{02} $$
$$ Quadrangle:  \vec{02}\times\vec{13} $$


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

The centeroid of a triangle is found by taking the average of the three 
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


### compute_panel_properies()

> Method that calculates the normal vectors, areas, centers, and radii for each
> panel of a mesh object 

---

#### Code Outline

```python
    panelUnitNormals = []
    panelAreas = []
    panelCenters = []
    panelRadii = [] 
```

> Initializes the lists of objects that this function is calculating

---

```python
    for iPanel, panel in enumerate(self.panels):
```

> Begins iterating through the rows of the self.panels matrix where `iPanel` is
> the index corresponding to the row and `panel` is the individual row 

---

```python
    if iPanel+1 in self.trianglesIDs:
```

> Checks whether the current panel corresponds to a triangular shaped panel

> **Note** that `iPanel+1` is used because the `get_triangle_quad_ids` method 
> references panels starting with 1 rather than 0

---

```python
triangleNormal = np.cross(self.vertices[panel[1]-1] - self.vertices[panel[0]-1], 
                          self.vertices[panel[2]-1] - self.vertices[panel[0]-1])
```
> Takes the cross product of vectors connecting coordinate 1 to coordinate 2 of 
> the panel and connecting coordinate 2 to coordinate 3 of the panel, resulting in
> a vector normal to the panel.

>**Note** that the vertices referenced are equal to `panel[1]-1`, this is because
>the panel data counts up from 1 while self.vertices matrix counts up from 0

---

```python
triangleNormalMag = np.linalg.norm(triangleNormal)
triangleUnitNormal = triangleNormal / triangleNormalMag
triangleArea = 0.5 * triangleNormalMag
```
> Calculates the magnitude of the normal vector, the unit normal vector, and the
> area of the triangular panel
