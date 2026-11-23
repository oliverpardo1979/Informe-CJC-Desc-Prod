raise SystemExit("Integrador del borrador completo desactivado: fase actual dedicada exclusivamente a Literatura.tex; compilar melitz-polanec.tex.")
"""Integra las figuras y la revisión en el borrador (idempotente)."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]; S=ROOT/'Paper/sections/melitz_polanec'
p=ROOT/'melitz-polanec.tex'; t=p.read_text(encoding='utf-8').replace('13 de noviembre de 2026','22 de noviembre de 2026')
if 'melitz_polanec/Literatura' not in t:
    t=t.replace(r'\input{Paper/sections/melitz_polanec/Metodologia}',r'\input{Paper/sections/melitz_polanec/Literatura}'+'\n'+r'\input{Paper/sections/melitz_polanec/Metodologia}')
if 'melitz_polanec/Cierre' not in t:
    t=t.replace(r'\input{Paper/sections/melitz_polanec/Referencias}',r'\input{Paper/sections/melitz_polanec/Cierre}'+'\n'+r'\clearpage'+'\n'+r'\input{Paper/sections/melitz_polanec/Referencias}')
p.write_text(t,encoding='utf-8')
p=S/'Hallazgos.tex';t=p.read_text(encoding='utf-8')
for old,new in [('fig_dopd_laboral.png','boletin_componentes_EAM.pdf'),('fig_dopd_laboral_EAC.png','boletin_componentes_EAC.pdf'),('fig_dopd_laboral_EAS.png','boletin_componentes_EAS.pdf')]:t=t.replace(old,new)
t=t.replace('Industria: componentes del cambio y comparación de la entrada','Industria: componentes del cambio de productividad')
t=t.replace('La marca negra es la suma algebraica de las contribuciones.','El rombo indica la suma algebraica de las contribuciones.')
t=t.replace('Comercio: resultados y una ventana de cobertura no comparable','Comercio: descomposición en las ventanas seleccionadas')
t=t.replace('La ventana sombreada 2010--2015 no es comparable por cambios de cobertura.','Se excluye 2010--2015 por cambios de cobertura.')
old='El panel B muestra que las referencias utilizadas por GR y FHK atribuyen a la entrada una contribución menos negativa que DOPD. Es una diferencia contable de método, no una estimación causal. Su magnitud debe revisarse con las pruebas de robustez antes de adoptar una interpretación económica definitiva.'
t=t.replace(old,'En estas ventanas industriales, GR y FHK atribuyen a la entrada una contribución menos negativa que DOPD. La comparación entre métodos se presenta por separado en la sección de resultados comparados; la revisión internacional muestra por qué ese orden no debe generalizarse.')
needle=r'\subsection{Pruebas pendientes antes de una versión publicable}'
if 'boletin_metodos.pdf' not in t:
    insert=r'''\begin{figure}[H]
\centering\includegraphics[width=.95\linewidth]{melitz_polanec/boletin_metodos.pdf}
\caption{El aporte de la entrada industrial cambia según la referencia utilizada}
\fuente{Fuente: cálculos propios sobre la misma muestra EAM. GR: Griliches--Regev; FHK: Foster--Haltiwanger--Krizan. Se comparan identidades contables, no estimadores causales.}
\end{figure}
Los tres métodos cierran sobre el mismo cambio agregado, pero distribuyen sus aportes de manera diferente. Por eso, comparar únicamente el término de reasignación de estudios que emplean métodos distintos puede inducir a conclusiones equivocadas.

\clearpage
'''
    t=t.replace(needle,insert+needle)
# La agenda extensa ahora está en el cierre; evitar una página de dos párrafos repetidos.
start=t.find(needle)
if start>=0:t=t[:start]
p.write_text(t,encoding='utf-8')
refs=json.loads((ROOT/'Literatura/referencias.json').read_text(encoding='utf-8'))
short={'melitz2015':'Melitz y Polanec','ifc2022':'IFC','cesar2020':'César y Falcone','brown2018':'Brown et al.','wb2024':'Banco Mundial','imf2025':'FMI','benhassine2019':'Ben Hassine','song2021':'Song'}
lines=[r'\begin{thebibliography}{99}']
for r in refs:
    lines.append(r'\bibitem['+short.get(r['id'], {'eslava2004':'Eslava et al.','eslava2006':'Eslava et al.','foster2001':'Foster et al.','pancost2022':'Pancost y Yeh'}.get(r['id'],r['autores']))+'('+str(r['anio'])+')]{'+r['id']+'} '+r['autores']+' ('+str(r['anio'])+'). '+r['titulo']+'. '+r'\emph{'+r['publicacion']+'}. '+r'\href{'+r['url']+r'}{Fuente editorial o institucional}.')
lines += [r'\bibitem[DANE(s. f.)]{daneEncuestas} DANE. EAM, EAC, EAS, IPP y cuentas nacionales departamentales. Archivos y decisiones documentados en \texttt{data/melitz\_polanec/fuente.md}.',r'\end{thebibliography}']
(S/'Referencias.tex').write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
print('Borrador actualizado.')
