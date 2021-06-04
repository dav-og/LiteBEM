#import logging
import numpy as np

from datetime import datetime
from libDelhommeau.green_functions.delhommeau import Delhommeau
from libDelhommeau.solver import linear_solvers

#from capytaine.bem.engines import BasicMatrixEngine, HierarchicalToeplitzMatrixEngine
#from capytaine.io.xarray import problems_from_dataset, assemble_dataset, kochin_data_array

#LOG = logging.getLogger(__name__)

from collections import OrderedDict
from functools import wraps

def delete_first_lru_cache(maxsize=1):
    """Behaves like functools.lru_cache(), but the oldest data in the cache is
    deleted *before* computing a new one, in order to limit RAM usage when
    stored objects are big."""

    def decorator(f):
        cache = OrderedDict()

        @wraps(f)
        def decorated_f(*args, **kwargs):
            # /!\ cache only args

            if args in cache:
                # Get item in cache
                return cache[args]

            if len(cache) + 1 > maxsize:
                # Drop oldest item in cache.
                cache.popitem(last=False)

            # Compute and store
            result = f(*args, **kwargs)
            cache[args] = result

            return result

        return decorated_f

    return decorator

# class MatrixEngine(ABC):
#     """Abstract method to build a matrix."""

#     @abstractmethod
#     def build_matrices(self, mesh1, mesh2, free_surface, sea_bottom, wavenumber, green_function):
#         pass

#     def build_S_matrix(self, *args, **kwargs):
#         """Similar to :code:`build_matrices`, but returning only :math:`S`"""
#         S, _ = self.build_matrices(*args, **kwargs)  # Could be optimized...
#         return S

class BasicMatrixEngine():#MatrixEngine):
    """
    Simple engine that assemble a full matrix (except for one reflection symmetry).
    Basically only calls :code:`green_function.evaluate`.
    Parameters
    ----------
    linear_solver: str or function, optional
        Setting of the numerical solver for linear problems Ax = b.
        It can be set with the name of a preexisting solver
        (available: "direct" and "gmres", the latter is the default choice)
        or by passing directly a solver function.
    matrix_cache_size: int, optional
        number of matrices to keep in cache
    """

    available_linear_solvers = {#'direct': linear_solvers.solve_directly,
                                'gmres': linear_solvers.solve_gmres}

    def __init__(self, *, linear_solver='gmres', matrix_cache_size=1):

        if linear_solver in self.available_linear_solvers:
            self.linear_solver = self.available_linear_solvers[linear_solver]
        else:
            self.linear_solver = linear_solver

        if matrix_cache_size > 0:
            self.build_matrices = delete_first_lru_cache(maxsize=matrix_cache_size)(self.build_matrices)

        self.exportable_settings = {
            'engine': 'BasicMatrixEngine',
            'matrix_cache_size': matrix_cache_size,
            'linear_solver': str(linear_solver),
        }

    def build_matrices(self, mesh1, mesh2, free_surface, sea_bottom, wavenumber, green_function):
        r"""Build the influence matrices between mesh1 and mesh2.
        Parameters
        ----------
        mesh1: Mesh or CollectionOfMeshes
            mesh of the receiving body (where the potential is measured)
        mesh2: Mesh or CollectionOfMeshes
            mesh of the source body (over which the source distribution is integrated)
        free_surface: float
            position of the free surface (default: :math:`z = 0`)
        sea_bottom: float
            position of the sea bottom (default: :math:`z = -\infty`)
        wavenumber: float
            wavenumber (default: 1.0)
        green_function: AbstractGreenFunction
            object with an "evaluate" method that computes the Green function.
        Returns
        -------
        tuple of matrix-like
            the matrices :math:`S` and :math:`K`
        """

        if (isinstance(mesh1, ReflectionSymmetricMesh)
                and isinstance(mesh2, ReflectionSymmetricMesh)
                and mesh1.plane == mesh2.plane):

            S_a, V_a = self.build_matrices(
                mesh1[0], mesh2[0], free_surface, sea_bottom, wavenumber,
                green_function)
            S_b, V_b = self.build_matrices(
                mesh1[0], mesh2[1], free_surface, sea_bottom, wavenumber,
                green_function)

            return BlockSymmetricToeplitzMatrix([[S_a, S_b]]), BlockSymmetricToeplitzMatrix([[V_a, V_b]])

        else:
            return green_function.evaluate(
                mesh1, mesh2, free_surface, sea_bottom, wavenumber,
            )

class BEMSolver:
    """
    Solver for linear potential flow problems.
    Parameters
    ----------
    green_function: AbstractGreenFunction
        Object handling the computation of the Green function.
    engine: MatrixEngine
        Object handling the building of matrices and the resolution of linear systems with these matrices.
    Attributes
    ----------
    exportable_settings : dict
        Settings of the solver that can be saved to reinit the same solver later.
    """

    def __init__(self, *, green_function=Delhommeau(), engine=BasicMatrixEngine()):
        self.green_function = green_function
        self.engine = engine

        try:
            self.exportable_settings = {
                **self.green_function.exportable_settings,
                **self.engine.exportable_settings
            }
        except AttributeError:
            pass

    @classmethod
    def from_exported_settings(settings):
        raise NotImplementedError

    def solve(self, problem, keep_details=True):
        """Solve the linear potential flow problem.
        Parameters
        ----------
        problem: LinearPotentialFlowProblem
            the problem to be solved
        keep_details: bool, optional
            if True, store the sources and the potential on the floating body in the output object
            (default: True)
        Returns
        -------
        LinearPotentialFlowResult
            an object storing the problem data and its results
        """
        LOG.info("Solve %s.", problem)

        if problem.wavelength < 8*problem.body.mesh.faces_radiuses.max():
            LOG.warning(f"Resolution of the mesh (8×max_radius={8*problem.body.mesh.faces_radiuses.max():.2e}) "
                        f"might be insufficient for this wavelength (wavelength={problem.wavelength:.2e})!")

        S, K = self.engine.build_matrices(
            problem.body.mesh, problem.body.mesh,
            problem.free_surface, problem.sea_bottom, problem.wavenumber,
            self.green_function
        )
        sources = self.engine.linear_solver(K, problem.boundary_condition)
        potential = S @ sources

        result = problem.make_results_container()
        if keep_details:
            result.sources = sources
            result.potential = potential

        for influenced_dof_name, influenced_dof_vectors in problem.influenced_dofs.items():
            # Scalar product on each face:
            influenced_dof_normal = np.sum(influenced_dof_vectors * problem.body.mesh.faces_normals, axis=1)
            # Sum over all faces:
            integrated_potential = - problem.rho * np.sum(potential * influenced_dof_normal * problem.body.mesh.faces_areas)
            # Store result:
            result.store_force(influenced_dof_name, integrated_potential)
            # Depending of the type of problem, the force will be kept as a complex-valued Froude-Krylov force
            # or stored as a couple of added mass and radiation damping coefficients.

        LOG.debug("Done!")

        return result

    def solve_all(self, problems, **kwargs):
        """Solve several problems.
        Optional keyword arguments are passed to `Nemoh.solve`.
        Parameters
        ----------
        problems: list of LinearPotentialFlowProblem
            several problems to be solved
        Returns
        -------
        list of LinearPotentialFlowResult
            the solved problems
        """
        return [self.solve(problem, **kwargs) for problem in sorted(problems)]

    def fill_dataset(self, dataset, bodies, **kwargs):
        """Solve a set of problems defined by the coordinates of an xarray dataset.
        Parameters
        ----------
        dataset : xarray Dataset
            dataset containing the problems parameters: frequency, radiating_dof, water_depth, ...
        bodies : list of FloatingBody
            the bodies involved in the problems
        Returns
        -------
        xarray Dataset
        """
        attrs = {'start_of_computation': datetime.now().isoformat(),
                 **self.exportable_settings}
        problems = problems_from_dataset(dataset, bodies)
        if 'theta' in dataset.coords:
            results = self.solve_all(problems, keep_details=True)
            kochin = kochin_data_array(results, dataset.coords['theta'])
            dataset = assemble_dataset(results, attrs=attrs, **kwargs)
            dataset.update(kochin)
        else:
            results = self.solve_all(problems, keep_details=False)
            dataset = assemble_dataset(results, attrs=attrs, **kwargs)
        return dataset

    def get_potential_on_mesh(self, result, mesh, chunk_size=50):
        """Compute the potential on a mesh for the potential field of a previously solved problem.
        Since the interaction matrix does not need to be computed in full to compute the matrix-vector product,
        only a few lines are evaluated at a time to reduce the memory cost of the operation.
        Parameters
        ----------
        result : LinearPotentialFlowResult
            the return of Nemoh's solver
        mesh : Mesh or CollectionOfMeshes
            a mesh
        chunk_size: int, optional
            Number of lines to compute in the matrix.
            (legacy, should be passed as an engine setting instead).
        Returns
        -------
        array of shape (mesh.nb_faces,)
            potential on the faces of the mesh
        Raises
        ------
        Exception: if the :code:`Result` object given as input does not contain the source distribution.
        """
        LOG.info(f"Compute potential on {mesh.name} for {result}.")

        if result.sources is None:
            raise Exception(f"""The values of the sources of {result} cannot been found.
            They probably have not been stored by the solver because the option keep_details=True have not been set.
            Please re-run the resolution with this option.""")

        if chunk_size > mesh.nb_faces:
            S = self.engine.build_S_matrix(
                mesh,
                result.body.mesh,
                result.free_surface, result.sea_bottom, result.wavenumber,
                self.green_function
            )
            phi = S @ result.sources

        else:
            phi = np.empty((mesh.nb_faces,), dtype=np.complex128)
            for i in range(0, mesh.nb_faces, chunk_size):
                S = self.engine.build_S_matrix(
                    mesh.extract_faces(list(range(i, i+chunk_size))),
                    result.body.mesh,
                    result.free_surface, result.sea_bottom, result.wavenumber,
                    self.green_function
                )
                phi[i:i+chunk_size] = S @ result.sources

        LOG.debug(f"Done computing potential on {mesh.name} for {result}.")

        return phi

    def get_free_surface_elevation(self, result, free_surface, keep_details=False):
        """Compute the elevation of the free surface on a mesh for a previously solved problem.
        Parameters
        ----------
        result : LinearPotentialFlowResult
            the return of the solver
        free_surface : FreeSurface
            a meshed free surface
        keep_details : bool, optional
            if True, keep the free surface elevation in the LinearPotentialFlowResult (default:False)
        Returns
        -------
        array of shape (free_surface.nb_faces,)
            the free surface elevation on each faces of the meshed free surface
        Raises
        ------
        Exception: if the :code:`Result` object given as input does not contain the source distribution.
        """
        fs_elevation = 1j*result.omega/result.g * self.get_potential_on_mesh(result, free_surface.mesh)
        if keep_details:
            result.fs_elevation[free_surface] = fs_elevation
        return fs_elevation

