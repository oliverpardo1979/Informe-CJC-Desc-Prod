"""Reconstruye el cuadro del boletín y verifica el cierre de las contribuciones."""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[2]
groups={}
for file,survey in [('dopd_laboral_ventanas.csv','EAM'),('dopd_laboral_ventanas_comercio_servicios.csv',None)]:
    with (ROOT/'data/melitz_polanec/tables'/file).open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            key=(survey or r['encuesta'],r['ventana'])
            g=groups.setdefault(key,{'total':float(r['cambio_total'])})
            g[r['componente']]=float(r['valor_pp'])
keys=['dentro_media_sobrevivientes','reasignacion_covarianza_sobrevivientes','entrada','salida']
for key,g in groups.items():
    assert abs(sum(g[k] for k in keys)-g['total'])<1e-7,(key,g)
order=[('EAM',y) for y in ['2010-2015','2015-2019','2019-2024']]+[('EAC',y) for y in ['2015-2019','2020-2024']]+[('EAS',y) for y in ['2010-2015','2015-2019','2019-2024']]
lines=[r'\begin{tabular}{llrrrrr}',r'\toprule',r'Encuesta & Periodo & Total & Media & Cov. & Entrada & Salida \\',r'\midrule']
for s,y in order:
    g=groups[s,y]
    vals=[f'{0.0 if abs(g[k])<0.05 else g[k]:.1f}'.replace('.',',') for k in ['total']+keys]
    lines.append(' & '.join([s,y.replace('-','--')]+vals)+r' \\')
lines += [r'\bottomrule',r'\end{tabular}']
(ROOT/'Paper/sections/melitz_polanec/CuadroResultados.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f'Identidades verificadas: {len(groups)} ventanas. Cuadro: {len(order)} filas.')
