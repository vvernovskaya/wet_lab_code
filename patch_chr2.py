import pyabf
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
from scipy.optimize import curve_fit

FIT_F_START = 0
FIT_F_FINISH = 1000
TAU_OFF = 2 * 10 ** (-4)  # seconds
START_TIME_AVG = 0.75
FINISH_TIME_AVG = 1.5


def lorentzian(x, f_c, x_0):
    return S_0 / (1 + (x - x_0 / f_c) ** 2)


# Data extraction
abf_sweeps = pyabf.ABF("patch_05_08_2021/21805018.abf")  # sweeps
abf_on = pyabf.ABF("patch_05_08_2021/21805019.abf")  # light on
abf_off = pyabf.ABF("patch_05_08_2021/21805020.abf")  # light off

abf_on.setSweep(0)
abf_off.setSweep(0)
y_on = abf_on.sweepY
y_off = abf_off.sweepY
y_delta = y_on - y_off
time = abf_on.sweepX
fs = 10e2

# Making PSD
f_on, psd_on = signal.welch(y_on, fs, 'flattop', 40000, scaling='density')
f_off, psd_off = signal.welch(y_off, fs, 'flattop', 40000, scaling='density')
f_d, psd_d = signal.welch(y_delta, fs, 'flattop', 40000, scaling='density')

S_0 = psd_d[min(range(len(f_d)), key=lambda k: abs(f_d[k]-FIT_F_START))]

# Preparing delta psd data for fitting
f_d_sparse = []
psd_d_sparse = []
for i in range(len(f_d)):
    if i % 2 == 0 and FIT_F_START < f_d[i] < FIT_F_FINISH:
        f_d_sparse.append(f_d[i])
        psd_d_sparse.append(psd_d[i])

# Curve fitting
params, cov = curve_fit(lorentzian, f_d_sparse, psd_d_sparse)

# Making plots for PSDs
fig_psd, ax_psd = plt.subplots()
fig_delta, ax_delta = plt.subplots()

ax_psd.plot(f_on, psd_on)
ax_psd.plot(f_off, psd_off)
ax_psd.set_title('PSDs for light on and light off')
ax_psd.set_yscale('log')
ax_psd.set_xscale('log')
ax_psd.set_xlabel('Frequency , Hz')
ax_psd.set_ylabel('PSD')

f = np.linspace(FIT_F_START, FIT_F_FINISH, 1000)
f_c_fit = params[0]
f_0_fit = params[1]

ax_delta.plot(f_d, psd_d)
ax_delta.plot(f, lorentzian(f, f_c_fit, f_0_fit))
ax_delta.set_title('PSD (on - off)')
ax_delta.set_yscale('log')
ax_delta.set_xscale('log')
ax_delta.set_xlabel('Frequency, Hz')
ax_delta.set_ylabel('Delta PSD')

# Calculating necessary values
sigma_2 = np.pi * f_c_fit * S_0 / 2  # variance
p_c = 1 / (2 * np.pi * f_c_fit * TAU_OFF)  # probability of closed state (p_c = 1 - p_o)

# Plotting sweeps, extracting currents from sweeps, plotting VAC
# and calculating single channel currents
fig_s, ax_s = plt.subplots()
fig_vac, ax_vac = plt.subplots(1, 2)

ax_s.set_title('Sweeps')
ax_s.set_xlabel('Time, s')
ax_s.set_ylabel('Current, pA')

ax_vac[0].set_title('VAC for whole cell')
ax_vac[0].set_xlabel('Voltage, mV')
ax_vac[0].set_ylabel('Current, pA')

ax_vac[1].set_title('VAC for single channel')
ax_vac[1].set_xlabel('Voltage, mV')
ax_vac[1].set_ylabel('Current, pA')

i_cell = []  # whole cell currents
i_single = []  # single channel currents
u_raw = []  # voltages
start_index_avg = int(START_TIME_AVG * abf_sweeps.dataPointsPerMs)
finish_index_avg = int(FINISH_TIME_AVG * abf_sweeps.dataPointsPerMs)

for sweep in abf_sweeps.sweepList:
    abf_sweeps.setSweep(sweep)
    ax_s.plot(abf_sweeps.sweepX, abf_sweeps.sweepY)
    i_cell.append(np.average(abf_sweeps.sweepY[start_index_avg:finish_index_avg]))
    i_single.append(sigma_2 / i_cell[len(i_cell)-1] / p_c)
    u_raw.append(abf_sweeps.sweepEpochs.levels[2])

ax_vac[0].plot(u_raw, i_cell, '.-')
ax_vac[1].plot(u_raw, i_single, '.-')

plt.show()
