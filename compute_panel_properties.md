# compute_panel_properies()

> Method that calculates the normal vectors, areas, centers, and radii for each
> panel of a mesh object 

---

## Code Outline

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
