import pytest
import numpy as np
import litebem.preprocessing.mesh as lpm
import litebem.preprocessing.body as lpb
import litebem.preprocessing.bem_problem_definitions as lpd

# reference data

hemi360Mesh =  f'tests/unit/preprocessorRefData/hemisphere360.nemoh'
hemi360Areas = f'tests/unit/preprocessorRefData/hemisphere360PanelAreas.txt'
hemi360Centers = f'tests/unit/preprocessorRefData/hemisphere360PanelCenters.txt'
hemi360Normals = f'tests/unit/preprocessorRefData/hemisphere360PanelNormals.txt'
hemi360Radii = f'tests/unit/preprocessorRefData/hemisphere360PanelRadii.txt'


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

# tests for hydrostatic calculations

def test_polygon_length():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    mesh.construct_polygons()
    assert len(mesh.polygons) == 37

def test_waterplane_area():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    assert round(mesh.waterplaneArea,1) == 3.1

def test_compute_volume_cob():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    volume,zb = mesh.compute_volume_cob()
    assert round(volume,3) == 2.071
    assert round(zb,3) == -0.374

def test_compute_moments_of_area():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    moments = mesh.compute_moments_of_area()
    assert len(moments) == 5

def test_compute_hydrostatic_stiffness():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    stiffnessMatrix = mesh.compute_hydrostatic_stiffness(0)
    assert round(stiffnessMatrix[2,2],0) == 31368
    assert round(stiffnessMatrix[3,3],3) == 24.655
    assert round(stiffnessMatrix[4,4],3) == 24.655


# tests for problem set up

def test_body_definition():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    body = lpb.Body(mesh)

def test_problem_definition():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'hemi360')
    body = lpb.Body(mesh)
    body.add_all_rigid_body_dofs()
    problemR = lpd.RadiationProblem(body=body,radiating_dof="Heave",omega=1)
    problemD = lpd.DiffractionProblem(body=body)
