import pytest
import numpy as np
#import libDelhommeau.solver.bem_solver as bs
#from libDelhommeau.green_functions.delhommeau import Delhommeau
#from libDelhommeau.pre_processor.bem_problem_definitions import RadiationProblem
# from libDelhommeau.pre_processor.bodies import Body
# from libDelhommeau.pre_processor.mesh import read_nemoh_mesh, Mesh
import litebem.preprocessor.mesh as lpm


# test read mesh functions

boatMeshPath =  f'tests/unit/data/sphere360.nemoh'

normalFileCap = f'tests/unit/data/hemisphere/panelNormals.txt'
areaFileCap = f'tests/unit/data/hemisphere/panelAreas.txt'
centerFileCap = f'tests/unit/data/hemisphere/panelCenters.txt'
radiiFileCap = f'tests/unit/data/hemisphere/panelradii.txt'

def test_read_nemoh_mesh_nfaces():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
    assert mesh.nPanels == 360

def test_read_nemoh_mesh_ntriangles():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
    assert len(mesh.trianglesIDs) == 36

def test_read_nemoh_mesh_nquads():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
    assert len(mesh.quadranglesIDs) == 324

def test_compute_panel_properties_normals():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
    mesh.compute_panel_properties()
    assert len(mesh.panelUnitNormals) == 360
    
def test_compute_panel_properties_centers():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
    mesh.compute_panel_properties()
    assert len(mesh.panelCenters) == 360

def test_compute_panel_properties_areas():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
    mesh.compute_panel_properties()
    assert len(mesh.panelAreas) == 360

def test_compute_panel_properties_radii():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
    mesh.compute_panel_properties()
    assert len(mesh.panelRadii) == 360

def test_panel_normal_values():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
    mesh.compute_panel_properties()
    
    valuesCap = open(normalFileCap)
    valuesCapList = []

    for line in valuesCap:
        line = line.rstrip()
        strings = line.split(' ')
        numbers = []
        for value in strings:
            value = float(value)
            numbers.append(value)

        valuesCapList.append(np.array(numbers))
    
    for i in range(len(valuesCapList)):
        for j in range(len(valuesCapList[i])):
            assert valuesCapList[i][j] == mesh.panelUnitNormals[i][j]

def test_panel_area_values():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
    mesh.compute_panel_properties()

    valuesCap = open(areaFileCap)
    valuesCapList = []

    for line in valuesCap:
        line = line.rstrip()
        numbers = float(line)
        valuesCapList.append(numbers)
    
    for i in range(len(valuesCapList)):
        assert valuesCapList[i] == mesh.panelAreas[i]

def test_panel_centers():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
    mesh.compute_panel_properties()
    
    valuesCap = open(centerFileCap)
    valuesCapList = []

    for line in valuesCap:
        line = line.rstrip()
        strings = line.split(' ')
        numbers = []
        for value in strings:
            value = float(value)
            numbers.append(value)

        valuesCapList.append(np.array(numbers))

    for i in range(len(valuesCapList)):
        for j in range(len(valuesCapList[i])):
            assert round(valuesCapList[i][j],13) == round(mesh.panelCenters[i][j],13)

def test_panel_radii():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
    mesh.compute_panel_properties()

    valuesCap = open(radiiFileCap)
    valuesCapList = []

    for line in valuesCap:
        line = line.rstrip()
        numbers = float(line)
        valuesCapList.append(numbers)

    for i in range(len(valuesCapList)):
        assert round(valuesCapList[i],13) == round(mesh.panelRadii[i],13)

# meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
# mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
# mesh.compute_face_normals_areas()

# TODO: create Body object in pre_processor.mesh that can be passed to
# RadiationProblem as an argument
# [ ]

# TODO: include some methods in Body object to calculate mesh properties -
# areas, normals, centers.
# [ ]

# TODO: pass problems to solver
# [ ]

# TODO: post-processor to return A(w), B(w), f_FK(w) etc
# [ ]
