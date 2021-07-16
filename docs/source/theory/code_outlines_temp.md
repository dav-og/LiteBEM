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

## init method

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
