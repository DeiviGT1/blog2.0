## app/data.py

import pandas as pd

def filter_top_teams_by_country(df, n=5):
    """
    Filtra el DataFrame para conservar solo las filas correspondientes a los n equipos 
    con mayor promedio de ELO en cada país.
    """
    # Calcular el promedio de ELO por país y equipo.
    avg_elo = df.groupby(['country', 'club'])['elo'].mean().reset_index()

    # Ordenar de forma descendente por el promedio de ELO dentro de cada país.
    avg_elo_sorted = avg_elo.sort_values(['country', 'elo'], ascending=[True, False])

    # Seleccionar los n equipos con mejor promedio de ELO por país.
    top_n_by_country = avg_elo_sorted.groupby('country').head(n)

    # Filtrar el DataFrame original.
    df_filtered = pd.merge(df, top_n_by_country[['country', 'club']], on=['country', 'club'], how='inner')
    return df_filtered

def load_data(file_path):
    """
    Carga y procesa el archivo CSV, asigna colores a los equipos y filtra los datos según los países y equipos.
    """
    df = pd.read_csv(file_path)
    
    # Diccionario de colores para los clubes
    club_colors = {
        # Inglaterra (ENG)
        'Arsenal':       '#EF0107',   # Rojo brillante
        'Chelsea':       '#034694',   # Azul fuerte
        'Liverpool':     '#C8102E',   # Rojo intenso
        'Man City':      '#6CABDD',   # Azul celeste
        'Man United':    '#DA291C',   # Rojo clásico,

        # España (ESP)
        'Ath Madrid':    '#E41B17',   # Rojo (para Atlético Madrid)
        'Barcelona':     '#A50044',   # Tono burdeos (blaugrana)
        'Real Madrid':   '#F5F5F5',   # Blanco (o gris claro para contraste)
        'Sevilla':       '#CD212A',   # Rojo
        'Valencia':      '#FF9B00',   # Naranja

        # Francia (FRA)
        'Lille':         '#E03A3E',   # Rojo
        'Lyon':          '#002B5C',   # Azul oscuro
        'Marseille':     '#003399',   # Azul
        'Monaco':        '#CD212A',   # Rojo intenso
        'Paris SG':      '#004170',   # Azul oscuro

        # Alemania (GER)
        'Bayern Munich': '#DC052D',   # Rojo
        'Dortmund':      '#FDB913',   # Amarillo brillante
        'Leverkusen':    '#0033A0',   # Azul
        'RB Leipzig':    '#000000',   # Negro
        'Schalke 04':    '#1C2C5B',   # Azul oscuro

        # Italia (ITA)
        'Inter':         '#245AA7',   # Azul
        'Juventus':      '#000000',   # Negro
        'Lazio':         '#6EC6E1',   # Azul cielo
        'Milan':         '#EB0A1E',   # Rojo
        'Roma':          '#8B0000'    # Rojo oscuro (burdeos)
    }
    
    # Agregar la columna "color" al DataFrame usando map.
    df['color'] = df['club'].map(club_colors)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year

    # Reagrupar y obtener promedio de ELO por fecha, año, club, país y color.
    df = df.groupby(['date', 'year', 'club', 'country', 'color'])[['elo']].mean().reset_index()
    
    # Filtrar solo los países deseados
    countries = ['ESP', 'ITA', 'ENG', 'GER', 'FRA']
    df = df[df['country'].isin(countries)]
    
    # Filtrar para conservar solo los top n equipos por país
    df = filter_top_teams_by_country(df, n=5)
    
    return df