"""Script de depuración para factores UK Gov."""
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

file_path = 'data/ghg-conversion-factors-2025-condensed-set.xlsx'
sheet_name = 'Fuels'

# Leer con None header primero
df_preview = pd.read_excel(file_path, sheet_name=sheet_name, header=None, nrows=30)

# Buscar fila con 'kg CO2e'
header_row = None
for idx in range(len(df_preview)):
    row_str = ' '.join(str(x) for x in df_preview.iloc[idx].values if pd.notna(x))
    if 'kg CO2e' in row_str:
        print(f"Encontrado 'kg CO2e' en fila {idx}")
        header_row = idx
        break

print(f"\nHeader row detectado: {header_row}")

# Leer con header correcto
df_sheet = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
print(f"\nColumnas: {df_sheet.columns.tolist()}")

# Strip whitespace
df_sheet.columns = df_sheet.columns.str.strip()
print(f"\nColumnas después de strip: {df_sheet.columns.tolist()}")

# Buscar CO2e
co2e_cols = [col for col in df_sheet.columns 
            if 'co2' in str(col).lower().replace(' ', '')]
print(f"\nColumnas CO2e encontradas: {co2e_cols}")

if co2e_cols:
    co2e_col = 'kg CO2e' if 'kg CO2e' in df_sheet.columns else co2e_cols[0]
    print(f"Columna CO2e seleccionada: '{co2e_col}'")
    
    # Ver datos
    print(f"\nDatos en columna {co2e_col}:")
    print(df_sheet[co2e_col].head(20))
    
    # Limpiar y contar
    df_sheet['kgCO2e'] = pd.to_numeric(df_sheet[co2e_col], errors='coerce')
    df_clean = df_sheet[pd.notna(df_sheet['kgCO2e'])]
    print(f"\nFilas con datos numéricos: {len(df_clean)}")
    
    print("\n✅ ¡Procesamiento exitoso!")
else:
    print("\n❌ No se encontraron columnas CO2e")
