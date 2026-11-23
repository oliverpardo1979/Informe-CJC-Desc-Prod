"""Genera catálogo, fichas y BibTeX; --download guarda copias locales de acceso abierto."""
from pathlib import Path
import json,sys,urllib.request,hashlib
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'Literatura'
refs=json.loads((OUT/'referencias.json').read_text(encoding='utf-8'))
(OUT/'fichas').mkdir(exist_ok=True)
for r in refs:
    t=f"# {r['autores']} ({r['anio']})\n\n**{r['titulo']}**\n\n"
    for k in ['publicacion','tipo','pais','periodo','metodo','medida','lectura','localizador','hallazgo','uso','url']:
        t+=f"- **{k.capitalize()}:** {r[k]}\n"
    t+='\nConsulta: 22 de noviembre de 2026. Síntesis propia; no transcripción.\n'
    (OUT/'fichas'/f"{r['id']}.md").write_text(t,encoding='utf-8')
lines=['# Literatura para el boletín empresarial','', 'Corte: 22 de noviembre de 2026. Veinte referencias formales: once artículos publicados, un capítulo, siete informes (uno preliminar) y un documento de trabajo institucional. Revisión dirigida, no sistemática ni exhaustiva.','', 'Prioridad: América Latina; Eslovenia, Francia y Corea ofrecen contrastes metodológicos. Se distingue el estatus editorial de la versión efectivamente leída. Brown et al. solo se utiliza desde su resumen; el texto consultado de César y Falcone es una versión de autor anterior a la publicación.','', '| Referencia | País | Tipo | Alcance de lectura |','|---|---|---|---|']
for r in refs: lines.append(f"| [{r['id']}](fichas/{r['id']}.md) | {r['pais']} | {r['tipo']} | {r['lectura']} |")
lines+=['','## Organización','', '`referencias.json` es el catálogo maestro; `referencias.bib` permite reutilizar las citas. `fichas/` registra hallazgos y límites. `pdf/` guarda copias locales de acceso abierto, excluidas de Git; `descargas.json` registra URL, fecha y huella SHA-256. Para recuperarlas: `python scripts/melitz_polanec/literatura.py --download`. No se intenta eludir accesos de pago.','', '## Cómo usar la comparación','', 'Comparar primero método, medida (PTF o laboral), pesos, empresa o establecimiento, periodo, deflactor y cobertura. Por ahora el boletín contrasta mecanismos y signos, no construye un ranking internacional de magnitudes. El estudio de Colombia del Banco Mundial es una prueba pendiente de reconciliación, no una validación de nuestros resultados.','', '## Búsqueda y exclusiones','', 'Búsquedas combinando Melitz, Polanec, productividad y Chile/Colombia/Brasil; rastreo de referencias y fuentes editoriales e institucionales. Se excluyeron blogs, diapositivas y resultados sin fuente formal identificable. García-Marín (2021) se conoce a través de IFC: no se presenta como documento leído ni como artículo arbitrado. El informe FMI combina GR y MP. No se confirma la implementación exacta de Brown et al. sin acceso al artículo completo.','', '## Siguientes lecturas','', 'Conseguir el texto completo de Brown et al. y el informe técnico de García-Marín; revisar el anexo en línea del FMI; ampliar países latinoamericanos sin relajar los criterios de verificabilidad.']
(OUT/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
bib=[]
for r in refs:
    kind='article' if r['tipo'].startswith('Artículo') else 'techreport'
    author=' and '.join(r['autores'].split('; ')) if ';' in r['autores'] else '{'+r['autores']+'}'
    bib.append('@'+kind+'{'+r['id']+',\n  author = {'+author+'},\n  title = {'+r['titulo']+'},\n  year = {'+str(r['anio'])+'},\n  note = {'+r['publicacion']+'},\n  url = {'+r['url']+'}\n}')
(OUT/'referencias.bib').write_text('\n\n'.join(bib)+'\n',encoding='utf-8')
if '--download' in sys.argv:
    (OUT/'pdf').mkdir(exist_ok=True); manifest=[]
    for r in refs:
        if not r['descarga']: continue
        p=OUT/'pdf'/f"{r['id']}.pdf"
        try:
            if not p.exists():
                req=urllib.request.Request(r['descarga'],headers={'User-Agent':'Mozilla/5.0'})
                data=urllib.request.urlopen(req,timeout=60).read()
                if not data.startswith(b'%PDF'): raise ValueError('Respuesta no PDF')
                p.write_bytes(data)
            manifest.append(dict(id=r['id'],url=r['descarga'],fecha='2026-11-22',archivo=str(p.relative_to(OUT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
            print(r['id'],'OK')
        except Exception as e: manifest.append(dict(id=r['id'],url=r['descarga'],error=str(e))); print(r['id'],str(e))
    (OUT/'descargas.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
