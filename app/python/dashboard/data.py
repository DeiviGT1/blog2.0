# app/python/dashboard/data.py

import pandas as pd

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
    df['color'] = df['club'].map(club_colors).fillna('#000000')
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year

    # ELO promedio si hay varias filas por fecha
    df = df.groupby(['date', 'year', 'club', 'country', 'color'])[['elo']].mean().reset_index()

    # Filtrar países
    countries = ['ESP', 'ITA', 'ENG', 'GER', 'FRA']
    df = df[df['country'].isin(countries)]

    return df