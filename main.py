import readingsUtils.csv_reading.txtUtils as TXT
import matplotlib.pyplot as plt
import mathsUtils as MATH
from math import sqrt, pow
import graphUtils as GRAPH
import numpy as np

normalised_timestamp_acc, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros = TXT.reading_into_txt(
        "data/unsegmented/S1/Recorder_2019_04_03_16_10/data.txt")
freq = 100 # based on documentaion
smoothing_factor = 12
down_sampling_factor = freq // 30  # 100Hz to 30Hz

# PARAMETERS FOR THE REST OF THE CODE
window_size = 20  # Size of the moving window for computing mean and standard deviation
envelopp_multiplier = 3  # Multiplier for the standard deviation to determine the envelopp
threshold_multiplier = 0.4 # if too low (<0.4), detection check shows ungesture instead of gesture, if too high, gesture are too much segmented

sigma = 2

"""
For the Recorder_2019_04_03_16_10, best config is respectively 20, 3, 0.4 and 2.
For the Recorder_2019_04_03_16_23, best is 20, 3, 0.4, 2
Does not work for Recorder_2019_04_03_16_35
"""

# COMPUTATION
# Calculate the number of samples to keep
num_samples = (len(x_accel) // smoothing_factor) * smoothing_factor

# Smooth the data by taking the mean of every smoothing_factor frames
smoothed_x_accel = np.mean(np.array(x_accel[:num_samples]).reshape(-1, smoothing_factor), axis=1)
smoothed_y_accel = np.mean(np.array(y_accel[:num_samples]).reshape(-1, smoothing_factor), axis=1)
smoothed_z_accel = np.mean(np.array(z_accel[:num_samples]).reshape(-1, smoothing_factor), axis=1)

# Down-sample the smoothed data
downsampled_x_accel = smoothed_x_accel[::down_sampling_factor]
downsampled_y_accel = smoothed_y_accel[::down_sampling_factor]
downsampled_z_accel = smoothed_z_accel[::down_sampling_factor]

num_samples = (len(x_accel) // smoothing_factor) * smoothing_factor


# Same for the gyros
smoothed_x_gyros = np.mean(np.array(x_gyros[:num_samples]).reshape(-1, smoothing_factor), axis=1)
smoothed_y_gyros = np.mean(np.array(y_gyros[:num_samples]).reshape(-1, smoothing_factor), axis=1)
smoothed_z_gyros = np.mean(np.array(z_gyros[:num_samples]).reshape(-1, smoothing_factor), axis=1)

downsampled_x_gyros = smoothed_x_gyros[::down_sampling_factor]
downsampled_y_gyros = smoothed_y_gyros[::down_sampling_factor]
downsampled_z_gyros = smoothed_z_gyros[::down_sampling_factor]


# Calculate the corresponding timestamp for the downsampled data
original_timestamp = np.linspace(0, num_samples / freq, num_samples)
downsampled_timestamp = original_timestamp[::smoothing_factor][::down_sampling_factor]

# Normalise the acceleration data
norm = []
for i in range(0, len(downsampled_x_accel)):
        norm.append(sqrt(pow(downsampled_x_accel[i], 2) + pow(downsampled_y_accel[i], 2) + pow(downsampled_z_accel[i], 2)))

norm_derivative, norm_gaussian, abs_norm, envelopp_norm, start_norm, end_norm = MATH.simple_segmentation(
        downsampled_timestamp, norm, sigma, window_size, envelopp_multiplier, threshold_multiplier)
GRAPH.plot_simple_segmentation(downsampled_timestamp, norm, norm_derivative, norm_gaussian, abs_norm, envelopp_norm, start_norm, end_norm)
xaccel_derivative, xaccel_gaussian, abs_xaccel, envelopp_xaccel, start_xaccel, end_xaccel = MATH.simple_segmentation(
        downsampled_timestamp, downsampled_x_accel, sigma, window_size, envelopp_multiplier, threshold_multiplier)
yaccel_derivative, yaccel_gaussian, abs_yaccel, envelopp_yaccel, start_yaccel, end_yaccel = MATH.simple_segmentation(
        downsampled_timestamp, downsampled_y_accel, sigma, window_size, envelopp_multiplier, threshold_multiplier)
zaccel_derivative, zaccel_gaussian, abs_zaccel, envelopp_zaccel, start_zaccel, end_zaccel = MATH.simple_segmentation(
        downsampled_timestamp, downsampled_z_accel, sigma, window_size, envelopp_multiplier, threshold_multiplier)

GRAPH.plots_data(downsampled_timestamp, 
                   "Derivative",
                   (xaccel_derivative, "xaccel_derivative"), 
                   (yaccel_derivative, "yaccel_derivative"), 
                   (zaccel_derivative, "zaccel_derivative"), 
                   (norm_derivative, "norm_derivative"))

GRAPH.plots_data(downsampled_timestamp, 
                 "Gaussian filtered",
                 (xaccel_gaussian, "x_accel"),
                 (yaccel_gaussian, "y_accel"),
                 (zaccel_gaussian, "z_accel"),
                 (norm_gaussian, "norm"))

plt.figure()
plt.subplot(4,1,1)
plt.plot(abs_xaccel, label="x_accel")
plt.plot(envelopp_xaccel, label="envelopp")
plt.legend()
plt.subplot(4,1,2)
plt.plot(abs_yaccel, label="y_accel")
plt.plot(envelopp_yaccel, label="envelopp")
plt.legend()
plt.subplot(4,1,3)
plt.plot(abs_zaccel, label="z_accel")
plt.plot(envelopp_zaccel, label="envelopp")
plt.legend()
plt.subplot(4,1,4)
plt.plot(abs_norm, label="norm_accel")
plt.plot(envelopp_norm, label="envelopp")
plt.suptitle("Adaptative envelopp")
plt.legend()
plt.show()

