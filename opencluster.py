import pandas as pd
import matplotlib.pyplot as plt
input_csv = "M67_gaia_dr3.csv"
gaia_csv = pd.read_csv(input_csv)

#print(list(gaia_csv.columns))
gaia_csv.plot(kind='scatter',x='bp_rp',y='phot_g_mean_mag',marker="." \
        , xlim=[0,3], ylim = [22, 6] \
        , xticks=[0,0.5,1.,1.5,2.,2.5,3] \
        , yticks=[22,20,18,16,14,12,10,8,6])

plt.show()
