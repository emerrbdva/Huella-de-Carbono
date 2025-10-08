import pandas as pd

# Leer el archivo con el header correcto
df = pd.read_excel('data/ghg-conversion-factors-2025-condensed-set.xlsx', 
                   sheet_name='Fuels', header=21)

print("Columnas encontradas:")
for i, col in enumerate(df.columns):
    print(f"  {i}: '{col}'")

print("\n\nPrimeras 10 filas de datos (solo columnas relevantes):")
cols_to_show = ['Activity', 'Fuel', 'Unit', 'kg CO2e']
print(df[cols_to_show].head(10))

print("\n\nFilas con datos numéricos en kg CO2e:")
df_clean = df[pd.notna(df['kg CO2e'])]
print(f"Total de filas con datos: {len(df_clean)}")
print(df_clean[cols_to_show].head(10))


