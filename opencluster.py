import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
input_csv  = "M67_gaia_dr3.csv"
output_cmd = "M67_gaia_dr3_cmd.png"
output_astrometry ="M67_gaia_dr3_mem.png" 

cl = pd.read_csv(input_csv)
#print(list(cl.columns))

plt.rcParams['figure.figsize'] = [20, 20]

# Draw Color-Magnitude Diagram
plt.subplot(3,3,7)
plt.scatter(cl.bp_rp, # X
        cl.phot_g_mean_mag, #Y
        marker = 's', # point type
        s = 0.1, # point size
        c = cl.bp_rp, # color = bp_rp
        vmin = 0, vmax = 2, # set color bar as X axis color
        cmap = 'jet') 
plt.xlim(0,3) # X axis range 
plt.ylim(22,6) # Y axis range
plt.xlabel('Bp - Rp') 
plt.ylabel('G mag')
plt.colorbar() 

# Draw Proper Motion diagram
cl['pm_error'] = (cl['pmra_error']**2 + cl['pmdec_error']**2)**0.5 # Add Proper motion error column
plt.subplot(3,3,8)
plt.scatter(cl.pmra,
        cl.pmdec,
        marker='s',
        s = 0.1,
        c = cl.pm_error,
        cmap='summer')
plt.xlim(-20,10)
plt.ylim(-20,10)
plt.xlabel('Proper Motion in R.A.')
plt.ylabel('Proper Motion in Dec.')
plt.colorbar()

# Draw R.A. Proper Motion - Distance diagram
cl['distance'] = 1000/cl['parallax'] # Add Distance (in pc) column
plt.subplot(3,3,2) 
plt.scatter(cl.pmra,
        cl.distance,
        marker='s',
        s = 0.1,
        c = cl.parallax_error,
        cmap='winter')
plt.xlim(-20,10)
plt.ylim(0,2000)
plt.colorbar()

# Draw Dec. Proper Motion - Distance diagram
plt.subplot(3,3,3)
plt.scatter(cl.pmdec,
        cl.distance,
        marker='s',
        s = 0.1,
        c = cl.parallax_error,
        cmap='hot')
plt.xlim(-20,10)
plt.ylim(0,2000)
plt.colorbar()

# Draw R.A. Proper Motion - Radial Velocity diagram
plt.subplot(3,3,5)
plt.scatter(cl.pmra,
        cl.radial_velocity,
        marker='s',
        s = 0.1,
        c = cl.radial_velocity_error,
        cmap='winter')
plt.xlim(-20,10)
plt.ylim(0,50)
plt.colorbar()

# Draw Dec. Proper Motion - Radial Velocity diagram
plt.subplot(3,3,6)
plt.scatter(cl.pmdec,
        cl.radial_velocity,
        marker='s',
        s = 0.1,
        c = cl.radial_velocity_error,
        cmap='hot')
plt.xlim(-20,10)
plt.ylim(0,50)
plt.xlabel('Proper Motion in Dec.')
plt.colorbar()

# Draw Distance - Radial Velocity diagram
plt.subplot(3,3,4)
plt.scatter(cl.distance,
        cl.radial_velocity,
        marker='s',
        s = 0.1,
        c = cl.radial_velocity_error,
        cmap='spring')
plt.xlim(0,2000)
plt.ylim(0,50)
plt.xlabel('Distance (pc)')
plt.ylabel('Radial Velocity')
plt.colorbar()

# Draw R.A. Radial Velocity - Distance Diagram
plt.subplot(3,3,1)
plt.scatter(cl.radial_velocity,
        cl.distance,
        marker='s',
        s = 0.1,
        c = cl.parallax_error,
        cmap='winter')
plt.xlim(0,50)
plt.ylim(0,2000)
plt.ylabel('Distance (pc)')
plt.xlabel('Radial Velocity')
plt.colorbar()

# Draw Spatial Potioin map(R.A. - Dec. map)
cl['mag_scale'] = (14-cl['phot_g_mean_mag'])*25
cl.loc[cl['mag_scale'] > 100, 'mag_scale']=100
cl.loc[cl['mag_scale'] < 0.01, 'mag_scale']=0.01
cl.loc[cl['phot_g_mean_mag'] < 10, 'mag_scale']=100
#print(cl[['phot_g_mean_mag','mag_scale']])
plt.subplot(3,3,9)
plt.scatter(cl.ra,
        cl.dec,
        s = cl.mag_scale,
        c = cl.bp_rp,
        vmin = 0,
        vmax = 2,
        cmap='jet')
plt.ylabel('R.A.')
plt.xlabel('Dec.')
plt.colorbar()

# Save gifure as a file
plt.savefig(output_cmd)
