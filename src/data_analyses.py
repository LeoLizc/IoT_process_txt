import pandas as pd
from scipy.stats import f_oneway, kruskal, levene, shapiro
from pingouin import welch_anova

def stats_paquetes(df):
    resumen = {}

    if 'mensaje' in df.columns:
        resumen['paquetes_totales'] = df['mensaje'].count()

    if 'crc_error' in df.columns:
        resumen['paquetes_ok'] = (df['crc_error'] == 0).sum()
        resumen['paquetes_err'] = (df['crc_error'] == 1).sum()
        resumen['crc_errors'] = df['crc_error'].sum()

    if 'previous_overflow_sum' in df.columns:
        resumen['overflow_sum'] = df['previous_overflow_sum'].sum()

    if resumen.get('paquetes_totales') and resumen.get('paquetes_ok') is not None:
        resumen['porcentaje_rx_ok'] = 100 * resumen['paquetes_ok'] / resumen['paquetes_totales']

    return pd.DataFrame([resumen])

def describir_metricas(df):
    cols = df.select_dtypes(include=['number']).columns.tolist()
    return df[cols].describe()

def comparar_metricas_por_distancia(df, metrica, columna_grupo='distancia'):
    grupos = [grupo[metrica].dropna() for _, grupo in df.groupby(columna_grupo)]

    grupos = [g for g in grupos if len(g) > 0]
    if len(grupos) < 2:
        return {"metrica": metrica, "test": "Insuficiente", "p-valor": None}

    normal = all(shapiro(g)[1] > 0.05 for g in grupos)

    # Si hay normalidad
    if normal:
        _, p_levene = levene(*grupos)
        if p_levene > 0.05:
            # Varianzas homogéneas → ANOVA clásico
            stat, p = f_oneway(*grupos)
            test = "ANOVA"
        else:
            # Varianzas desiguales → Welch ANOVA
            resultado = welch_anova(data=df[[columna_grupo, metrica]].dropna(), dv=metrica, between=columna_grupo)
            stat = resultado["F"].iloc[0]
            p = resultado["p-unc"].iloc[0]
            test = "ANOVA de Welch"
    else:
        # No hay normalidad → Kruskal-Wallis
        stat, p = kruskal(*grupos)
        test = "Kruskal-Wallis"

    return {"metrica": metrica, "test": test, "p-valor": p}