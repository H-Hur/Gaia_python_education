#import opencluster_draw as od
import matplotlib.pyplot as plt
import pandas as pd
input_csv  = "NGC2362.csv" # 자료 다운로드 받은 파일 이름
output_group ="N2362_mem.png" # 분류 결과 확인할 그림파일 이름

cl = pd.read_csv(input_csv)

# 사용할 자료의 오차 조건 설정--------------------------------------------------
# 적경 고유운동 오차 조거 pmra_error < 0.03
con1 = (cl['pmra_error'] < 0.5)
# 적위 고유운동 오차 조건 pmdec_error < 0.03 
con2 = (cl['pmdec_error'] < 0.5)
# ruwe <= 1.4 
con3 = (cl['ruwe'] <= 1.4)
# 연주시차 오차 조건 parallax_error < 0.03  & parallax / parallax_error > 5
con4_1 = (cl['parallax_error'] < 0.3)
con4_2 = (cl['parallax']/cl['parallax_error'] > 5)

# 오차조건 적용하여 Pandas 배열 추출
cl_filt = cl[con1 & con2 & con3 & con4_1 & con4_2]
# 실제로 사용할 열만 따로 추출
cl_filt2 = cl_filt[['pmra','pmdec','pmra_error','pmdec_error' \
    ,'ruwe','parallax','parallax_error','radial_velocity' \
    ,'radial_velocity_error','phot_g_mean_mag' \
    ,'ra','dec','bp_rp','solution_id','source_id']]
print(cl_filt2.isnull().sum())


# 가우시안 믹스쳐 모델(GMM) 적용 ----------------------------------------
# 가우시안 분포 적용할 모델 import
from sklearn.mixture import GaussianMixture

# GMM 모델에 사용할 열 고르기: 적경 고유운동, 적위 고유운동, 연주시차
cl_filt3 = cl_filt2[['pmra','pmdec','parallax']]
#print(cl_filt3)
# GMM: n_components = 모델의 총 수
# n_comppnents: 별을 몇 개 그룹으로 분류할 것인디
gmm = GaussianMixture(n_components=4, random_state=0)
gmm.fit(cl_filt3)
labels = gmm.predict(cl_filt3)
cl_filt3["group"] = labels
#print(len(cl_filt3.loc[cl_filt3['group'] == 0]))
#print(len(cl_filt3.loc[cl_filt3['group'] == 1]))
h = cl_filt3.hist(figsize=(20,12))
plt.savefig('histogram.png')


#print(cl_filt3)


# GMM 모델 적용 결과 시각화 ---------------------------
plt.rcParams['figure.figsize'] = [20, 20]

# Draw Color-Magnitude Diagram
plt.subplot(3,3,7)
plt.scatter(cl_filt2.bp_rp, # X
        cl_filt2.phot_g_mean_mag, #Y
        marker = 's', # point type
        s = 0.1, # point size
        c = cl_filt3.group, # color = bp_rp
        cmap = 'jet')
plt.xlim(-0.5,3) # X axis range 
plt.ylim(22,6) # Y axis range
plt.xlabel('Bp - Rp')
plt.ylabel('G mag')
plt.colorbar()

# Draw Proper Motion diagram
cl_filt2['pm_error'] = (cl_filt2['pmra_error']**2 + cl_filt2['pmdec_error']**2)**0.5 # Add Proper motion error column
plt.subplot(3,3,8)
plt.scatter(cl_filt2.pmra,
        cl_filt2.pmdec,
        marker='s',
        s = 0.1,
        c = cl_filt3.group,
        cmap='jet')
plt.xlim(-20,10)
plt.ylim(-20,10)
plt.xlabel('Proper Motion in R.A.')
plt.ylabel('Proper Motion in Dec.')
plt.colorbar()

# Draw R.A. Proper Motion - Distance diagram
cl_filt2['distance'] = 1000/cl_filt2['parallax'] # Add Distance (in pc) column
plt.subplot(3,3,2) 
plt.scatter(cl_filt2.pmra,
        cl_filt2.distance,
        marker='s',
        s = 0.1,
        c = cl_filt3.group,
        cmap='jet')
plt.xlim(-20,10)
plt.ylim(0,2000)
plt.colorbar()

# Draw Dec. Proper Motion - Distance diagram
plt.subplot(3,3,3)
plt.scatter(cl_filt2.pmdec,
        cl_filt2.distance,
        marker='s',
        s = 0.1,
        c = cl_filt3.group,
        cmap='jet')
plt.xlim(-20,10)
plt.ylim(0,2000)
plt.colorbar()

# Draw R.A. Proper Motion - Radial Velocity diagram
plt.subplot(3,3,5)
plt.scatter(cl_filt2.pmra,
        cl_filt2.radial_velocity,
        marker='s',
        s = 0.1,
        c = cl_filt3.group,
        cmap='jet')
plt.xlim(-20,10)
plt.ylim(0,50)
plt.colorbar()

# Draw Dec. Proper Motion - Radial Velocity diagram
plt.subplot(3,3,6)
plt.scatter(cl_filt2.pmdec,
        cl_filt2.radial_velocity,
        marker='s',
        s = 0.1,
        c = cl_filt3.group,
        cmap='jet')
plt.xlim(-20,10)
plt.ylim(0,50)
plt.xlabel('Proper Motion in Dec.')
plt.colorbar()

# Draw Distance - Radial Velocity diagram
plt.subplot(3,3,4)
plt.scatter(cl_filt2.distance,
        cl_filt2.radial_velocity,
        marker='s',
        s = 0.1,
        c = cl_filt3.group,
        cmap='jet')
plt.xlim(0,2000)
plt.ylim(0,50)
plt.xlabel('Distance (pc)')
plt.ylabel('Radial Velocity')
plt.colorbar()

# Draw R.A. Radial Velocity - Distance Diagram
plt.subplot(3,3,1)
plt.scatter(cl_filt2.radial_velocity,
        cl_filt2.distance,
        marker='s',
        s = 0.1,
        c = cl_filt3.group,
        cmap='jet')
plt.xlim(0,50)
plt.ylim(0,2000)
plt.ylabel('Distance (pc)')
plt.xlabel('Radial Velocity')
plt.colorbar()

# Draw Spatial Potioin map(R.A. - Dec. map)
cl['mag_scale'] = (14-cl['phot_g_mean_mag'])*25
cl_filt2.loc[cl['mag_scale'] > 100, 'mag_scale']=100
cl_filt2.loc[cl['mag_scale'] < 0.01, 'mag_scale']=0.01
cl_filt2.loc[cl['phot_g_mean_mag'] < 10, 'mag_scale']=100
#print(cl[['phot_g_mean_mag','mag_scale']])
plt.subplot(3,3,9)
plt.scatter(cl_filt2.ra,
        cl_filt2.dec,
        s = cl_filt2.mag_scale,
        c = cl_filt3.group,
        cmap='jet')
plt.ylabel('R.A.')
plt.xlabel('Dec.')
plt.colorbar()

# Save gifure as a file
plt.savefig(output_group)
