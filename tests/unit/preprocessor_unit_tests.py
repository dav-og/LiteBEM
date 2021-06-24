import pytest
import numpy as np
import litebem.preprocessor.mesh as lpm
#import libDelhommeau.solver.bem_solver as bs
#from libDelhommeau.green_functions.delhommeau import Delhommeau
#from libDelhommeau.pre_processor.bem_problem_definitions import RadiationProblem
# from libDelhommeau.pre_processor.bodies import Body
# from libDelhommeau.pre_processor.mesh import read_nemoh_mesh, Mesh


# reference data

hemi360Mesh =  f'./preprocessorRefData/hemisphere360.nemoh'
hemi360Areas = f'./preprocessorRefData/hemisphere360PanelAreas.txt'
hemi360Centers = f'./preprocessorRefData/hemisphere360PanelCenters.txt'
hemi360Normals = f'./preprocessorRefData/hemisphere360PanelNormals.txt'
hemi360Radii = f'./preprocessorRefData/hemisphere360PanelRadii.txt'


# tests for reading nemoh mesh

def test_read_nemoh_mesh_nfaces():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    assert mesh.nPanels == 360

def test_read_nemoh_mesh_ntriangles():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    assert len(mesh.trianglesIDs) == 36

def test_read_nemoh_mesh_nquads():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    assert len(mesh.quadranglesIDs) == 324


# tests for computing mesh panel properties

def test_compute_panel_properties_normals():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    mesh.compute_panel_properties()
    assert len(mesh.panelUnitNormals) == 360

def test_compute_panel_properties_centers():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    mesh.compute_panel_properties()
    assert len(mesh.panelCenters) == 360

def test_compute_panel_properties_areas():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    mesh.compute_panel_properties()
    assert len(mesh.panelAreas) == 360

def test_compute_panel_properties_radii():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    mesh.compute_panel_properties()
    assert len(mesh.panelRadii) == 360

def test_panel_normal_values():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    mesh.compute_panel_properties()

    valuesCap = open(hemi360Normals)
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
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    mesh.compute_panel_properties()

    valuesCap = open(hemi360Areas)
    valuesCapList = []

    for line in valuesCap:
        line = line.rstrip()
        numbers = float(line)
        valuesCapList.append(numbers)

    for i in range(len(valuesCapList)):
        assert valuesCapList[i] == mesh.panelAreas[i]

def test_panel_centers():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    mesh.compute_panel_properties()

    valuesCap = open(hemi360Centers)
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
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    mesh.compute_panel_properties()

    valuesCap = open(hemi360Radii)
    valuesCapList = []

    for line in valuesCap:
        line = line.rstrip()
        numbers = float(line)
        valuesCapList.append(numbers)

    for i in range(len(valuesCapList)):
        assert round(valuesCapList[i],13) == round(mesh.panelRadii[i],13)

# TODO: create Body object in pre_processor.mesh that can be passed to
# RadiationProblem as an argument
# [ ]

# TODO: pass problems to solver
# [ ]

# TODO: post-processor to return A(w), B(w), f_FK(w) etc
# [ ]
