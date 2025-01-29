## app/data.py

import pandas as pd

def filter_top_teams_by_country(df, n=5):
    """
    Filtra el DataFrame para conservar solo las filas correspondientes a los n equipos
    con mayor promedio de ELO en cada país.
    """
    # Calcular el promedio de ELO por país y equipo
    avg_elo = df.groupby(['country', 'club'])['elo'].mean().reset_index()
    # Ordenar de forma descendente por el promedio de ELO dentro de cada país
    avg_elo_sorted = avg_elo.sort_values(['country', 'elo'], ascending=[True, False])
    # Seleccionar los n equipos con mejor promedio de ELO por país
    top_n_by_country = avg_elo_sorted.groupby('country').head(n)
    # Filtrar el DataFrame original
    df_filtered = pd.merge(df, top_n_by_country[['country', 'club']], on=['country', 'club'], how='inner')
    return df_filtered

def load_data(file_path):
    """
    Carga y procesa el archivo CSV, asigna colores a los equipos y filtra los datos.
    """
    df = pd.read_csv(file_path)
    
    # Diccionario de colores para los clubes
    club_colors = {
        # Inglaterra (ENG)
        'Arsenal':       '#EF0107',
        'Chelsea':       '#034694',
        'Liverpool':     '#C8102E',
        'Man City':      '#6CABDD',
        'Man United':    '#DA291C',

        # España (ESP)
        'Ath Madrid':    '#E41B17',
        'Barcelona':     '#A50044',
        'Real Madrid':   '#F5F5F5',
        'Sevilla':       '#CD212A',
        'Valencia':      '#FF9B00',

        # Francia (FRA)
        'Lille':         '#E03A3E',
        'Lyon':          '#002B5C',
        'Marseille':     '#003399',
        'Monaco':        '#CD212A',
        'Paris SG':      '#004170',

        # Alemania (GER)
        'Bayern Munich': '#DC052D',
        'Dortmund':      '#FDB913',
        'Leverkusen':    '#0033A0',
        'RB Leipzig':    '#000000',
        'Schalke 04':    '#1C2C5B',

        # Italia (ITA)
        'Inter':         '#245AA7',
        'Juventus':      '#000000',
        'Lazio':         '#6EC6E1',
        'Milan':         '#EB0A1E',
        'Roma':          '#8B0000'
    }
    
    # Agregar la columna "color" al DataFrame usando map
    df['color'] = df['club'].map(club_colors)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year

    # ELO promedio si hay varias filas por fecha
    df = df.groupby(['date', 'year', 'club', 'country', 'color'])[['elo']].mean().reset_index()

    # Filtrar países
    countries = ['ESP', 'ITA', 'ENG', 'GER', 'FRA']
    df = df[df['country'].isin(countries)]
    
    # Filtrar top 5 equipos por país
    df = filter_top_teams_by_country(df, n=5)

    return df