import numpy as np
from litebem.preprocessing.airy_waves import airy_waves_potential

import logging
from datetime import datetime
from typing import Sequence, List, Union

import pandas as pd
import xarray as xr

LOG = logging.getLogger(__name__)

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
    pressure = -1j * pb.omega * pb.rho * airy_waves_potential(pb.body.mesh.panelCenters, pb, convention=convention)
    forces = {}
    for dof in pb.influenced_dofs:
        # Scalar product on each face:
        normal_dof_amplitude_on_face = np.sum(pb.body.dofs[dof] * pb.body.mesh.panelUnitNormals, axis=1)
        # Sum over all faces:
        forces[dof] = np.sum(pressure * normal_dof_amplitude_on_face * pb.body.mesh.panelAreas)
    return forces

######################
#  Dataset creation  #
######################

def _dataset_from_dataframe(df: pd.DataFrame,
                            variables: Union[str, Sequence[str]],
                            dimensions: Sequence[str],
                            optional_dims: Sequence[str],
                            ) -> Union[xr.DataArray, xr.Dataset]:
    """Transform a pandas.Dataframe into a xarray.Dataset.

    Parameters
    ----------
    df: pandas.DataFrame
        the input dataframe
    variables: string or sequence of strings
        the variables that will be stored in the output dataset.
        If a single name is provided, a DataArray of this variable will be provided instead.
    dimensions: sequence of strings
        Names of dimensions the variables depends on.
        They will always appear as dimension in the output dataset.
    optional_dims: sequence of strings
        Names of dimensions the variables depends on.
        They will appears as dimension in the output dataset only if they have
        more than one different values.
    """
    for variable_name in variables:
        df = df[df[variable_name].notnull()].dropna(axis='columns')  # Keep only records with non null values of all the variables
    df = df.drop_duplicates()
    df = df.set_index(optional_dims + dimensions)

    da = df.to_xarray()[variables]
    da = _squeeze_dimensions(da, dimensions=optional_dims)
    return da

def _squeeze_dimensions(data_array, dimensions=None):
    """Remove dimensions if they are of size 1. The coordinates become scalar coordinates."""
    if dimensions is None:
        dimensions = data_array.dims
    for dim in dimensions:
        if len(data_array[dim]) == 1:
            data_array = data_array.squeeze(dim, drop=False)
    return data_array

def collect_records(results):
    records_list = []
    #TODO add in warning about only supporting cases with a free surface
    for result in results:
        for record in result.records:
                records_list.append(record)
    return records_list

def assemble_dataset(results: Sequence[LinearPotentialFlowResult],
                     wavenumber=False, wavelength=False, mesh=False, hydrostatics=False,
                     attrs=None) -> xr.Dataset:
    """Transform a list of :class:`LinearPotentialFlowResult` into a :class:`xarray.Dataset`.

    .. todo:: The :code:`mesh` option to store informations on the mesh could be improved.
              It could store the full mesh in the dataset to ensure the reproducibility of
              the results.

    Parameters
    ----------
    results: list of LinearPotentialFlowResult
        The results that will be read.
    wavenumber: bool, optional
        If True, the coordinate 'wavenumber' will be added to the ouput dataset.
    wavelength: bool, optional
        If True, the coordinate 'wavelength' will be added to the ouput dataset.
    mesh: bool, optional
        If True, store some infos on the mesh in the output dataset.
    hydrostatics: bool, optional
        If True, store the hydrostatic data in the output dataset if they exist.
    attrs: dict, optional
        Attributes that should be added to the output dataset.
    """
    dataset = xr.Dataset()

    error_msg = 'results must be either of type LinearPotentialFlowResult or a bemio.io object'
    if hasattr(results, '__iter__'):
        try:
            if 'litebem' in results[0].__module__:
                bemio_import = False
            else:
                raise TypeError(error_msg)
        except:
            raise TypeError(error_msg)

    else:
        try:
            if 'bemio.io' in results.__module__:
                bemio_import = True
            else:
                raise TypeError(error_msg)
        except:
            raise TypeError(error_msg)

    if bemio_import:
        #TODO add compatibility with bemio.io objects
        raise TypeError('bemio.io objects are not compatible with litebem')

    else:
        records = pd.DataFrame(collect_records(results))
        all_dofs_in_order = {k: None for r in results for k in r.body.dofs.keys()}

    if attrs is None:
        attrs = {}
    attrs['creation_of_dataset'] = datetime.now().isoformat()
    if len(records) == 0:
        raise ValueError("No result passed to assemble_dataset.")

    inf_dof_cat = pd.CategoricalDtype(categories=all_dofs_in_order.keys())
    records["influenced_dof"] = records["influenced_dof"].astype(inf_dof_cat)
    rad_dof_cat = pd.CategoricalDtype(categories=all_dofs_in_order.keys())
    if 'added_mass' in records.columns:
        records["radiating_dof"] = records["radiating_dof"].astype(rad_dof_cat)

    optional_dims = ['g', 'rho', 'body_name', 'water_depth']

    # RADIATION RESULTS
    if 'added_mass' in records.columns:
        radiation_cases = _dataset_from_dataframe(
            records,
            variables=['added_mass', 'radiation_damping'],
            dimensions=['omega', 'radiating_dof', 'influenced_dof'],
            optional_dims=optional_dims)
        dataset = xr.merge([dataset, radiation_cases])

    # DIFFRACTION RESULTS
    if 'diffraction_force' in records.columns:
        conventions = set(records['convention'].dropna())
        if len(conventions) > 1:
            LOG.warning("Assembling a dataset mixing several conventions.")
        else:
            attrs['incoming_waves_convention'] = conventions.pop()

        diffraction_cases = _dataset_from_dataframe(
            records,
            variables=['diffraction_force', 'Froude_Krylov_force'],
            dimensions=['omega', 'wave_direction', 'influenced_dof'],
            optional_dims=optional_dims)
        dataset = xr.merge([dataset, diffraction_cases])

    #TODO add in functionality for reporting wavenumber, wavelength, and hydrostatics

    dataset.attrs.update(attrs)
    return dataset

################################
#  Handling of complex values  #
################################

def separate_complex_values(ds: xr.Dataset) -> xr.Dataset:
    """Return a new Dataset where complex-valued arrays of shape (...)
    have been replaced by real-valued arrays of shape (2, ...).

    .. seealso::
        :func:`merge_complex_values`
            The invert operation
    """
    ds = ds.copy()
    for variable in ds.data_vars:
        if ds[variable].dtype == complex:
            da = ds[variable]
            new_da = xr.DataArray(np.asarray((np.real(da).data, np.imag(da).data)),
                                  dims=('complex',) + da.dims)
            ds[variable] = new_da
            ds.coords['complex'] = ['re', 'im']
    return ds


def merge_complex_values(ds: xr.Dataset) -> xr.Dataset:
    """Return a new Dataset where real-valued arrays of shape (2, ...)
    have been replaced by complex-valued arrays of shape (...).

    .. seealso::
        :func:`separate_complex_values`
            The invert operation
    """
    if 'complex' in ds.coords:
        ds = ds.copy()
        for variable in ds.data_vars:
            if 'complex' in ds[variable].coords:
                da = ds[variable]
                new_dims = [d for d in da.dims if d != 'complex']
                new_da = xr.DataArray(da.sel(complex='re').data + 1j*da.sel(complex='im').data, dims=new_dims)
                ds[variable] = new_da
        ds = ds.drop_vars('complex')
    return ds