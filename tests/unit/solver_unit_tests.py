import litebem.preprocessing.mesh as lpm
import litebem.preprocessing.body as lpb
from litebem.preprocessing.bem_problem_definitions import RadiationProblem,DiffractionProblem
import litebem.solver.bem_solver as lps
import litebem.postprocessing.results as lpr

# reference data and variables for tests

floatMeshPath = f'tests/unit/preprocessorRefData/float-fixed.nemoh'
sparMeshPath = f'tests/unit/preprocessorRefData/spar-fixed.nemoh'

meshHeader,meshVerts,meshFaces = lpm.read_nemoh_mesh(floatMeshPath)
floatMesh = lpm.Mesh(meshVerts,meshFaces,name=f'float')

meshHeader,meshVerts,meshFaces = lpm.read_nemoh_mesh(sparMeshPath)
sparMesh = lpm.Mesh(meshVerts,meshFaces,name=f'spar')

floatBody = lpb.Body(floatMesh)
sparBody = lpb.Body(sparMesh)

floatBody.add_translation_dof(name='Heave')
sparBody.add_translation_dof(name='Heave')

# tests for using LiteBEM to setup and solve problems

def test_solve_single_body():
    problem = RadiationProblem(body=floatBody,radiating_dof='Heave',omega=1)
    solver = lps.BEMSolver()
    result = solver.solve(problem)

def test_solve_multi_body():
    multiBody = floatBody+sparBody
    problem = RadiationProblem(body=multiBody,radiating_dof='float__Heave',omega=1)
    solver = lps.BEMSolver()
    result = solver.solve(problem)