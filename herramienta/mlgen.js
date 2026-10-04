/* Motor: llena la planilla de publicación masiva de Mercado Libre.
   Clona el bloque de ejemplo (filas de la primera publicación) una vez por producto
   y cambia solo Título, Marca, Modelo y Fotos. Todo lo demás del libro queda intacto. */
(function (root) {
  const colNum = (c) => { let n = 0; for (const ch of c) n = n * 26 + ch.charCodeAt(0) - 64; return n; };
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const unesc = (s) => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&amp;/g, '&');
  const norm = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').trim().toLowerCase();

  function parseSST(xml) {
    const out = [];
    const re = /<si>([\s\S]*?)<\/si>/g; let m;
    while ((m = re.exec(xml))) {
      const parts = []; const tr = /<t(?:\s[^>]*)?>([\s\S]*?)<\/t>/g; let t;
      while ((t = tr.exec(m[1]))) parts.push(unesc(t[1]));
      out.push(parts.join(''));
    }
    return out;
  }
  function splitRows(sheetXml) {
    const start = sheetXml.indexOf('<sheetData>');
    const end = sheetXml.indexOf('</sheetData>');
    if (start < 0 || end < 0) throw new Error('La hoja no tiene datos (sheetData).');
    const body = sheetXml.slice(start + 11, end);
    const rows = []; const re = /<row\b[^>]*?(?:\/>|>[\s\S]*?<\/row>)/g; let m;
    while ((m = re.exec(body))) rows.push({ n: +/\br="(\d+)"/.exec(m[0])[1], xml: m[0] });
    return { pre: sheetXml.slice(0, start + 11), rows, post: sheetXml.slice(end) };
  }
  function parseCells(rowXml) {
    const cells = []; const re = /<c\b r="([A-Z]+)\d+"([^>]*?)(?:\/>|>([\s\S]*?)<\/c>)/g; let m;
    while ((m = re.exec(rowXml))) cells.push({ col: m[1], attrs: m[2], inner: m[3] || '' });
    return cells;
  }
  function cellText(cell, sst) {
    if (!cell) return '';
    const v = /<v>([\s\S]*?)<\/v>/.exec(cell.inner);
    if (/\bt="s"/.test(cell.attrs) && v) return sst[+v[1]] || '';
    const t = /<t(?:\s[^>]*)?>([\s\S]*?)<\/t>/.exec(cell.inner);
    if (t) return unesc(t[1]);
    return v ? unesc(v[1]) : '';
  }
  function expandShared(xml) {
    const masters = {};
    xml.replace(/<f\b([^>/]*\bt="shared"[^>/]*)>([\s\S]*?)<\/f>/g, (all, attrs, txt) => {
      const si = /\bsi="(\d+)"/.exec(attrs)[1]; masters[si] = txt; return all;
    });
    const rebuild = (attrs, si) => {
      const ca = /\bca="1"/.test(attrs) ? ' ca="1"' : '';
      return `<f${ca}>${masters[si]}</f>`;
    };
    xml = xml.replace(/<f\b([^>/]*\bt="shared"[^>/]*)>([\s\S]*?)<\/f>/g, (all, attrs) => rebuild(attrs, /\bsi="(\d+)"/.exec(attrs)[1]));
    xml = xml.replace(/<f\b([^>]*\bt="shared"[^>]*)\/>/g, (all, attrs) => rebuild(attrs, /\bsi="(\d+)"/.exec(attrs)[1]));
    return xml;
  }

  const NOF = { createFolders: false };
  async function locate(zip) {
    const wb = await zip.file('xl/workbook.xml').async('string');
    const rels = await zip.file('xl/_rels/workbook.xml.rels').async('string');
    const sstFile = zip.file('xl/sharedStrings.xml');
    const sst = sstFile ? parseSST(await sstFile.async('string')) : [];
    const sheets = [...wb.matchAll(/<sheet\b[^>]*?name="([^"]*)"[^>]*?r:id="([^"]+)"[^>]*\/>/g)].map(m => ({ name: unesc(m[1]), rid: m[2], hidden: /state="(very)?[hH]idden"/.test(m[0]) }));
    for (const s of sheets) {
      if (s.hidden) continue;
      const rel = new RegExp(`<Relationship\\b[^>]*Id="${s.rid}"[^>]*>`).exec(rels)[0];
      let target = /Target="([^"]+)"/.exec(rel)[1];
      target = target.replace(/^\/?xl\//, '').replace(/^\//, '');
      const path = 'xl/' + target;
      const xml = await zip.file(path).async('string');
      const { rows } = splitRows(xml);
      const hdrRow = rows.find(r => r.n === 3);
      if (!hdrRow) continue;
      const hdr = {}; for (const c of parseCells(hdrRow.xml)) hdr[c.col] = cellText(c, sst);
      const find = (pred) => Object.keys(hdr).find(k => pred(norm(hdr[k])));
      const cols = {
        titulo: find(h => h.startsWith('titulo')),
        marca: find(h => h === 'marca'),
        modelo: find(h => h === 'modelo'),
        fotos: find(h => h === 'fotos'),
        resumen: find(h => h.startsWith('resumen de errores')),
      };
      if (cols.titulo && cols.marca && cols.modelo && cols.fotos) return { path, sheetName: s.name, cols, sst, hdr };
    }
    throw new Error('No encontré la hoja de productos (con columnas Título, Marca, Modelo y Fotos).');
  }

  /* Lee el bloque de ejemplo: filas consecutivas con Título lleno desde la primera fila de datos. */
  async function readTemplate(zip) {
    const loc = await locate(zip);
    const xml = await zip.file(loc.path).async('string');
    const { rows } = splitRows(xml);
    const first = rows.find(r => r.n > 3 && /<f[\s>]/.test(r.xml));
    if (!first) throw new Error('No encontré la primera fila de datos.');
    const block = [];
    for (let n = first.n; ; n++) {
      const r = rows.find(x => x.n === n); if (!r) break;
      const t = cellText(parseCells(r.xml).find(c => c.col === loc.cols.titulo), loc.sst).trim();
      if (!t) break;
      block.push(r);
    }
    if (!block.length) throw new Error(`La fila ${first.n} está vacía: llena un producto de ejemplo en la planilla.`);
    const sizeCol = Object.keys(loc.hdr).find(k => norm(loc.hdr[k]) === 'talla');
    const sizes = sizeCol ? block.map(r => cellText(parseCells(r.xml).find(c => c.col === sizeCol), loc.sst)) : [];
    const ex = parseCells(block[0].xml);
    const get = (col) => cellText(ex.find(c => c.col === col), loc.sst);
    return { ...loc, startRow: first.n, blockSize: block.length, sizes,
      example: { titulo: get(loc.cols.titulo), marca: get(loc.cols.marca), modelo: get(loc.cols.modelo) } };
  }

  /* products: [{titulo, marca, modelo, fotos}] */
  async function build(JSZip, templateBuf, products) {
    const zip = await JSZip.loadAsync(templateBuf);
    const info = await readTemplate(zip);
    const { cols, path, startRow, blockSize } = info;
    let xml = expandShared(await zip.file(path).async('string'));
    const parts = splitRows(xml);
    const blockRows = parts.rows.filter(r => r.n >= startRow && r.n < startRow + blockSize);

    // Estilo por defecto de columnas (para celdas que no existían, p.ej. Fotos)
    const colStyle = {};
    for (const m of xml.matchAll(/<col\b[^>]*min="(\d+)"[^>]*max="(\d+)"[^>]*?(?:style="(\d+)")?[^>]*\/>/g)) {
      if (m[3]) for (let i = +m[1]; i <= +m[2]; i++) colStyle[i] = m[3];
    }

    // Shared strings
    const sstPath = 'xl/sharedStrings.xml';
    let sstXml = await zip.file(sstPath).async('string');
    let sstCount = parseSST(sstXml).length; const newSi = []; const sstIdx = new Map();
    const strIndex = (s) => {
      if (sstIdx.has(s)) return sstIdx.get(s);
      const i = sstCount + newSi.length; newSi.push(`<si><t xml:space="preserve">${esc(s)}</t></si>`); sstIdx.set(s, i); return i;
    };

    // Características: deben ser iguales en todas las variantes -> se toman de la primera fila del ejemplo
    const firstCells = parseCells(blockRows[0].xml);
    const charFrom = colNum(cols.modelo), charTo = cols.resumen ? colNum(cols.resumen) - 1 : colNum(cols.modelo);

    const generated = [];
    products.forEach((p, i) => {
      blockRows.forEach((br, j) => {
        const n = startRow + i * blockSize + j;
        let cells = parseCells(br.xml);
        // homogeneizar características
        cells = cells.filter(c => { const k = colNum(c.col); return !(k >= charFrom && k <= charTo); })
          .concat(firstCells.filter(c => { const k = colNum(c.col); return k >= charFrom && k <= charTo; }).map(c => ({ ...c })));
        const setStr = (col, val) => {
          let c = cells.find(x => x.col === col);
          if (!c) { const st = colStyle[colNum(col)]; c = { col, attrs: st ? ` s="${st}"` : '', inner: '' }; cells.push(c); }
          const s = /\bs="(\d+)"/.exec(c.attrs);
          if (val === '' || val == null) { c.attrs = s ? ` s="${s[1]}"` : ''; c.inner = ''; return; }
          c.attrs = (s ? ` s="${s[1]}"` : '') + ' t="s"';
          c.inner = `<v>${strIndex(val)}</v>`;
        };
        setStr(cols.titulo, p.titulo);
        setStr(cols.marca, p.marca);
        setStr(cols.modelo, p.modelo);
        setStr(cols.fotos, p.fotos);
        cells.sort((a, b) => colNum(a.col) - colNum(b.col));
        const body = cells.map(c => {
          let attrs = c.attrs, inner = c.inner;
          if (/<f[\s>]/.test(inner)) { // fórmula: quitar valor cacheado, Excel recalcula
            inner = inner.replace(/<v[^>]*\/>|<v[^>]*>[\s\S]*?<\/v>/g, '');
            attrs = attrs.replace(/\s*\bt="[^"]*"/, '');
          }
          return inner ? `<c r="${c.col}${n}"${attrs}>${inner}</c>` : `<c r="${c.col}${n}"${attrs}/>`;
        }).join('');
        const open = /^<row\b[^>]*?(?=\/?>)/.exec(br.xml)[0].replace(/\br="\d+"/, `r="${n}"`).replace(/\s*\bspans="[^"]*"/, '');
        generated.push({ n, xml: `${open}>${body}</row>` });
      });
    });
    const lastGen = startRow + products.length * blockSize - 1;
    const kept = parts.rows.filter(r => r.n < startRow || r.n > lastGen);
    const all = kept.concat(generated).sort((a, b) => a.n - b.n);
    const maxRow = all.length ? all[all.length - 1].n : lastGen;
    xml = parts.pre + all.map(r => r.xml).join('') + parts.post;
    xml = xml.replace(/<dimension ref="([A-Z]+\d+):([A-Z]+)\d+"\/>/, (m, a, b) => `<dimension ref="${a}:${b}${maxRow}"/>`);
    zip.file(path, xml, NOF);

    if (newSi.length) {
      const total = sstCount + newSi.length;
      sstXml = sstXml.replace('</sst>', newSi.join('') + '</sst>')
        .replace(/(<sst\b[^>]*?)\scount="\d+"/, `$1 count="${total}"`)
        .replace(/(<sst\b[^>]*?)\suniqueCount="\d+"/, `$1 uniqueCount="${total}"`);
      zip.file(sstPath, sstXml, NOF);
    }
    // Forzar recálculo y quitar calcChain (evita el aviso de "reparar" en Excel)
    let wb = await zip.file('xl/workbook.xml').async('string');
    wb = /<calcPr\b/.test(wb) ? wb.replace(/<calcPr\b([^>]*?)\/>/, (m, a) => `<calcPr${a.replace(/\s*fullCalcOnLoad="[^"]*"/, '')} fullCalcOnLoad="1"/>`) : wb;
    zip.file('xl/workbook.xml', wb, NOF);
    if (zip.file('xl/calcChain.xml')) {
      zip.remove('xl/calcChain.xml');
      const ct = await zip.file('[Content_Types].xml').async('string');
      zip.file('[Content_Types].xml', ct.replace(/<Override\b[^>]*calcChain[^>]*\/>/, ''), NOF);
      const rels = await zip.file('xl/_rels/workbook.xml.rels').async('string');
      zip.file('xl/_rels/workbook.xml.rels', rels.replace(/<Relationship\b[^>]*calcChain[^>]*\/>/, ''), NOF);
    }
    return { info, rows: products.length * blockSize,
      out: await zip.generateAsync({ type: 'uint8array', compression: 'DEFLATE', compressionOptions: { level: 6 } }) };
  }

  const api = { build, readTemplate: async (JSZip, buf) => readTemplate(await JSZip.loadAsync(buf)) };
  if (typeof module !== 'undefined') module.exports = api; else root.MLGen = api;
})(this);
