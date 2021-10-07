import litebem.preprocessing.mesh as lpm
import litebem.preprocessing.body as lpb
from litebem.preprocessing.bem_problem_definitions import RadiationProblem,DiffractionProblem
import litebem.solver.bem_solver as lps
import numpy as np
import time

start_time = time.time()

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

print(multiBody.dofs)

omega = np.linspace(0.1,10,150)


problem = [RadiationProblem(body=multiBody,radiating_dof='float__Heave',omega=omega)
           for omega in omega
]

solver = lps.BEMSolver()

resultR = solver.solve_all(problem)

multiAddedMassData = open('tests/unit/solverRefData/multiAddedMassLiteCouple.txt','w')
multiRadiationDampingData = open('tests/unit/solverRefData/multiRadiationDampingLite.txt','w')

for result in resultR:
    multiAddedMassData.write(str(result.added_masses['spar__Heave']) + '\n')
    multiRadiationDampingData.write(str(result.radiation_dampings['float__Heave']) + '\n')

print("--- %s seconds ---" % (time.time() - start_time))