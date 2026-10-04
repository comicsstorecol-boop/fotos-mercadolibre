# Herramienta de publicación masiva (Camisetas)
1. Claude identifica el estampado de cada foto y arma `lote.json`.
2. `python3 lote.py lote.json salida.xlsx` guarda fotos en `camisetas/`, genera el Excel y avanza `contador.txt`.
3. Commit + push para que las URLs queden públicas.
