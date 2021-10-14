import litebem.preprocessing.mesh as lpm
import litebem.preprocessing.body as lpb
from litebem.preprocessing.bem_problem_definitions import RadiationProblem,DiffractionProblem
import litebem.solver.bem_solver as lps
from litebem.postprocessing.results import assemble_dataset
import numpy as np

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

multiBody = floatBody+sparBody

problems = []

problem1_2 = RadiationProblem(body=multiBody,radiating_dof='float__Heave',omega=1)
problem2_1 = RadiationProblem(body=multiBody,radiating_dof='spar__Heave',omega=1)
# problem1_1 = RadiationProblem(body=floatBody,radiating_dof='Heave',omega=1)

problemD = DiffractionProblem(body=multiBody,omega=1)

problems.append(problem1_2)
problems.append(problem2_1)
problems.append(problemD)

solver = lps.BEMSolver()

resultR = solver.solve_all(problems)

dataset = assemble_dataset(resultR)
print(dataset)
# resultFloat = solver.solve(problem1_1)

# print(resultR[0].added_masses)
# print(resultR[1].added_masses)
# print(resultR[0].__module__)
