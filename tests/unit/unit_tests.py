import pytest
import numpy as np
#import libDelhommeau.solver.bem_solver as bs
#from libDelhommeau.green_functions.delhommeau import Delhommeau
#from libDelhommeau.pre_processor.bem_problem_definitions import RadiationProblem
# from libDelhommeau.pre_processor.bodies import Body
# from libDelhommeau.pre_processor.mesh import read_nemoh_mesh, Mesh
import litebem.preprocessor.mesh as lpm


# test read mesh functions

boatMeshPath =  f'../unit/data/boat_200.mar'

def test_read_nemoh_mesh_nfaces():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
    assert mesh.nfaces == 500

def test_read_nemoh_mesh_ntriangles():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
    assert len(mesh.trianglesIDs) == 500

def test_read_nemoh_mesh_nquads():
    meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
    mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
    assert len(mesh.quadranglesIDs) == 0

# def test_compute_face_normals():
#     meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(boatMeshPath)
#     mesh = lpm.Mesh(meshVerts, meshFaces, name=f'boatMesh')
#     mesh.compute_face_normals_areas()
#     assert len(mesh.faceUnitNormals) == 500

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
