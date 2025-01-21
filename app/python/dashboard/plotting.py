# app/python/dashboard/plotting.py

import io
import base64

# Si tu servidor no tiene entorno gráfico, configura Agg:
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def plot_team_trend(team, df, method='cubic', num_points=200, color=None, ax=None):
    """
    Grafica la tendencia suavizada del ELO para un equipo específico sobre un ax dado.
    Devuelve el ax si lo creaste internamente, o modifica el existente.
    """
    # Asegurarse de que 'date' sea datetime y extraer el año
    if df['date'].dtype != 'datetime64[ns]':
        df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year

    # Agrupar datos (promedio de ELO por año, club y country)
    df_grouped = df.groupby(['year', 'club', 'country'])[['elo']].mean().reset_index()

    # Filtrar datos del equipo y ordenar por año
    team_data = df_grouped[df_grouped['club'] == team].sort_values('year')

    if team_data.empty:
        print(f"No se encontraron datos para el equipo: {team}")
        return ax

    # Si no se suministra un color, se extrae del DataFrame original
    if color is None:
        try:
            color = df[df['club'] == team]['color'].iloc[0]
        except IndexError:
            color = None

    # Ejes x (año) y y (ELO)
    x = team_data['year'].values
    y = team_data['elo'].values

    # Generar nuevos puntos en x para suavizar
    xnew = np.linspace(x.min(), x.max(), num=num_points, endpoint=True)

    try:
        f_interp = interp1d(x, y, kind=method)
    except Exception as e:
        print(f"Error al crear la interpolación: {e}")
        return ax

    ynew = f_interp(xnew)

    # Crear ax si no se suministra
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    # Graficar puntos originales y curva
    ax.plot(x, y, 'o', color=color, alpha=0.8)
    ax.plot(xnew, ynew, '-', label=f'{team}', color=color, alpha=0.6, linewidth=3)

    ax.set_xlabel('Año')
    ax.set_ylabel('ELO')
    ax.legend(loc='best')

    return ax

def plot_team_trend_chart(df, team):
    
    # Creamos la figura
    fig, ax = plt.subplots(figsize=(10, 6))

    # Llamamos a la función existente
    plot_team_trend(team, df, ax=ax, method='cubic', num_points=200)

    # Convertimos la imagen a base64
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf8')
    plt.close(fig)

    return img_base64

def plot_top_teams_country(df, country):
    """
    Filtra el DataFrame por país y grafica en barras los 5 equipos
    con mayor promedio de ELO. Devuelve la imagen codificada en base64.
    """
    df_country = df[df['country'] == country]
    if df_country.empty:
        # Si no hay datos, retorna una imagen con texto
        fig, ax = plt.subplots(figsize=(6,4))
        ax.text(0.5, 0.5, f"No hay datos para {country}", ha='center', va='center', transform=ax.transAxes)
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close(fig)
        return img_base64

    # Calcular ELO promedio por club
    elo_mean = df_country.groupby('club')['elo'].mean().reset_index()
    top5 = elo_mean.sort_values('elo', ascending=False).head(5)

    # Obtener colores
    colors = []
    for club in top5['club']:
        subset = df[df['club'] == club]
        if not subset.empty and 'color' in subset.columns:
            colors.append(subset['color'].iloc[0])
        else:
            colors.append('skyblue')

    # Graficar
    fig, ax = plt.subplots(figsize=(10,6))
    ax.bar(top5['club'], top5['elo'], color=colors)
    ax.set_title(f"Top 5 equipos en {country} - ELO promedio")
    ax.set_xlabel("Club")
    ax.set_ylabel("ELO promedio")
    ax.tick_params(axis='x', rotation=45)

    min_elo = df['elo'].min()
    ax.set_ylim(bottom=min_elo)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf8')
    plt.close(fig)
    return img_base64

def obtener_ranking_por_pais(df, pais, top_n=5):
    """
    Para cada año, obtiene los top_n equipos del país por ELO promedio,
    asignando un ranking (1 = mejor ELO).
    Devuelve un DataFrame con columnas: club, elo, ranking, year.
    """
    rankings = []
    for anio in sorted(df['year'].unique()):
        df_anio = df[(df['year'] == anio) & (df['country'] == pais)]
        if df_anio.empty:
            continue
        ranking_df = df_anio.groupby('club')['elo'].mean().reset_index()
        ranking_df = ranking_df.sort_values('elo', ascending=False).head(top_n)
        ranking_df['ranking'] = range(1, len(ranking_df) + 1)
        ranking_df['year'] = anio
        rankings.append(ranking_df)

    if rankings:
        return pd.concat(rankings)
    else:
        return pd.DataFrame()

def plot_ranking_evolution(df, country):
    """
    Genera un gráfico de línea mostrando la evolución del ranking (Top 5) en el país dado.
    Retorna la imagen en base64.
    """
    ranking_df = obtener_ranking_por_pais(df, country, top_n=5)

    fig, ax = plt.subplots(figsize=(12,8))
    ax.set_title(f'Evolución del Ranking ELO (Top 5) en {country}')
    ax.set_xlabel('Año')
    ax.set_ylabel('Ranking (1=mejor)')

    if ranking_df.empty:
        ax.text(0.5, 0.5, f"No hay datos para {country}", ha='center', va='center', transform=ax.transAxes)
    else:
        clubs = ranking_df['club'].unique()
        for club in clubs:
            datos = ranking_df[ranking_df['club'] == club]

            # Determinar color del club
            df_color = df[df['club'] == club]
            if not df_color.empty and 'color' in df_color.columns:
                color_club = df_color['color'].iloc[0]
            else:
                color_club = 'black'

            ax.plot(datos['year'], datos['ranking'], marker='o', linewidth=5, color=color_club, label=club) 
            last_year = datos['year'].max()
            last_ranking = datos.loc[datos['year'] == last_year, 'ranking'].values[0]
            ax.text(last_year + 0.2, last_ranking, club,
                    fontsize=12, fontweight='bold', color=color_club,
                    va='center', ha='left')

        # Invertir eje Y para que el ranking 1 esté arriba
        ax.invert_yaxis()
        ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf8')
    plt.close(fig)
    return img_base64

def plot_violin_elo(df):
    """
    Genera un Violin Plot de ELO vs. país.
    Devuelve la imagen en base64.
    """
    fig, ax = plt.subplots(figsize=(10,6))
    sns.violinplot(x='country', y='elo', data=df, palette="Set3", inner='box', linewidth=1, ax=ax)
    ax.set_xlabel('País')
    ax.set_ylabel('ELO')
    ax.set_title('Distribución del ELO por País')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf8')
    plt.close(fig)
    return img_base64

def plot_heatmap_elo(df):
    """
    Crea un heatmap (club vs año) con la media de ELO.
    Devuelve la imagen en base64.
    """
    pivot_elo = df.pivot_table(index='club', columns='year', values='elo', aggfunc='mean')

    fig, ax = plt.subplots(figsize=(12,10))
    sns.heatmap(pivot_elo, cmap='coolwarm', linewidths=.5, ax=ax)
    ax.set_xlabel('Año')
    ax.set_ylabel('Club')
    ax.set_title('Heatmap de ELO (Club vs Año)')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf8')
    plt.close(fig)
    return img_base64