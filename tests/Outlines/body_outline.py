import litebem.preprocessing.mesh as lpm
import litebem.preprocessing.body as lpb
from litebem.preprocessing.bem_problem_definitions import RadiationProblem,DiffractionProblem
import litebem.solver.bem_solver as lps
import numpy as np

hemi360Mesh = f'tests/unit/preprocessorRefData/hemisphere360.nemoh'

meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)

mesh = lpm.Mesh(meshVerts,meshFaces,name=f'hemi360')
print(np.asarray(mesh.panels))

body = lpb.Body(mesh)

# body.add_translation_dof(name='Heave')

# problems = []
# omega = np.linspace(0.1,4,40)

# for omega in omega:
#     problem = RadiationProblem(body=body,radiating_dof='Heave',omega=omega)
#     problems.append(problem)

# solver = lps.BEMSolver()

# resultR = solver.solve_all(problems)

# addedMass = []
# radiationDamping = []

# addedMassData = open('tests/unit/solverRefData/addedMass.txt','w')
# radiationDampingData = open('tests/unit/solverRefData/radiationDamping.txt','w')

# for result in resultR:
#     addedMassData.write(str(result.added_masses['Heave']) + '\n')
#     radiationDampingData.write(str(result.radiation_dampings['Heave']) + '\n')

# addedMassData.close()
# radiationDampingData.close()

