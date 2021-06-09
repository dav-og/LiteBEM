import numpy as np
from collections import Counter

from itertools import count

class Mesh():
    """Mesh class

    Parameters
    ----------
    vertices : array_like of shape (nv, 3)
        Array of mesh vertices coordinates. Each line of the array represents one vertex
        coordinates
    panels : array_like of shape (nf, 4)
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

    def get_triangle_quad_ids(self):
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
        '''calculate panel normal vectors, areas, centers and radii'''
        panelUnitNormals = []
        panelAreas = []
        panelCenters = []
        panelRadii = []
        print(self.panels)
        print(self.vertices)
        # print(f'test1: {self.vertices[self.panels[489][2]]}')
        for iPanel, panel in enumerate(self.panels):
            if iPanel+1 in self.trianglesIDs:
                triangleNormal = np.cross(self.vertices[panel[1]-1] - self.vertices[panel[0]-1],
                                          self.vertices[panel[2]-1] - self.vertices[panel[0]-1])
                triangleNormalMag = np.linalg.norm(triangleNormal)
                triangleUnitNormal = triangleNormal / triangleNormalMag
                triangleArea = 0.5 * triangleNormalMag
                #print(iPanel)
                triangleCenter = (self.vertices[panel[0]-1] + self.vertices[panel[1]-1] + self.vertices[panel[2]-1])/3.0
                #triangleCenter = np.sum(self.vertices[panel[0:3]])/3.0
                triangleRadius = np.max([np.abs(self.vertices[panel[0]-1] - triangleCenter),
                                         np.abs(self.vertices[panel[1]-1] - triangleCenter),
                                         np.abs(self.vertices[panel[2]-1] - triangleCenter)])
                panelUnitNormals.append(triangleUnitNormal)
                panelAreas.append(triangleArea)
                panelCenters.append(triangleCenter)
                panelRadii.append(triangleRadius)
            elif iPanel+1 in self.quadranglesIDs:
                quadNormal = np.cross(self.vertices[panel[2]-1] - self.vertices[panel[0]-1],
                                      self.vertices[panel[3]-1] - self.vertices[panel[1]-1])
                quadNormalMag = np.linalg.norm(quadNormal)
                quadUnitNormal = quadNormal / quadNormalMag
                quadArea = quadNormalMag * 0.5

                quadTri1Center = np.sum(self.vertices[panel[[0,1,2]]])/3
                quadTri2Center = np.sum(self.vertices[panel[[0,2,3]]])/3
                quadTri3Center = np.sum(self.vertices[panel[[0,1,3]]])/3
                quadTri4Center = np.sum(self.vertices[panel[[1,2,3]]])/3

                # intersection method:
                # https://mathworld.wolfram.com/Line-LineIntersection.html 
                x1 = quadTri1Center
                x2 = quadTri2Center
                x3 = quadTri3Center
                x4 = quadTri4Center

                a = x2 - x1
                b = x4 - x3
                c = x3 - x1

                x = x1 + a*(np.dot(np.cross(c, b), np.cross(a, b)) /
                            (np.linalg.norm(np.cross(a, b))**2))
                quadCenter = x
                quadRadius = np.max([np.abs(self.vertices[panel[0]-1] - quadCenter),
                                     np.abs(self.vertices[panel[1]-1] - quadCenter),
                                     np.abs(self.vertices[panel[2]-1] - quadCenter),
                                     np.abs(self.vertices[panel[3]-1] - quadCenter)])
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
        self.panelCenters = panelCenters
        self.panelUnitNormals = panelUnitNormals
        self.panelAreas = panelAreas
        self.panelRadii = panelRadii

    def compute_panel_radii(self):
        '''calculate panel radii: defined as distance between panel center and
        furthest vertex'''

        # self.panelRadii = panelRadii

    # Capytaine approach:
    # https://github.com/mancellin/capytaine/blob/4fb70c71bd791272cca548a4ea0c92b24a49622f/capytaine/meshes/properties.py#L12
    # NEMOH approach:
    # https://github.com/LHEEA/Nemoh/blob/49393be96bd590e267bfbc16347b665cda0edeb8/preProcessor/Mesh.f90#L207


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
