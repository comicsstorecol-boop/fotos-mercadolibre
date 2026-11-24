# Herramienta de publicación masiva (Camisetas)
1. Claude identifica el estampado de cada foto y arma `lote.json`.
2. `python3 lote.py lote.json salida.xlsx` guarda fotos en `camisetas/`, genera el Excel y avanza `contador.txt`.
3. Commit + push para que las URLs queden públicas.

## Importante: fotos vía Shopify
Mercado Libre NO aceptó URLs de raw.githubusercontent.com (fotos quedaron "verificando" para siempre).
Flujo actual: fotos a GitHub -> Shopify `fileCreate` (originalSource = URL de GitHub, filename `ml-CsXXXX-nombre.jpg`)
-> usar `https://cdn.shopify.com/s/files/1/0721/1728/9233/files/ml-CsXXXX-nombre.jpg` en la columna Fotos.
Cs0001-Cs0005 quedaron quemados en ML; siguiente consecutivo en contador.txt.

## Actualización 2026-10-04
Shopify CDN tampoco funcionó ("La foto no se cargó correctamente"). Solo sirven URLs del Gestor de fotos de ML (http2.mlstatic.com).
Flujo final: Fernando sube fotos al Gestor de fotos y pega las URLs en el mismo orden que las fotos; Claude identifica, arma el Excel con gen.js.
Cs0001-Cs0010 quedaron usados en ML.

## Buzo niño cuello redondo (tipo `buzo-nino-cuello-redondo`)
Mismo consecutivo Bz (contador-buzos.txt). Acumulado propio: `acumulado-buzo-nino-cuello-redondo-desde-BzXXXX.json`, archivos de 200 buzos (lotes de 20).
`pendiente-buzo-nino-cuello-redondo.json` = nombres identificados esperando URLs del Gestor.
- Si llegan fotos/diseños repetidos (mismo estampado idéntico), se quitan siempre sin preguntar (Bz0276 eliminado por repetido).
- Segundo archivo de 200 buzos niño cuello redondo: desde Bz0377, precio 89999 (`acumulado-buzo-nino-cuello-redondo-desde-Bz0377.json`).
- Cuarto archivo de 200 buzos niño cuello redondo: desde Bz0769 (`acumulado-buzo-nino-cuello-redondo-desde-Bz0769.json`). El tercero (desde Bz0572) cerró con 196.
- Lote Bz0769-Bz0787: Santa "Rollin Holidays" (marihuana) dejado por fuera, pendiente de decisión de Fernando. Las URLs pueden llegar en otro orden que las fotos: se emparejan mirando la foto de cada URL.

## Buzo hombre cuello redondo (tipo `buzo-adulto-cuello-redondo`)
Consecutivo Bz (contador-buzos.txt), precio 89999, 6 por talla S-XL. Archivos de 100 buzos acumulando lotes (`acumulado-buzo-adulto-cuello-redondo-desde-BzXXXX.json`).
`pendiente-buzo-adulto-cuello-redondo.json` = nombres identificados esperando URLs. Primer lote (desde Bz0825): "Merry Christmas F*ckers" (Santa dedo medio) dejado por fuera, pendiente de decisión de Fernando.
