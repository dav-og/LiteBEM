import litebem.preprocessing.mesh as lpm
import litebem.preprocessing.body as lpb
from litebem.preprocessing.bem_problem_definitions import RadiationProblem,DiffractionProblem
import litebem.solver.bem_solver as lps

hemi360Mesh = f'tests/unit/preprocessorRefData/hemisphere360.nemoh'

meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)

mesh = lpm.Mesh(meshVerts,meshFaces,name=f'hemi360')

body = lpb.Body(mesh)

body.add_all_rigid_body_dofs()

problemR = RadiationProblem(body=body,radiating_dof='Heave',omega=1)
problemD = DiffractionProblem(body=body)

solver = lps.BEMSolver()

result = solver.solve(problemR)
