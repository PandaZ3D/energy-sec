import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

'''
skymote powered at 3 V
# power
Current Consumption: MCU on, Radio RX 21.8 mA
Current Consumption: MCU on, Radio TX 19.5 mA
Current Consumption: MCU on, Radio off 1.800 mA
# microprocessor
Active current at Vcc = 3V, 1MHz 500 μA
Sllep current in LPM0 Vcc = 3v, 225 μA
Sleep current in LPM3 Vcc = 3V, 32.768kHz active 2.6 μA
'''

# operating 3 V
voltage = 3.0
# radio tx current
radio_tx = 21.8e-3
# radio rx current
radio_rx = 19.5e-3
# radio off current
radio_off = 1.8e-3
# cpu active current
cpu_active = 500e-6
# cpu LPM
cpu_lpm = 225e-6
# cpu deep LM
cpu_dlmp = 2.6e-6
# energest ticks per second
energest_seconds = 32768
# run time (6 seconds)
interval = 6.0

num_nodes = 3
num_sim = 10
#test-$TEST-$counter.csv

def calculate_energy(df, col, part):
	return (df[col] * part * voltage) / (energest_seconds)

# open data file
data = pd.read_csv("example-data-2.csv", 
	usecols=['node','interval','cpu','lpm','dlpm','rx','tx','idle'],
	skiprows=1,
	skipfooter=2,
	engine='python'
)

# average amount of energy consumed of the network
#	calculate energy consumption of network for each run
#	save that value for each run
#	find mean, std-dev of new metric
# average amount of energy consumed per component
#	calculate the amount of energy consumed per component for each node
#	save value for each run
#	average over number of nodes * number of sim
# average time each component was in use %
#	get the amount of time (seconds) each component was used
#	save value for each run
#	average over number of runs
# total energy consumption of network over time
#	calculate energy consumed for each mote at each time
# 	save values for each  simulation
#	average values for each time

# new csv: simulation, total energy 
# total energy of the network
total_energy = 0
# grab all values of a particular node
node_data = data.loc[data['node'] == 2]

# time axis
time = np.arange(0,len(node_data.index)*6,6)

# calculate cpu energy cost: (in uJ)
e_cpu_active = calculate_energy(node_data, 'cpu', cpu_active) #(node_data['cpu'] * cpu_active * voltage) / (energest_seconds)
e_cpu_lpm = calculate_energy(node_data, 'lpm', cpu_lpm)
e_cpu_dlpm = calculate_energy(node_data, 'dlpm', cpu_dlmp)
# calculate radio energy cost (in mJ)
e_rx = calculate_energy(node_data, 'rx', radio_rx)
e_tx = calculate_energy(node_data, 'tx', radio_rx)
e_idle = calculate_energy(node_data, 'idle', radio_off)
# total energy per node (in mJ)
total_energy += e_cpu_active + e_cpu_lpm + e_cpu_dlpm + e_rx + e_tx + e_idle
total_energy *= 1000
# total_energy = total_energy.expanding(1).sum() 

# a simple line plot
plt.plot(time, total_energy)
plt.ylabel('Instantanious Energy Consumption (mJ)')
plt.xlabel('Time (s)')
plt.title('Instantanious Energy Consumption of the Network')
#ax = plt.gca()
#ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2e'))
#ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.3e'))

plt.show()
#plt.savefig('cpu_active.png')