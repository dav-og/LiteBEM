from os import path
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
        self.name = 'mesh'
        self.get_triangle_quad_ids()
        self.compute_panel_properties()
        self.construct_polygons()
        self.waterplane_area()

    def get_triangle_quad_ids(self):
        '''
        identify which panels are quadrilateral and which are triangles

        Notes
        -----
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

    def unit_normal_vector(self, vecA, vecB):
        '''calculate unit normal from two vectors'''
        normVec = np.cross(vecA, vecB)
        normLen = np.linalg.norm(normVec)
        unitNorm = normVec / normLen
        return normVec, normLen, unitNorm

    def vector_area_triangle(self, normLen):
        '''calculate area of a triangle'''
        return normLen * 0.5

    def center_triangle(self, vertA, vertB, vertC):
        '''calculate center of a triangle panel'''
        return (vertA + vertB + vertC)/3.0

    def center_quad(self, vertA, vertB, vertC, vertD, areaTriA, areaTriB, quadArea):
        '''calculate center of a quad panel'''
        # TODO: check different method for calculation (weight 4
        # constituent triangles, not just 2!)
        centerTriA = self.center_triangle(vertA, vertB, vertC)
        centerTriB = self.center_triangle(vertA, vertC, vertD)
        # triABD
        # triBCD
        quadCenter = (areaTriA*centerTriA + areaTriB*centerTriB)/(quadArea)
        return quadCenter

    def tri_panel_properties(self, panel):
        '''return triangle panel properties'''
        # fix: subtract 1 to correct for nemoh mesh indexing convention
        # TODO: move this fix higher up
        vertA = self.vertices[panel[0]-1]
        vertB = self.vertices[panel[1]-1]
        vertC = self.vertices[panel[2]-1]
        panelVertices = [vertA, vertB, vertC]

        vecAB = vertB - vertA
        vecAC = vertC - vertA
        triNorm, triNormLen, triUnitNorm = self.unit_normal_vector(vecAB, vecAC)
        triArea = self.vector_area_triangle(triNormLen)
        triCenter = self.center_triangle(vertA, vertB, vertC)

        radiiMag = []
        for coord in panelVertices:
            radiiVec = coord - triCenter
            radiiMag.append(np.linalg.norm(radiiVec))
        triRadius = max(radiiMag)

        return triUnitNorm, triArea, triCenter, triRadius

    def quad_panel_properties(self, panel):
        '''return quad panel properties'''
        # fix: subtract 1 to correct for nemoh mesh indexing convention
        # TODO: move this fix higher up
        vertA = self.vertices[panel[0]-1]
        vertB = self.vertices[panel[1]-1]
        vertC = self.vertices[panel[2]-1]
        vertD = self.vertices[panel[3]-1]

        panelVertices = [vertA, vertB, vertC, vertD]

        vecAC = vertC - vertA
        vecBD = vertD - vertB
        vecAB = vertB - vertA
        vecAD = vertD - vertA

        quadNorm, quadNormLen, quadUnitNorm = self.unit_normal_vector(vecAC, vecBD)
        triANorm, triANormLen, triAUnitNorm = self.unit_normal_vector(vecAB, vecAC)
        triBNorm, triBNormLen, triBUnitNorm = self.unit_normal_vector(vecAD, vecAC)
        areaTriA = self.vector_area_triangle(triANormLen)
        areaTriB = self.vector_area_triangle(triBNormLen)
        quadArea = areaTriA + areaTriB

        # center calculation
        quadCenter = self.center_quad(vertA, vertB, vertC, vertD, areaTriA,
                                      areaTriB, quadArea)

        # radius calculation
        radiiMag = []
        for coord in panelVertices:
            radiiVec = coord-quadCenter
            radiiMag.append(np.linalg.norm(radiiVec))
        quadRadius = max(radiiMag)

        return quadCenter, quadUnitNorm, quadArea, quadRadius

    def compute_panel_properties(self):
        '''
        calculate panel normal vectors, areas, centers and radii

        Notes
        -----
        - TODO: add warning/error for triangular panels that are not defined by
          repeating vertices 1 and 4
        '''
        panelUnitNormals = []
        panelAreas = []
        panelCenters = []
        panelRadii = []
        for iPanel, panel in enumerate(self.panels):
            if iPanel+1 in self.trianglesIDs:
                triUnitNorm, triArea, triCenter, triRadius = self.tri_panel_properties(panel)
                panelUnitNormals.append(triUnitNorm)
                panelAreas.append(triArea)
                panelCenters.append(triCenter)
                panelRadii.append(triRadius)
            elif iPanel+1 in self.quadranglesIDs:
                quadCenter, quadUnitNorm, quadArea, quadRadius = self.quad_panel_properties(panel)
                panelCenters.append(quadCenter)
                panelUnitNormals.append(quadUnitNorm)
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

        self.panelAreas = np.asarray(panelAreas)
        self.panelCenters = np.asarray(panelCenters)
        self.panelRadii = np.asarray(panelRadii)
        self.panelUnitNormals = np.asarray(panelUnitNormals)

    def waterplane_area(self):
        '''calculates the waterplane area for the given mesh'''
        sum1 = 0
        sum2 = 0

        vertices = np.asarray(self.vertices)
        points = vertices[self.polygons]
        points = points[:-1,0:2]

        for i in range(len(points)):
            index2 = (i+1)%len(points)
            prod = points[i,0]*points[index2,1]
            sum1 += prod

        for i in range(len(points)):
            index2 = (i+1)%len(points)
            prod = points[index2,0]*points[i,1]
            sum2 += prod

        self.waterplaneArea = abs(1/2*(sum1-sum2))

    def construct_polygons(self):
        '''
        orders the vertices on the cut water plane into a continuous polygon
        '''

        vertices = np.asarray(self.vertices)
        panels = np.asarray(self.panels)
        panels = panels-1

        z = vertices[:,2]

        verticesOnPlane = z == 0
        panelsOn = verticesOnPlane[panels].sum(axis=1)
        panelsOnIDs = np.nonzero(panelsOn)
        panelsOnPlane = panels[panelsOnIDs[0]]

        panelPlaneVertices = dict()

        for i in range(len(panelsOnPlane)):
            for j in range(len(panelsOnPlane[i])):
                if verticesOnPlane[panelsOnPlane[i,j]] == True:
                    topLeft = panelsOnPlane[i,j+1]
                    topRight = panelsOnPlane[i,j]
                    panelPlaneVertices[topLeft] = topRight
                    break
        path = list()
        while True:
            vLeftInit,vRight = panelPlaneVertices.popitem()
            path.append(vLeftInit)
            path.append(vRight)
            vLeftNew = vRight
            while True:
                try:
                    vRight = panelPlaneVertices.pop(vLeftNew)
                    path.append(vRight)
                    vLeftNew = vRight
                except KeyError:
                    break
            break
        self.polygons = path

    def compute_volume_cob(self, rhoW=1023):
        '''calculates the displaced volume and center of buoyancy of the mesh'''
        panels = np.asarray(self.panels)-1
        vertices = np.asarray(self.vertices)
        origin = np.asarray([0,0,0])

        volumes = list()
        centroids = list()

        for ipanel,panel in enumerate(panels):

            if ipanel+1 in self.trianglesIDs:
                vertA = vertices[panel[0]]
                vertB = vertices[panel[1]]
                vertC = vertices[panel[2]]

                Vi = np.linalg.det([vertA, vertB, vertC])/6
                Ci = (vertA + vertB + vertC + origin)/4

                volumes.append(Vi)
                centroids.append(Ci)

            elif ipanel+1 in self.quadranglesIDs:
                vertA = vertices[panel[0]]
                vertB = vertices[panel[1]]
                vertC = vertices[panel[2]]
                vertD = vertices[panel[3]]

                Vi1 = np.linalg.det([vertA, vertB, vertC])/6
                Vi2 = np.linalg.det([vertA, vertC, vertD])/6
                Ci1 = (vertA + vertB + vertC + origin)/4
                Ci2 = (vertA + vertC + vertD + origin)/4

                volumes.append(Vi1)
                volumes.append(Vi2)
                centroids.append(Ci1)
                centroids.append(Ci2)

        volumeTotal = sum(volumes)
        zCentroids = np.asarray(centroids)[:,2]

        sumZb = 0

        for i in range(len(zCentroids)):
            sumZb += rhoW*volumes[i]*zCentroids[i]

        volumeTotal = sum(volumes)
        zb = sumZb/(rhoW*volumeTotal)

        return volumeTotal,zb

    def compute_hydrostatic_stiffness(self, cog, volume=True, cob=True,
                                      rhoW=1023, g=9.81):
        if volume == True:
            values = self.compute_volume_cob()
            volume = values[0]
            if cob == True:
                cob = values[1]

        moments = self.compute_moments_of_area()

        gmT = moments[2]/volume - (cog-cob)
        gmL = moments[3]/volume - (cog-cob)

        K33 = rhoW*g*self.waterplaneArea
        K34 = rhoW*g*moments[0]
        K35 = -rhoW*g*moments[1]
        K44 = rhoW*g*volume*gmT
        K45 = rhoW*g*moments[4]
        K55 = rhoW*g*volume*gmL

        stiffnessMatrix = np.array([[0,0,0,0,0,0],
                                    [0,0,0,0,0,0],
                                    [0,0,K33,K34,K35,0],
                                    [0,0,K34,K44,K45,0],
                                    [0,0,K35,K45,K55,0],
                                    [0,0,0,0,0,0]])

        stiffnessMatrix[np.fabs(stiffnessMatrix) < 1e-4] = 0

        return stiffnessMatrix

    def compute_moments_of_area(self):
        sumSx = 0
        sumSy = 0
        sumIx = 0
        sumIy = 0
        sumIxy = 0

        vertices = np.asarray(self.vertices)
        points = vertices[self.polygons]
        points = points[:-1,0:2]

        moments = list()

        for i in range(len(points)):
            i2 = (i+1) % len(points)

            termSx = points[i,1] + points[i2,1]
            termSy = points[i,0] + points[i2,0]
            termIx = points[i,1]**2 + points[i,1]*points[i2,1] + points[i2,1]**2
            termIy = points[i,0]**2 + points[i,0]*points[i2,0] + points[i2,0]**2
            termIxy = points[i,0]*points[i2,1] + 2*points[i,0]*points[i,1] + 2*points[i2,0]*points[i2,1] + points[i2,0]*points[i,1]

            area = points[i,0]*points[i2,1] - points[i2,0]*points[i,1]

            sumSx += termSx*area
            sumSy += termSy*area
            sumIx += termIx*area
            sumIy += termIy*area
            sumIxy += termIxy*area

        Sx = (1/6)*sumSx
        Sy = (1/6)*sumSy
        Ix = (1/12)*sumIx
        Iy = (1/12)*sumIy
        Ixy = (1/24)*sumIxy

        moments.append(Sx)
        moments.append(Sy)
        moments.append(Ix)
        moments.append(Iy)
        moments.append(Ixy)

        return moments

    @property
    def quadraturePoints(self):
        return (self.panelCenters.reshape((self.nPanels, 1, 3)),  # Points
                self.panelAreas.reshape((self.nPanels, 1)))       # Weights

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
