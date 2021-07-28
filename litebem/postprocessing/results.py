import numpy as np
# from litebem.preprocessing.bem_problem_definitions import LinearPotentialFlowProblem
from litebem.preprocessing.airy_waves import airy_waves_potential

class LinearPotentialFlowResult:

    def __init__(self, problem):
        self.problem = problem

        self.sources = None
        self.potential = None
        self.fs_elevation = {}

    # __str__ = LinearPotentialFlowProblem.__str__

    def __getattr__(self, name):
        """Direct access to the attributes of the included problem."""
        try:
            return getattr(self.problem, name)
        except AttributeError:
            raise AttributeError(f"{self.__class__} does not have a attribute named {name}.")

class DiffractionResult(LinearPotentialFlowResult):

    def __init__(self, problem):
        super().__init__(problem)
        self.forces = {}

    def store_force(self, dof, force):
        self.forces[dof] = 1j*self.omega*force

    @property
    def records(self):
        params = self.problem._asdict()
        FK = froude_krylov_force(self.problem)
        return [dict(**params,
                     influenced_dof=dof,
                     diffraction_force=self.forces[dof],
                     Froude_Krylov_force=FK[dof])
                for dof in self.influenced_dofs]

class RadiationResult(LinearPotentialFlowResult):

    def __init__(self, problem):
        super().__init__(problem)
        self.added_masses = {}
        self.radiation_dampings = {}

    def store_force(self, dof, force):
        self.added_masses[dof] = force.real
        if self.problem.omega == np.infty:
            self.radiation_dampings[dof] = 0
        else:
            self.radiation_dampings[dof] = self.problem.omega * force.imag

    @property
    def records(self):
        params = self.problem._asdict()
        return [dict(params,
                     influenced_dof=dof,
                     added_mass=self.added_masses[dof],
                     radiation_damping=self.radiation_dampings[dof])
                for dof in self.influenced_dofs]

def froude_krylov_force(pb, convention="Nemoh"):
    pressure = -1j * pb.omega * pb.rho * airy_waves_potential(pb.body.mesh.faces_centers, pb, convention=convention)
    forces = {}
    for dof in pb.influenced_dofs:
        # Scalar product on each face:
        normal_dof_amplitude_on_face = np.sum(pb.body.dofs[dof] * pb.body.mesh.faces_normals, axis=1)
        # Sum over all faces:
        forces[dof] = np.sum(pressure * normal_dof_amplitude_on_face * pb.body.mesh.faces_areas)
    return forces
