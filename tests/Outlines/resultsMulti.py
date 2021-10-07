import matplotlib.pyplot as plt
import numpy as np

addedMass = f'tests/unit/solverRefData/multiAddedMassLite300.txt'
addedMassCap = f'tests/unit/solverRefData/multiAddedMassCap300.txt'
addedMassLiteCouple = f'tests/unit/solverRefData/multiAddedMassLiteCouple.txt'
addedMassCapCouple = f'tests/unit/solverRefData/multiAddedMassCapCouple.txt'
radiationDamping = f'tests/unit/solverRefData/multiRadiationDampingLite.txt'
RadiationDampingCap = f'tests/unit/solverRefData/multiRadiationDamping.txt'


AMvaluesCap = open(addedMassCap)
AMvalues = open(addedMass)
AMvaluesCapCouple = open(addedMassCapCouple)
AMvaluesLiteCouple = open(addedMassLiteCouple)
RDvaluesCap = open(RadiationDampingCap)
RDvalues = open(radiationDamping)
AMvaluesCapList = []
AMvaluesList = []
AMvaluesCapCoupleList = []
AMvaluesLiteCoupleList = []
RDvaluesCapList = []
RDvaluesList = []

for line in AMvaluesCap:
    line = line.rstrip()
    numbers = float(line)
    AMvaluesCapList.append(numbers)

for line in AMvalues:
    line = line.rstrip()
    numbers = float(line)
    AMvaluesList.append(numbers)

for line in AMvaluesCapCouple:
    line = line.rstrip()
    numbers = float(line)
    AMvaluesCapCoupleList.append(numbers)

for line in AMvaluesLiteCouple:
    line = line.rstrip()
    numbers = float(line)
    AMvaluesLiteCoupleList.append(numbers)

for line in RDvaluesCap:
    line = line.rstrip()
    numbers = float(line)
    RDvaluesCapList.append(numbers)

for line in RDvalues:
    line = line.rstrip()
    numbers = float(line)
    RDvaluesList.append(numbers)

omega = np.linspace(0.1,10,300)
omega2 = np.linspace(0.1,10,150)

# plt.rcParams["figure.figsize"] = (7,3)
plt.figure(1)
plt.plot(omega,AMvaluesCapList,'-k',label='Capytaine',linewidth=3.0)
plt.plot(omega,AMvaluesList,'--c',label='LiteBEM',linewidth=2.0)
plt.xlabel('Wave Frequency (rad/s)')
plt.ylabel('Added Mass (kg)')
plt.legend()

plt.figure(2)
plt.plot(omega2,AMvaluesCapCoupleList,'-k',label='Capytaine',linewidth=3.0)
plt.plot(omega2,AMvaluesLiteCoupleList,'--c',label='LiteBEM',linewidth=2.0)
plt.xlabel('Wave Frequency (rad/s)')
plt.ylabel('Added Mass (kg)')
plt.legend()

plt.figure(3)
plt.plot(omega2,RDvaluesCapList,'-k',label='Capytaine',linewidth=3.0)
plt.plot(omega2,RDvaluesList,'--c',label='LiteBEM',linewidth=2.0)
plt.xlabel('Wave Frequency (rad/s)')
plt.ylabel('Radiation Damping (Nm/s)')
plt.legend()

plt.show()