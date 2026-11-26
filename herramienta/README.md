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
`pendiente-buzo-adulto-cuello-redondo.json` = nombres identificados esperando URLs. Primer lote (desde Bz0825): Santa "Merry Christmas F*ckers" publicado como Bz0844 "Santa Merry Christmas" (sin la grosería, al final del lote).
- Primer archivo de buzos hombre cuello redondo (desde Bz0825) cerró con 89 buzos (Bz0825-Bz0913) por decisión de Fernando. El siguiente archivo arranca en Bz0914 con acumulado nuevo `acumulado-buzo-adulto-cuello-redondo-desde-Bz0914.json`.

## Camiseta hombre manga corta (tipo `camiseta-adulto`) — archivo desde Cs3099
Nuevo archivo de 160 camisetas en tandas de 20 (`acumulado-adulto-desde-Cs3099.json`).
`pendiente-camiseta-adulto.json` = nombres identificados esperando URLs del Gestor (tanda 1: Cs3099-Cs3118).
- OBLIGATORIO: antes de entregar cada Excel, abrir las URLs en Chrome (cuadrícula con código + nombre) y verificar que cada foto coincide con su nombre. Las URLs pueden venir corridas o repetidas.
- Tanda 2: las URLs venían corridas (Dragon Ball 1984 y Bunbury repetidas; sin URL Los Auténticos Decadentes y Si Vis Pacem). Se rehizo como Cs3119-Cs3136 antes de publicar; esas 2 quedan en pendiente-camiseta-adulto.json.
- Tanda 5: Pablo Escobar Confidential dejado por fuera (pendiente-camiseta-adulto.json, ya con URL), pendiente de decisión de Fernando.
