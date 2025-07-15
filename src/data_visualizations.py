import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression

#Histograma de las métricas
def plot_histograma(df, output_path='output'):
    
    drop_cols = ['numero', 'crc_error', 'previous_overflow_sum', 'size (bytes)']
    for col in drop_cols:
        if col in df.columns:
            df = df.drop(col, axis=1)
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if not numeric_cols:
        print("No numeric columns found.")
        return

    os.makedirs(output_path, exist_ok=True)

    for col in numeric_cols:
        plt.figure(figsize=(6, 4))
        sns.histplot(df[col].dropna(), kde=True, bins=7)
        plt.title(f'Histograma: {col}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_path, f"histograma_{col}.png"))
        plt.close()

#Diagrama de correlación de las métricas
def plot_correlacion(df, output_path='output'):
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if not numeric_cols:
        print("No numeric columns found for correlation.")
        return

    corr = df[numeric_cols].corr()

    os.makedirs(output_path, exist_ok=True)

    plt.figure(figsize=(1.2 * len(numeric_cols), 1.2 * len(numeric_cols)))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", square=True)
    plt.title("Correlación entre métricas")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "correlacion.png"))
    plt.close()

def plot_metricas_por_distancia(df, metricas, tipo='box', columna_grupo='prueba', output_path='output'):
    metricas_presentes = [m for m in metricas if m in df.columns]
    os.makedirs(output_path, exist_ok=True)

    for metrica in metricas_presentes:
        plt.figure(figsize=(6, 4))
        if tipo == 'box':
            sns.boxplot(data=df, x=columna_grupo, y=metrica)
        elif tipo == 'hist':
            sns.histplot(data=df, x=metrica, hue=columna_grupo, kde=True, element="step", common_norm=False)
        plt.title(f'{metrica} por {columna_grupo}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_path, f"{tipo}_{metrica}.png"))
        plt.close()

# Modelo de propagación de la señal
def plot_modelo_propagacion(df, nombre_modelo="", output_path='output'):
    df_modelo = df[df['rssi (dBm)'].notna() & df['distancia'].notna() & (df['distancia'] > 0)].copy()
    df_modelo['log_distancia'] = np.log10(df_modelo['distancia'])

    X = df_modelo[['log_distancia']]
    y = df_modelo['rssi (dBm)']

    modelo = LinearRegression()
    modelo.fit(X, y)

    intercepto = modelo.intercept_
    pendiente = modelo.coef_[0]
    n = -pendiente / 10

    print(f"Modelo ajustado ({nombre_modelo}):")
    print(f"rssi (dBm) ≈ {intercepto:.2f} + ({pendiente:.2f}) * log10(distancia)")
    print(f"Pérdida (n) ≈ {n:.2f}")

    os.makedirs(output_path, exist_ok=True)
    
    plt.figure(figsize=(7, 5))
    sns.scatterplot(data=df_modelo, x='log_distancia', y='rssi (dBm)', alpha=0.6, label='Datos')
    sns.lineplot(x=df_modelo['log_distancia'], y=modelo.predict(X), color='red', label='Modelo ajustado')
    plt.title(f"Modelo de propagación {nombre_modelo}: rssi (dBm) vs log10(distancia)")
    plt.xlabel("log10(distancia en metros)")
    plt.ylabel("rssi (dBm)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, f"modelo_propagacion_{nombre_modelo}.png"))
    plt.close()

    return modelo, intercepto, pendiente, n