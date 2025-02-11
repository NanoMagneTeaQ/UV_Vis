import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.interpolate import make_interp_spline
from scipy.signal import savgol_filter


material_name =  r"$ZnTe$"
material_namefile= "ZnTe"


# Load the .ods file and read the data
file_path = '<FILE PATH>'
data = pd.read_excel(file_path)

# Display the first few rows to understand its structure
data.head()

# Extract relevant columns
energy = data['energy']
alpha_hv_sq = data['alpha h nu 2']


    # Savitzky-Golay Filter (smoothing)
window_length = 801  # Length of the filter window (must be odd)
polyorder = 4      # Order of the polynomial



y_smooth = savgol_filter(alpha_hv_sq, window_length, polyorder)



# Step 1: Identify linear region manually by selecting energy range

linear_region = (energy >= 2.26) & (energy <= 2.4)
                    #2.9 to 3.4 for ZnO
                    #2.4 to 2.57 for cds
                    #2.26 to 2.4 for ZnTe
                # See from the graph 1st then set

energy_linear = energy[linear_region]
alpha_hv_sq_linear = alpha_hv_sq[linear_region]



# Step 2: Perform linear fit on the selected region
slope, intercept, r_value, p_value, std_err = linregress(energy_linear, alpha_hv_sq_linear)

# Calculate fitted line
fitted_line = slope * energy_linear + intercept

# Find the x-intercept (band gap) where y = 0 => Eg = -intercept / slope
Eg = -intercept / slope

# Step 3: Plot the Tauc plot with linear fit and Eg annotation

plt.figure(figsize=(16,9))
plt.scatter(energy, alpha_hv_sq, s=3, color='blue', label='Data Points')
plt.plot(energy, y_smooth, color='red',linestyle='solid', linewidth = 3, label='Tend of data point')

plt.plot(energy_linear, fitted_line, color='Black',linestyle = '-.', label='Linear Fit', linewidth=2)
plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.axvline(Eg, color='green', linestyle='--', label=f'Band Gap = {Eg:.3f} eV')

# Annotate the intersection point
plt.annotate(f'({Eg:.3f}, 0)',fontsize = 12, xy=(Eg, 0), xytext=(Eg - 0.3, max(alpha_hv_sq_linear) * 0.3),
             arrowprops=dict(facecolor='black', arrowstyle='->'))



# plt.title(r'$(\alpha h \nu)^2$ vs. Energy (eV) with Band Gap')
plt.title(f'Tauc Plot for Band Gap Energy for {material_name}')

plt.xlabel('Energy (eV)')
plt.ylabel(r'$(\alpha h \nu)^2\;\; (eV^2\;m^{-2})$')
plt.grid(True)
plt.legend()

# Save the plot as an image
# plt.savefig(f'<Path to save>', bbox_inches='tight', pad_inches=0.1)  
# plt.close()

plt.show()


Eg