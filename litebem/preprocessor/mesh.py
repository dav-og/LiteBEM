import numpy as np

class Mesh():
    """Mesh class

    Parameters
    ----------
    vertices : array_like of shape (nVertices, 3)
        Array of mesh vertices coordinates. Each line of the array represents one vertex
        coordinates
    panels : array_like of shape (nPanels, 4)
        Arrays of mesh connectivities for panels. Each line of the array represents indices of
        vertices that form the panel, expressed in counterclockwise order to ensure outward normals
        description.
    name : str, optional
        The name of the mesh.
    """

    def __init__(self, vertices=None, panels=None, name=None):
        self.vertices = vertices
        self.panels = panels
        self.nPanels = len(panels)
        self.get_triangle_quad_ids()
        self.compute_panel_properties()

    def get_triangle_quad_ids(self):
        '''
        identify which panels are quadrilateral and which are triangles

        Notes
        -----
        - this function is called upon instantiation of the Mesh class
        - this function will identify if any panels have the same vertex listed
          twice
        - TODO: compute_panel_properties() expects the first and last vertex to
          be the same for triangular panels; we could improve the robustness by
          identifying which vertices are the same and modifying the vector
          expressions accordingly
        '''

        trianglesIDs = []
        quadranglesIDs = []
        for iPanel, panel in enumerate(self.panels):
            if len(np.unique(panel)) == 3:
                trianglesIDs.append(iPanel+1)
            elif len(np.unique(panel)) == 4:
                quadranglesIDs.append(iPanel+1)
            else:
                raise ValueError(f'Panel {iPanel} has {len(np.unique(panel))} unique '
                                 f'vertices. \n'
                                 f'\tOnly triangular and quadrilateral panels '
                                 f'are currently supported. \n')
        self.trianglesIDs = trianglesIDs
        self.quadranglesIDs = quadranglesIDs

    def compute_panel_properties(self):
        '''
        calculate panel normal vectors, areas, centers and radii

        Notes
        -----
        - this function is called upon instantiation of the Mesh class
        - several vector expressions are implemented to create class attributes
          for the panel normals, areas, centers and radii
        - TODO: create separate functions for th different vector operations to
          shorten this particular function
        - TODO: add warning/error for triangular panels that are not defined by
          repeating vertices 1 and 4
        '''

        panelUnitNormals = []
        panelAreas = []
        panelCenters = []
        panelRadii = []
        for iPanel, panel in enumerate(self.panels):
            if iPanel+1 in self.trianglesIDs:
                triangleNormal = np.cross(self.vertices[panel[1]-1] - self.vertices[panel[0]-1],
                                          self.vertices[panel[2]-1] - self.vertices[panel[0]-1])
                triangleNormalMag = np.linalg.norm(triangleNormal)
                triangleUnitNormal = triangleNormal / triangleNormalMag
                triangleArea = 0.5 * triangleNormalMag
                triangleCenter = (self.vertices[panel[0]-1] + self.vertices[panel[1]-1] + self.vertices[panel[2]-1])/3.0

                panelVertices = [self.vertices[panel[0]-1], self.vertices[panel[1]-1],
                                 self.vertices[panel[2]-1]]
                radiiMag = []

                for coord in panelVertices:
                    radiiVector = coord-triangleCenter
                    radiiMag.append(np.linalg.norm(radiiVector))

                triangleRadius = max(radiiMag)

                panelUnitNormals.append(triangleUnitNormal)
                panelAreas.append(triangleArea)
                panelCenters.append(triangleCenter)
                panelRadii.append(triangleRadius)

            elif iPanel+1 in self.quadranglesIDs:
                quadNormal = np.cross(self.vertices[panel[2]-1] - self.vertices[panel[0]-1],
                                      self.vertices[panel[3]-1] - self.vertices[panel[1]-1])
                quadNormalMag = np.linalg.norm(quadNormal)
                quadUnitNormal = quadNormal / quadNormalMag

                # area calculation
                a1 = np.linalg.norm(np.cross(self.vertices[panel[1]-1] - self.vertices[panel[0]-1],
                                             self.vertices[panel[2]-1] - self.vertices[panel[0]-1]))*0.5
                a2 = np.linalg.norm(np.cross(self.vertices[panel[3]-1] - self.vertices[panel[0]-1],
                                             self.vertices[panel[2]-1] - self.vertices[panel[0]-1]))*0.5
                quadArea = a1 + a2

                # center calculation 
                # TODO: check different method for calculation
                c1 = (self.vertices[panel[0]-1] + self.vertices[panel[1]-1] + self.vertices[panel[2]-1])/3.0
                c2 = (self.vertices[panel[0]-1] + self.vertices[panel[2]-1] + self.vertices[panel[3]-1])/3.0
                quadCenter = (a1*c1 + a2*c2)/(quadArea)

                # radius calculation
                panelVertices = [self.vertices[panel[0]-1], self.vertices[panel[1]-1],
                                 self.vertices[panel[2]-1], self.vertices[panel[3]-1]]
                radiiMag = []
                for coord in panelVertices:
                    radiiVector = coord-quadCenter
                    radiiMag.append(np.linalg.norm(radiiVector))
                quadRadius = max(radiiMag)

                panelCenters.append(quadCenter)
                panelUnitNormals.append(quadUnitNormal)
                panelAreas.append(quadArea)
                panelRadii.append(quadRadius)
            else:
                print(f'iPanel : {iPanel}')
                print(f'panel : {panel}')
                print(f'self.trianglesIDs : {self.trianglesIDs}')
                raise ValueError(f'Panel {iPanel} has {len(np.unique(panel))} unique '
                                 f'vertices. \n'
                                 f'\tOnly triangular and quadrilateral panels '
                                 f'are currently supported. \n')

        self.panelAreas = panelAreas
        self.panelCenters = panelCenters
        self.panelRadii = panelRadii
        self.panelUnitNormals = panelUnitNormals

def read_nemoh_mesh(pathToMesh):#
    '''
    reads nemoh mesh file; return headers, vertices and panels.

    Parameters
    ----------
    pathToMesh: str
        path to the nemoh mesh file (i.e. .mar or .nemoh format mesh)

    Returns
    -------
    header : array
    vertices : array
    panels : array

    Raises
    ------
    None

    Notes
    -----
    - nemoh meshes have two parts: a list of vertices in 3D space, and a list of
      panel definitions that describes how the vertices are joined together
    - this read function is expecting the use of lines containing 4 or more
      zeros in the mesh file to seperate the list of vertices and panels (and at
      the end of the file)
    '''
    vertices = []
    panels = []
    ftoggle = 0 # toggle - if reading mesh vertices or panel definitions
    with open(pathToMesh) as f:
        for iline, line in enumerate(f):
            # read header line
            if iline == 0:
                header = np.asarray(line.split(), dtype=int)
                continue
            # catch '0 0 0 0' divider in nemoh mesh file
            if np.count_nonzero(np.asarray(line.split()) == '0') >= 4:
                ftoggle = 1
                continue
            # append each vertex to list
            if ftoggle == 0:
                vertices.append(np.asarray(line.split(), dtype=float)[1:])
                continue
            # append each panel to list
            if ftoggle == 1:
                panels.append(np.asarray(line.split(), dtype=int))
                continue
            if np.count_nonzero(np.asarray(line.split()) == '0') >= 4:
                break
    return header, vertices, panels
