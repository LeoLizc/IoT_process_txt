import pandas as pd
import re

def load_csv(directory, name, muestras):
    df = pd.read_csv(f"{directory}{name}.csv")
    
    if 'sto' in df.columns:
        df['sto_int'] = df['sto'].astype(int)
        df['sto_fraq'] = df['sto'] - df['sto_int']
        
        mask = df['sto_fraq'] > 0.5
        df.loc[mask, 'sto_int'] += 1
        df.loc[mask, 'sto_fraq'] -= 1
        
        df['muestras'] = (df['sto'] + 0.5) * (32 if muestras == 4 else 64)
        df['muestras_2'] = df['sto_int'] + 0.5 - df['sto_fraq']
        
    df['prueba'] = name
    return df

def limpiar_datos(df, columnas=None, iqr_multiplier=1.5):
    df_limpio = df.copy()
    
    if columnas is None:
        columnas = df_limpio.select_dtypes(include='number').columns.tolist()

    df_limpio = df_limpio.dropna(subset=columnas)

    for col in columnas:
        Q1 = df_limpio[col].quantile(0.25)
        Q3 = df_limpio[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - iqr_multiplier * IQR
        upper_bound = Q3 + iqr_multiplier * IQR

        df_limpio = df_limpio[(df_limpio[col] >= lower_bound) & (df_limpio[col] <= upper_bound)]

    return df_limpio

def extraer_distancia(prueba):
    match = re.search(r'(?<![A-Za-z0-9])(\d+)m(?![A-Za-z])', prueba)
    if match:
        return float(match.group(1))
    return None