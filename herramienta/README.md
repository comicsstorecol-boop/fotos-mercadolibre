# Herramienta de publicación masiva (Camisetas)
1. Claude identifica el estampado de cada foto y arma `lote.json`.
2. `python3 lote.py lote.json salida.xlsx` guarda fotos en `camisetas/`, genera el Excel y avanza `contador.txt`.
3. Commit + push para que las URLs queden públicas.

## Importante: fotos vía Shopify
Mercado Libre NO aceptó URLs de raw.githubusercontent.com (fotos quedaron "verificando" para siempre).
Flujo actual: fotos a GitHub -> Shopify `fileCreate` (originalSource = URL de GitHub, filename `ml-CsXXXX-nombre.jpg`)
-> usar `https://cdn.shopify.com/s/files/1/0721/1728/9233/files/ml-CsXXXX-nombre.jpg` en la columna Fotos.
Cs0001-Cs0005 quedaron quemados en ML; siguiente consecutivo en contador.txt.
