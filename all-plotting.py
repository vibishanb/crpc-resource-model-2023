import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import common_fn as cf
import seaborn as sns
import os
sns.set_context("poster")
# plt.rcParams["svg.hashsalt"]=0

# Figures 2 and 3: Steady state plots across resource use efficiencies and supplies
## The x-axis labels in the figures generated here are the inverse of those in the main text because the initial labels referred to the resource whose supply was limited, rather than supplemented. This is also reflected in the column title of the csv file, which says ResLimits, as a reference to the resource whose external supply was limited. This notation was changed during the writing into terms of supplementation rather than limitation and the x-axis labels were modified accordingly during the preparation of the final figures.

pre_path='therapy-models/'
df=pd.read_csv('/data/1.1.1-eq_values_collated_all_res_limits.csv')

parms_array=np.unique(df['EffCases'].to_numpy())
parm_format='{}'
plot_parm=df.columns[0]

for name in parms_array:
    for popsize in df['PopSize']:
        d=df[(df['PopSize']==popsize) * (df['EffCases']==name)]
        cf.eqratio_v_parm_bar(d,plot_parm,pre_path,parm_name=name,post_path=str(popsize),save=True)

# Figure 4: Additional resource supply cases
pre_path='/extra-resource-supply-cases/pop_size-0.5k/'
parm_names=['o2-HE_test-HE', 'o2-HE_test-LE', 'o2-LE_test-HE', 'o2-LE_test-LE']
# dir_names=['1.1.1']
parm_format='{}'
cases=pd.read_csv('/data/res_supply_cases.csv')
parms_array=cases.Names.to_numpy()

for name in parm_names:
	cf.mkdirs(pre_path=pre_path,parm_name=name)
# 	cf.timeseries(pre_path=pre_path,parm_name=name,parm_array=parms_array,parm_format=parm_format)
	df=cf.eq_values(pre_path=pre_path,parm_name=name,parm_array=parms_array,parm_format=parm_format)
	df.iloc[:,1:]=df.iloc[:,1:].astype(np.float64)
	df[['p_o2', 'pt1', 'pt2', 's_test']]=df.iloc[:, 0].str.split('-', n=3, expand=True) #n=3 forces the split to happen only on the first three instances of the hyphen-I needed this because some of the s_test values with a hyphen were also getting split, adding an extra unnecessary column.
	df.drop(columns=['pt1', 'pt2'], inplace=True)
	df['s_test']=df['s_test'].astype(np.float64)
	df['p_o2']=df['p_o2'].astype(np.float64)    
	df['Total']=df['Tpos_eq']+df['Tpro_eq']+df['Tneg_eq']
	df=df[df['Tpro_eq']>0] #Preventing division by zero in the next step
	df['Tratio']=(df['Tpro_eq']/df['Tpos_eq'])
	pdf=df.pivot('p_o2', 's_test', 'Tratio').sort_index(ascending=True)
	fig,ax=plt.subplots()
	ax=sns.heatmap(pdf.astype(np.float64), annot_kws={"size": 10}, square=False, vmin=0.25, vmax=1, cmap="viridis", mask=np.zeros_like(pdf))
	fig.savefig('/figures/'+pre_path+name+'/'+'Tpro-Tpos-eqratio-vs-res-supply.svg')
	fig.clf()
	plt.close(fig)
	plot_parm=df.columns[0]
	cf.eqratio_v_parm_bar(df,plot_parm,pre_path,parm_name=name,save=True)


# Figure 5A and B: Heatmaps of upper and lower limits of o2 and test
sns.set_context("poster")
df_o2 = pd.read_csv('/data/o2-test-upper-lower-limits/l_lim_o2Tpro-u_lim_o2Tpro_eq_values.csv')
pdf_o2=df_o2.round(decimals=3).pivot('u_lim_o2Tpro', 'l_lim_o2Tpro', 'Tpro_eq')
fig,ax=plt.subplots()
ax=sns.heatmap(pdf_o2.astype(np.float64), annot_kws={"size": 10}, square=False, vmin=0, vmax=10000, cmap="viridis", mask=np.zeros_like(pdf))
ax.set_xlabel('Lower limit')
ax.set_ylabel('Upper limit')
fig.savefig('/figures/o2_lims_heatmap.svg')

df_test = pd.read_csv('/data/o2-test-upper-lower-limits/l_lim_testTpro-u_lim_testTpro_eq_values.csv')
pdf_test=df_test.round(decimals=3).pivot('u_lim_testTpro', 'l_lim_testTpro', 'Tpro_eq')
fig,ax=plt.subplots()
ax=sns.heatmap(pdf_test.astype(np.float64), annot_kws={"size": 10}, square=False, vmin=0, vmax=10000, cmap="viridis", mask=np.zeros_like(pdf))
ax.set_xlabel('Lower limit')
ax.set_ylabel('Upper limit')
fig.savefig('/figures/test_lims_heatmap.svg')


# Figure 5C: Representative time series
df = pd.read_csv("/data/representative-timeseries.csv")
fig, ax = plt.subplots(1, 1, figsize = (4, 3))
ax.plot(df.t[:600]/24/60, df.o2[:600], color="tab:cyan", label='o2')
ax.plot(df.t[:600]/24/60, df.test[:600], color="tab:orange", label='test')
ax.set_ylabel('Resource (proportion)')
ax.set_xlabel('Time (days)')
ax.legend()
plt.tight_layout()
fig.savefig('/figures/resource-dynamics-zoomed.png', dpi=300)