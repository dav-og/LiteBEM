import matplotlib.pyplot as plt
import numpy as np
import litebem.preprocessing.mesh as lpm

hemi360Mesh = f'tests/unit/preprocessorRefData/hemisphere360.nemoh'
meshHeader, meshVerts, meshFaces = lpm.read_nemoh_mesh(hemi360Mesh)
mesh = lpm.Mesh(meshVerts,meshFaces,name=f'hemi360')

hemi360Areas = f'tests/unit/preprocessorRefData/hemisphere360PanelAreas.txt'
hemi360Centers = f'tests/unit/preprocessorRefData/hemisphere360PanelCenters.txt'
hemi360Normals = f'tests/unit/preprocessorRefData/hemisphere360PanelNormals.txt'
hemi360Radii = f'tests/unit/preprocessorRefData/hemisphere360PanelRadii.txt'

addedMass = f'tests/unit/solverRefData/addedMass.txt'
addedMassCap = f'tests/unit/solverRefData/addedMassCap.txt'
radiationDamping = f'tests/unit/solverRefData/RadiationDamping.txt'
radiationDampingCap = f'tests/unit/solverRefData/RadiationDampingCap.txt'

AMvaluesCap = open(addedMassCap)
AMvalues = open(addedMass)
RDvaluesCap = open(radiationDampingCap)
RDvalues = open(radiationDamping)
Avalues = open(hemi360Areas)
Rvalues = open(hemi360Radii)
RDvaluesCapList = []
RDvaluesList = []
AMvaluesCapList = []
AMvaluesList = []
AvaluesList = []
RvaluesList = []

for line in AMvaluesCap:
    line = line.rstrip()
    numbers = float(line)
    AMvaluesCapList.append(numbers)

for line in AMvalues:
    line = line.rstrip()
    numbers = float(line)
    AMvaluesList.append(numbers)

for line in RDvaluesCap:
    line = line.rstrip()
    numbers = float(line)
    RDvaluesCapList.append(numbers)

for line in RDvalues:
    line = line.rstrip()
    numbers = float(line)
    RDvaluesList.append(numbers)
    
for line in Avalues:
    line = line.rstrip()
    numbers = float(line)
    AvaluesList.append(numbers)

for line in Rvalues:
    line = line.rstrip()
    numbers = float(line)
    RvaluesList.append(numbers)

omega = np.linspace(0.1,4,40)

plt.rcParams["figure.figsize"] = (7,3)
plt.figure(1)
plt.plot(omega,AMvaluesCapList,'-k',label='Capytaine',linewidth=3.0)
plt.plot(omega,AMvaluesList,'--c',label='LiteBEM',linewidth=2.0)
plt.xlabel('Wave Frequency (rad/s)')
plt.ylabel('Added Mass (kg)')
plt.legend()

plt.figure(2)
plt.plot(omega,RDvaluesCapList,'-k',label='Capytaine',linewidth=3.0)
plt.plot(omega,RDvaluesList,'--c',label='LiteBEM',linewidth=2.0)
plt.xlabel('Wave Frequency (rad/s)')
plt.ylabel('Radiation Damping (Nm/s)')
plt.legend()

plt.figure(3)
plt.plot(range(mesh.nPanels//2),AvaluesList[0:180],'-k',label='Capytaine',linewidth=3.0)
plt.plot(range(mesh.nPanels//2),mesh.panelAreas[0:180],'--c',label='LiteBEM',linewidth=2.0)
plt.xlabel('Panel ID')
plt.ylabel('Area (m^2)')
plt.legend()

plt.figure(4)
plt.plot(range(mesh.nPanels//2),RvaluesList[0:180],'-k',label='Capytaine',linewidth=3.0)
plt.plot(range(mesh.nPanels//2),mesh.panelRadii[0:180],'--c',label='LiteBEM',linewidth=2.0)
plt.xlabel('Panel ID')
plt.ylabel('Radii (m)')
plt.legend()

plt.show()