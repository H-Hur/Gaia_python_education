import pandas as pd
import matplotlib.pyplot as plt
#import opencluster_draw as od
import math
import numpy as np
#import seaborn as sns
#input_csv  = "M67_gaia_dr3.csv"
#output_cmd = "M67_gaia_dr3_cmd.png"
#output_astrometry ="M67_gaia_dr3_mem.png" 
input_csv  = "M67_gaia_dr3.csv"
output_cmd = "M67_gaia_dr3.png"
output_astrometry ="M67_mem.png" 

cl = pd.read_csv(input_csv)
#print(list(cl.columns))


# pmra_error < 0.03
con1 = (cl['pmra_error'] < 0.5)
# pmdec_error < 0.03 
con2 = (cl['pmdec_error'] < 0.5)
# ruwe <= 1.4 
con3 = (cl['ruwe'] <= 1.4)
# parallax_error < 0.03  & parallax / parallax_error > 5
con4_1 = (cl['parallax_error'] < 0.3)
con4_2 = (cl['parallax']/cl['parallax_error'] > 5)

cl_filt = cl[con1 & con2 & con3 & con4_1 & con4_2]

cl.isnull().sum()

plt.rcParams['figure.figsize'] = [20, 20]
# Draw Color-Magnitude Diagram
plt.subplot(3,3,7)
plt.scatter(cl_filt.bp_rp, # X
        cl_filt.phot_g_mean_mag, #Y
        marker = 's', # point type
        s = 0.1, # point size
        c = cl_filt.bp_rp, # color = bp_rp
        vmin = 0, vmax = 2, # set color bar as X axis color
        cmap = 'jet')
plt.xlim(0,3) # X axis range 
plt.ylim(22,6) # Y axis range
plt.xlabel('Bp - Rp')
plt.ylabel('G mag')
plt.colorbar()

# Draw Proper Motion diagram
cl_filt['pm_error'] = (cl_filt['pmra_error']**2 + cl_filt['pmdec_error']**2)**0.5 # Add Proper motion error column
plt.subplot(3,3,8)
plt.scatter(cl_filt.pmra,
        cl_filt.pmdec,
        marker='s',
        s = 0.1,
        c = cl_filt.pm_error,
        cmap='summer')
plt.xlim(-20,10)
plt.ylim(-20,10)
plt.xlabel('Proper Motion in R.A.')
plt.ylabel('Proper Motion in Dec.')
plt.colorbar()

# Draw R.A. Proper Motion - Distance diagram
cl_filt['distance'] = 1000/cl_filt['parallax'] # Add Distance (in pc) column
plt.subplot(3,3,2)
plt.scatter(cl_filt.pmra,
        cl_filt.distance,
        marker='s',
        s = 0.1,
        c = cl_filt.parallax_error,
        cmap='winter')
plt.xlim(-20,10)
plt.ylim(0,2000)
plt.colorbar()

# Draw Dec. Proper Motion - Distance diagram
plt.subplot(3,3,3)
plt.scatter(cl_filt.pmdec,
        cl_filt.distance,
        marker='s',
        s = 0.1,
        c = cl_filt.parallax_error,
        cmap='hot')
plt.xlim(-20,10)
plt.ylim(0,2000)
plt.colorbar()

# Draw R.A. Proper Motion - Radial Velocity diagram
plt.subplot(3,3,5)
plt.scatter(cl_filt.pmra,
        cl_filt.radial_velocity,
        marker='s',
        s = 0.1,
        c = cl_filt.radial_velocity_error,
        cmap='winter')
plt.xlim(-20,10)
plt.ylim(0,50)
plt.colorbar()

# Draw Dec. Proper Motion - Radial Velocity diagram
plt.subplot(3,3,6)
plt.scatter(cl_filt.pmdec,
        cl_filt.radial_velocity,
        marker='s',
        s = 0.1,
        c = cl_filt.radial_velocity_error,
        cmap='hot')
plt.xlim(-20,10)
plt.ylim(0,50)
plt.xlabel('Proper Motion in Dec.')
plt.colorbar()

# Draw Radial Velocity - Parallax - diagram
plt.subplot(3,3,4)
plt.scatter(cl_filt.radial_velocity,
        cl_filt.parallax,
        marker='s',
        s = 0.1,
        c = cl_filt.radial_velocity_error,
        cmap='spring')
plt.xlim(0,50)
plt.ylim(0.5,1.5)
plt.xlabel('Radial Velocity')
plt.ylabel('Parallax (mas)')
plt.colorbar()

# Draw R.A. Radial Velocity - Distance Diagram
plt.subplot(3,3,1)
plt.scatter(cl_filt.radial_velocity,
        cl_filt.distance,
        marker='s',
        s = 0.1,
        c = cl_filt.parallax_error,
        cmap='winter')
plt.xlim(0,50)
plt.ylim(0,2000)
plt.ylabel('Distance (pc)')
plt.xlabel('Radial Velocity')
plt.colorbar()

# Draw Spatial Potioin map(R.A. - Dec. map)
cl_filt['mag_scale'] = (14-cl_filt['phot_g_mean_mag'])*25
cl_filt.loc[cl_filt['mag_scale'] > 100, 'mag_scale']=100
cl_filt.loc[cl_filt['mag_scale'] < 0.01, 'mag_scale']=0.01
cl_filt.loc[cl_filt['phot_g_mean_mag'] < 10, 'mag_scale']=100
#print(cl_filt[['phot_g_mean_mag','mag_scale']])
plt.subplot(3,3,9)
plt.scatter(cl_filt.ra,
        cl_filt.dec,
        s = cl_filt.mag_scale,
        c = cl_filt.bp_rp,
        vmin = 0,
        vmax = 2,
        cmap='jet')
plt.ylabel('R.A.')
plt.xlabel('Dec.')
plt.colorbar()


plt.savefig(output_cmd)

