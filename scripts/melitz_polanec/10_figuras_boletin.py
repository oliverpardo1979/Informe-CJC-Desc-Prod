"""Figuras legibles del boletín; usa tablas existentes, sin recalcular microdatos."""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2]
T=ROOT/'data/melitz_polanec/tables'; O=ROOT/'Paper/figures/melitz_polanec'; O.mkdir(exist_ok=True,parents=True)
a=pd.read_csv(T/'dopd_laboral_ventanas.csv'); a['encuesta']='EAM'
b=pd.read_csv(T/'dopd_laboral_ventanas_comercio_servicios.csv')
d=pd.concat([a,b],ignore_index=True)
keys=['dentro_media_sobrevivientes','reasignacion_covarianza_sobrevivientes','entrada','salida']
labels=['Cambio dentro de las empresas','Reasignación entre empresas','Entrada','Salida']
colors=['#81909e','#2378bd','#e66a32','#139a76']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
orders={'EAM':['2010-2015','2015-2019','2019-2024'],'EAC':['2015-2019','2020-2024'],'EAS':['2010-2015','2015-2019','2019-2024']}
for s,order in orders.items():
    x=d[d.encuesta.eq(s)].pivot(index='ventana',columns='componente',values='valor_pp').loc[order]
    totals=d[d.encuesta.eq(s)].groupby('ventana').cambio_total.first().loc[order]
    assert np.allclose(x[keys].sum(axis=1),totals,atol=1e-7)
    fig,ax=plt.subplots(figsize=(9,4.2)); pos=np.arange(len(x)); lo=np.zeros(len(x)); hi=lo.copy()
    for k,l,c in zip(keys,labels,colors):
        v=x[k].to_numpy(); ax.barh(pos,v,left=np.where(v>=0,hi,lo),color=c,label=l,height=.48,edgecolor='white'); hi+=np.maximum(v,0); lo+=np.minimum(v,0)
    ax.scatter(totals,pos,marker='D',s=45,color='#152536',label='Cambio total',zorder=5)
    for y,v in zip(pos,totals): ax.annotate(f'{v:.1f}'.replace('.',','),(v,y),xytext=(0,18),textcoords='offset points',ha='center',weight='bold')
    ax.set_yticks(pos,order); ax.invert_yaxis(); ax.axvline(0,color='#8c99a2',lw=.8)
    ax.set_xlim(-12,20); ax.set_xlabel('Cambio acumulado (puntos logarítmicos × 100)'); ax.grid(axis='x',alpha=.15); ax.set_axisbelow(True)
    fig.legend(loc='upper center',ncol=2,frameon=False,fontsize=10); fig.subplots_adjust(top=.76,left=.14,bottom=.17,right=.97)
    fig.savefig(O/f'boletin_componentes_{s}.pdf'); plt.close(fig)
cmp=pd.read_csv(T/'dopd_laboral_comparacion.csv').iloc[:3]
fig,ax=plt.subplots(figsize=(9,3.8)); pos=np.arange(3)
for j,(m,c) in enumerate(zip(['DOPD','GR','FHK'],['#2378bd','#81909e','#bdc6cf'])):
    ax.bar(pos+(j-1)*.23,cmp[m+'_entrada'],width=.22,color=c,label=m)
ax.axhline(0,color='#8c99a2');ax.set_xticks(pos,cmp.ventana);ax.set_ylabel('Aporte de entrada (puntos log × 100)');ax.legend(frameon=False,ncol=3);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True);fig.tight_layout();fig.savefig(O/'boletin_metodos.pdf');plt.close(fig)
# Comparación cualitativa: signos, nunca magnitudes de indicadores distintos.
fig,ax=plt.subplots(figsize=(9,2.8));ax.axis('off')
tab=ax.table(cellText=[['Colombia EAM 2010–2015','−','+','−','+'],['Chile IFC 2010–2015','−','+','−','+']],colLabels=['Aplicación','Cambio dentro\nde las empresas','Reasignación\nentre empresas','Entrada','Salida'],cellLoc='center',colWidths=[.30,.23,.23,.12,.12],loc='center')
tab.auto_set_font_size(False);tab.set_fontsize(10);tab.scale(1,2.8)
for (r,c),cell in tab.get_celld().items():
    cell.set_edgecolor('white')
    cell.set_facecolor('#17324d' if r==0 else '#edf2f6')
    if r==0:cell.set_text_props(color='white',weight='bold')
fig.tight_layout();fig.savefig(O/'boletin_signos_chile.pdf');plt.close(fig)
print('Cinco figuras PDF generadas; identidades verificadas.')
