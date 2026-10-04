// node gen.js productos.json salida.xlsx  -> llena la plantilla
const fs = require('fs'), path = require('path');
let JSZip; try { JSZip = require('jszip'); } catch { JSZip = require(path.join(__dirname, 'node_modules/jszip')); }
const G = require('./mlgen.js');
(async () => {
  const prods = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const tpl = fs.readFileSync(path.join(__dirname, 'plantilla-camisetas.xlsx'));
  const r = await G.build(JSZip, tpl, prods);
  fs.writeFileSync(process.argv[3], r.out);
  console.log(`OK ${prods.length} productos, ${r.rows} filas -> ${process.argv[3]}`);
})().catch(e => { console.error(e); process.exit(1); });
