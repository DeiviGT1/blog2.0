# app/python/dashboard/data.py

import pandas as pd

def load_data(file_path):
    """
    Carga y procesa el archivo CSV, asigna colores a los equipos y filtra los datos.
    """
    df = pd.read_csv(file_path)
    
    # Diccionario de colores para los clubes
    club_colors = {
        # Ejemplos – para cada club se ha asignado un color representativo (en formato hexadecimal).
        # Nota: Para algunos clubes la información es aproximada.
        
        'Aachen':                '#E31B23',   # Rojo (basado en uniformes históricos)
        'Aalborg':               '#E31B23',   # Rojo (AaB suele usar el rojo como color principal)
        'Aalst':                 '#0066B3',   # Azul (según algunas referencias)
        'Aarhus':                '#FF7F00',   # Naranja (AGF Aarhus tradicionalmente usa tonos anaranjados)
        'Aberdeen':              '#FF0000',   # Rojo (Aberdeen FC)
        'Adanaspor':             '#E60000',   # Rojo intenso
        'AEK':                   '#FFC400',   # Amarillo (AEK Atenas suele usar amarillo y negro; aquí se elige el amarillo)
        'AIK':                   '#000000',   # Negro (AIK, club de Estocolmo, usa negro y blanco; se elige el negro)
        'Ajaccio':               '#E31B23',   # Rojo (AC Ajaccio utiliza el rojo)
        'Ajax':                  '#F99F1B',   # Naranja (Ajax de Ámsterdam es famoso por su naranja)
        'Akademisk':             '#003399',   # Azul oscuro (según equipaciones tradicionales)
        'Alanya':                '#C8102E',   # Rojo (basado en colores históricos de clubes turcos similares)
        'Alaves':                '#0040FF',   # Azul (Alavés tradicionalmente usa azul)
        'Albacete':              '#0070BB',   # Azul (basado en su equipación)
        'Altay':                 '#E31B23',   # Rojo (Altay SK suele usar rojo)
        'Alverca':               '#0000FF',   # Azul (referencia aproximada)
        'Alzano':                '#FF0000',   # Rojo (basado en uniformes históricos)
        'Amica Wronki':          '#E31B23',   # Rojo (común en equipos polacos)
        'Amiens':                '#E31B23',   # Rojo (Amiens SC utiliza rojo como color principal)
        'Anderlecht':            '#440099',   # Púrpura (Anderlecht es conocido por el púrpura)
        'Ankaraguecue':          '#B31B1B',   # Rojo oscuro (en línea con varios clubes turcos)
        'Antalyaspor':           '#FF7F00',   # Naranja (Antalyaspor suele usar naranja)
        'Anzhi':                 '#008000',   # Verde (Anzhi Makhachkala suele usar verde)
        'Apollon':               '#003399',   # Azul (Apollon Limassol utiliza azul)
        'Arges Pitesti':         '#E31B23',   # Rojo (según equipaciones históricas)
        'Aris':                  '#003399',   # Azul (Aris FC griego tradicionalmente usa azul)
        'Arsenal':               '#EF0107',   # Rojo (oficial)
        'Aston Villa':           '#670E36',   # Púrpura oscuro (Aston Villa tradicionalmente usa púrpura)
        'Astra':                 '#E31B23',   # Rojo (basado en colores históricos)
        'Atalanta':              '#1D7A46',   # Verde (Atalanta utiliza el verde y negro; se elige el verde)
        'Ath Bilbao':            '#DB001B',   # Rojo (Athletic Club de Bilbao usa rojo y blanco; se elige el rojo)
        'Ath Madrid':            '#E41B17',   # Rojo (oficial en el ejemplo)
        'Atletico B':            '#D71920',   # Rojo (variante del rojo del Atlético de Madrid)
        'Austria Wien':          '#5B0099',   # Violeta (Austria Viena usa tonos violetas)
        'Auxerre':               '#003399',   # Azul (Auxerre históricamente usa azul)
        'AZ Alkmaar':            '#0000FF',   # Azul (AZ es conocido por su azul)
        'Bacau':                 '#FF0000',   # Rojo (según equipación local)
        'Badajoz':               '#006633',   # Verde (color tradicional en equipos de la zona)
        'Barcelona':             '#A50044',   # Rojo (según ejemplo)
        'Bari':                  '#0000FF',   # Azul (Bari suele usar azul y blanco; se elige el azul)
        'Barnsley':              '#FF0000',   # Rojo (Barnsley FC utiliza rojo)
        'Bastia':                '#004170',   # Azul (Bastia utiliza azul y blanco; se elige el azul)
        'Bayern Munich':         '#DC052D',   # Rojo (oficial en el ejemplo)
        'Beerschot VA':          '#E31B23',   # Rojo (según referencias históricas)
        'Beira Mar':             '#0066CC',   # Azul (común en clubes portuenses)
        'Belenenses':            '#0000FF',   # Azul (tradicional en el club lisboeta)
        'Benfica':               '#FF0000',   # Rojo (Benfica es conocido por su rojo)
        'Besiktas':              '#000000',   # Negro (oficialmente negro y blanco)
        'Betis':                 '#008000',   # Verde (Betis usa verde y rojo; se elige el verde)
        'Beveren':               '#003399',   # Azul (color tradicional)
        'Bielefeld':             '#0000FF',   # Azul (Bielefeld usa azul)
        'Birmingham':            '#003399',   # Azul (Birmingham City usa azul)
        'Bistrita':              '#E31B23',   # Rojo (basado en colores históricos)
        'Blackburn':             '#000000',   # Negro (Blackburn Rovers usa negro y blanco)
        'Boavista':              '#000000',   # Negro (Boavista FC es famoso por su camiseta negra)
        'Bochum':                '#003399',   # Azul (Bochum utiliza azul)
        'Bodoe Glimt':           '#FFCC00',   # Amarillo (Bodø/Glimt es conocido por su amarillo brillante)
        'Bologna':               '#ED1C24',   # Rojo (Bologna FC usa rojo y azul, se elige el rojo)
        'Bolton':                '#FFFFFF',   # Blanco (Bolton Wanderers tradicionalmente usa blanco)
        'Bordeaux':              '#0000FF',   # Azul (Bordeaux suele usar azul y blanco)
        'Bradford':              '#FF0000',   # Rojo (según equipación histórica)
        'Brann':                 '#0000FF',   # Azul (SK Brann utiliza azul)
        'Brasov':                '#E31B23',   # Rojo (basado en fuentes históricas)
        'Bregenz':               '#003399',   # Azul (según equipación local)
        'Brescia':               '#0000FF',   # Azul (Brescia utiliza azul)
        'Brondby':               '#FF0000',   # Rojo (Brøndby IF usa rojo)
        'Bryne':                 '#E31B23',   # Rojo (según referencias locales)
        'Bursaspor':             '#C8102E',   # Rojo (Bursaspor utiliza rojo y blanco)
        'Caen':                  '#0000FF',   # Azul (Stade Malherbe Caen usa azul)
        'Cagliari':              '#003399',   # Azul (Cagliari CF tradicionalmente usa azul)
        'Cambuur':               '#FFCC00',   # Amarillo (SC Cambuur usa amarillo)
        'Campomaiorense':        '#006600',   # Verde (color aproximado para equipos portugueses de divisiones inferiores)
        'Cannes':                '#0000FF',   # Azul (según equipación histórica)
        'Celta':                 '#00B2A9',   # Turquesa (Celta de Vigo es conocido por este color)
        'Celtic':                '#009933',   # Verde (Celtic FC es famoso por su verde)
        'Cesena':                '#0000FF',   # Azul (Cesena suele usar azul)
        'Charleroi':             '#E31B23',   # Rojo (según equipación actual/histórica)
        'Charlton':              '#E31B23',   # Rojo (Charlton Athletic usa rojo y blanco)
        'Chateauroux':           '#003399',   # Azul (según equipación)
        'Chelsea':               '#034694',   # Azul (oficial)
        'Chemnitz':              '#E31B23',   # Rojo (según fuentes históricas en el fútbol alemán)
        'Chievo':                '#004170',   # Azul oscuro (Chievo Verona utiliza azul oscuro)
        'Club Brugge':           '#0000FF',   # Azul (Club Brugge es conocido por su azul)
        'Compostela':            '#006600',   # Verde (CD Compostela utiliza verde en algunas épocas)
        'Cordoba':               '#E31B23',   # Rojo (según equipaciones históricas)
        'Cosenza':               '#0000FF',   # Azul (Cosenza usa azul y blanco)
        'Cottbus':               '#008000',   # Verde (1. FC Cottbus utiliza verde)
        'Coventry':              '#009933',   # Verde (Coventry City es conocido por el verde)
        'Craiova 1948':          '#E31B23',   # Rojo (CS Universitatea Craiova suele usar rojo)
        'Creteil':               '#0000FF',   # Azul (Creteil usa azul en sus uniformes)
        'Crewe':                 '#E31B23',   # Rojo (Crewe Alexandra tradicionalmente utiliza rojo)
        'Crystal Palace':        '#1B458F',   # Azul (Crystal Palace es reconocido por su azul)
        'CSKA Moskva':           '#CC0000',   # Rojo (CSKA de Moscú usa rojo)
        'Cuiseaux-Louhans':      '#003399',   # Azul (color representativo aproximado)
        'Den Bosch':             '#E31B23',   # Rojo (FC Den Bosch suele usar rojo)
        'Denizlispor':           '#E60000',   # Rojo (Denizlispor utiliza rojo en su imagen)
        'Derby':                 '#FFFFFF',   # Blanco (Derby County tradicionalmente usa blanco y negro)
        'Dinamo Bucuresti':      '#E31B23',   # Rojo (Dinamo es conocido por su rojo)
        'Dortmund':              '#FDB913',   # Amarillo (oficial en el ejemplo)
        'Duisburg':              '#0000FF',   # Azul (Duisburger SV utiliza azul)
        'Dundee':                '#0000FF',   # Azul (Dundee FC suele usar azul)
        'Dundee United':         '#FF0000',   # Rojo (Dundee United utiliza rojo y naranja; se elige el rojo)
        'Dynamo Moskva':         '#E31B23',   # Rojo (variante del rojo del Dinamo)
        'Eibar':                 '#0000FF',   # Azul (SD Eibar es conocido por su azul)
        'Ein Frankfurt':         '#000000',   # Negro (Eintracht Frankfurt utiliza negro y rojo)
        'Elche':                 '#0070BB',   # Azul (Elche CF suele usar azul)
        'Elfsborg':              '#FFCC00',   # Amarillo (IF Elfsborg utiliza amarillo)
        'Empoli':                '#0070BB',   # Azul (Empoli FC usa azul)
        'Erzurumspor':           '#E60000',   # Rojo (común en clubes turcos)
        'Esbjerg':               '#003399',   # Azul (Esbjerg fB utiliza azul)
        'Espanol':               '#FF0000',   # Rojo (RCD Espanyol suele usar rojo y azul; se elige el rojo)
        'Est Amadora':           '#006600',   # Verde (según equipación histórica)
        'Ethnikos Asteras':       '#E31B23',   # Rojo (equipación aproximada para clubes griegos)
        'Everton':               '#003399',   # Azul (Everton FC es conocido por su azul)
        'Extensiv Craiova':      '#E31B23',   # Rojo (basado en equipos rumanos)
        'Extremadura':           '#006600',   # Verde (según equipación histórica)
        'Fakel Voronezh':        '#E31B23',   # Rojo (en línea con otros equipos rusos)
        'Farense':               '#FFCC00',   # Amarillo (según equipación local)
        'Farul':                 '#0000FF',   # Azul (color aproximado)
        'FC Kobenhavn':          '#FFFFFF',   # Blanco (FCK suele usar blanco)
        'FC Koln':               '#EE0000',   # Rojo (1. FC Köln es conocido por su rojo)
        'Fenerbahce':            '#14274E',   # Azul oscuro (Fenerbahçe utiliza azul oscuro y amarillo; se elige el azul oscuro)
        'Fermana':               '#E31B23',   # Rojo (según equipación histórica)
        'Feyenoord':             '#FF0000',   # Rojo (Feyenoord es reconocido por su rojo)
        'Fiorentina':            '#59006B',   # Violeta (Fiorentina es famosa por su violeta)
        'For Sittard':           '#FFCC00',   # Amarillo (color aproximado)
        'Fortuna Koeln':         '#E31B23',   # Rojo (basado en uniformes históricos)
        'Freiburg':              '#009933',   # Verde (SC Freiburg es conocido por su verde)
        'Fulham':                '#FFFFFF',   # Blanco (Fulham suele usar blanco)
        'GAIS':                  '#006600',   # Verde (GAIS, club sueco, utiliza verde)
        'GAK':                   '#0000FF',   # Azul (según equipación histórica)
        'Galatasaray':           '#A30B0B',   # Rojo (Galatasaray es conocido por el rojo y amarillo; se elige el rojo)
        'Gaziantepspor':         '#E60000',   # Rojo (común en equipos de la región)
        'Geel':                  '#FFCC00',   # Amarillo (K.F.C. Verbroedering Geel utiliza amarillo)
        'Genclerbirligi':        '#E60000',   # Rojo (común en clubes turcos)
        'Genk':                  '#E31B23',   # Rojo (Genk utiliza rojo)
        'Genoa':                 '#000080',   # Azul oscuro (Genoa CFC tradicionalmente usa azul)
        'Gent':                  '#003399',   # Azul (KAA Gent es conocido por su azul)
        'Getafe':                '#00529F',   # Azul (Getafe CF utiliza azul)
        'Gil Vicente':           '#006600',   # Verde (según equipación portuguesa)
        'Goeteborg':             '#0000FF',   # Azul (IFK Göteborg utiliza azul)
        'Gornik':                '#E31B23',   # Rojo (equipación aproximada para clubes polacos)
        'Goztep':                '#E60000',   # Rojo (similar a otros clubes turcos)
        'Graafschap':            '#FFCC00',   # Amarillo (tradicional en el club)
        'Greuther Furth':        '#003399',   # Azul (en línea con la imagen del club)
        'Grimsby':               '#0000FF',   # Azul (Grimsby Town utiliza azul)
        'Grodzisk':              '#E31B23',   # Rojo (basado en fuentes históricas)
        'Gueugnon':              '#003399',   # Azul (según equipación histórica)
        'Guimaraes':             '#FF0000',   # Rojo (Vitória SC de Guimarães suele usar rojo)
        'Guingamp':              '#FF0000',   # Rojo (Guingamp es conocido por su rojo)
        'Haecken':               '#000000',   # Negro (color representativo aproximado)
        'Haka':                  '#FFCC00',   # Amarillo (FC Haka suele usar amarillo)
        'Halmstad':              '#006600',   # Verde (Halmstads BK utiliza verde)
        'Hamburg':               '#FFFFFF',   # Blanco (Hamburger SV es conocido por su blanco)
        'Hammarby':             '#008000',   # Verde (Hammarby IF utiliza verde)
        'Hannover':              '#0000FF',   # Azul (Hannover 96 suele usar azul)
        'Hansa Rostock':         '#0040FF',   # Azul (Hansa Rostock utiliza azul)
        'Harelbeke':             '#E31B23',   # Rojo (basado en equipación histórica belga)
        'Haugesund':             '#FFCC00',   # Amarillo (FK Haugesund utiliza amarillo)
        'Hearts':                '#000000',   # Negro (Heart of Midlothian es conocido por el negro)
        'Heerenveen':            '#0066FF',   # Azul (SC Heerenveen utiliza azul y blanco; se elige el azul)
        'Helsingborg':           '#003399',   # Azul (Helsingborgs IF es conocido por el azul)
        'Herfolge':              '#E31B23',   # Rojo (según equipación histórica)
        'Hertha':                '#004170',   # Azul (Hertha BSC utiliza azul)
        'Hibernian':             '#006600',   # Verde (Hibernian FC suele usar verde)
        'HJK Helsinki':          '#FFCC00',   # Amarillo (HJK utiliza amarillo)
        'Huddersfield':          '#0000FF',   # Azul (Huddersfield Town usa azul)
        'Inter':                 '#245AA7',   # Azul (oficial en el ejemplo)
        'Ionikos':               '#E31B23',   # Rojo (basado en equipación griega)
        'Ipswich':               '#0000FF',   # Azul (Ipswich Town utiliza azul)
        'Iraklis':               '#003399',   # Azul (según equipación histórica griega)
        'Istanbulspor':          '#E60000',   # Rojo (común en equipos turcos)
        'Jokerit':               '#000000',   # Negro (club finlandés, se asigna negro)
        'Juventus':              '#000000',   # Negro (oficial)
        'Kaiserslautern':        '#FF0000',   # Rojo (1. FC Kaiserslautern usa rojo)
        'Kalamata':              '#E31B23',   # Rojo (según equipación histórica griega)
        'Karlsruhe':             '#0066CC',   # Azul (Karlsruher SC utiliza azul)
        'Kavala':                '#E31B23',   # Rojo (basado en equipación histórica)
        'Kilmarnock':            '#0000FF',   # Azul (Kilmarnock FC usa azul)
        'Kocaelispor':           '#E60000',   # Rojo (club turco tradicionalmente rojo)
        'Kryliya Sovetov':       '#006600',   # Verde (según equipación de clubes rusos)
        'La Coruna':             '#A50044',   # Vino (Deportivo La Coruña es conocido por este tono)
        'Las Palmas':            '#FFA500',   # Naranja (UD Las Palmas utiliza naranja)
        'LASK':                  '#003399',   # Azul (LASK Linz suele usar azul)
        'Laval':                 '#FF0000',   # Rojo (USL Dunkerque y Laval usan rojo en algunas épocas)
        'Lazio':                 '#6EC6E1',   # Azul celeste (oficial en el ejemplo)
        'Le Havre':              '#0000FF',   # Azul (Le Havre AC utiliza azul)
        'Le Mans':               '#E31B23',   # Rojo (según equipación histórica)
        'Lecce':                 '#E60000',   # Rojo (U.S. Lecce usa rojo)
        'Lech':                  '#0066CC',   # Azul (Lech Poznań es conocido por su azul)
        'Leeds':                 '#FFFFFF',   # Blanco (Leeds United tradicionalmente usa blanco)
        'Leganes':               '#00529F',   # Azul (CD Leganés utiliza azul)
        'Legia':                 '#E31B23',   # Rojo (Legia Warszawa usa rojo)
        'Leicester':             '#003399',   # Azul (Leicester City utiliza azul)
        'Leiria':                '#006600',   # Verde (según equipación histórica)
        'Lens':                  '#E60000',   # Rojo (RC Lens es conocido por el rojo)
        'Levante':               '#003399',   # Azul (Levante UD utiliza azul y rojo; se elige el azul)
        'Leverkusen':            '#0033A0',   # Azul (oficial en el ejemplo)
        'Lierse':                '#E31B23',   # Rojo (según equipación belga histórica)
        'Lille':                 '#E03A3E',   # Rojo (oficial en el ejemplo)
        'Lillestrom':            '#0000FF',   # Azul (IL Hødd y Lillestrøm suelen usar azul)
        'Liverpool':             '#C8102E',   # Rojo (oficial)
        'LKS':                  '#003399',   # Azul (color aproximado para clubes polacos/esteuropeos)
        'Lleida':                '#E31B23',   # Rojo (según equipación histórica)
        'Logrones':              '#FF0000',   # Rojo (color aproximado)
        'Lok Moskva':            '#E31B23',   # Rojo (basado en equipos rusos)
        'Lok Nizhny':            '#E31B23',   # Rojo (similar al anterior)
        'Lokeren':               '#003399',   # Azul (en línea con la imagen del club belga)
        'Lommel':                '#E60000',   # Rojo (según equipación local)
        'Lorient':               '#0000FF',   # Azul (en línea con el FC Lorient)
        'Lubin':                 '#0066CC',   # Azul (color aproximado para clubes polacos)
        'Lustenau':              '#0000FF',   # Azul (según equipación local)
        'Lyngby':                '#FFCC00',   # Amarillo (Lyngby BK utiliza amarillo)
        'Lyon':                  '#002B5C',   # Azul oscuro (oficial en el ejemplo)
        'Maastricht':            '#E31B23',   # Rojo (color aproximado)
        'Mainz':                 '#FF0000',   # Rojo (1. FSV Mainz 05 suele usar rojo y blanco; se elige el rojo)
        'Malaga':                '#0000FF',   # Azul (Málaga CF utiliza azul)
        'Mallorca':              '#FF0000',   # Rojo (RCD Mallorca es conocido por el rojo)
        'Man City':              '#6CABDD',   # Azul (oficial en el ejemplo)
        'Man United':            '#DA291C',   # Rojo (oficial en el ejemplo)
        'Mannheim':              '#003399',   # Azul (según equipación histórica)
        'Maritimo':              '#006600',   # Verde (color aproximado para clubes portugueses)
        'Marseille':             '#003399',   # Azul (oficial en el ejemplo)
        'Mechelen':              '#E31B23',   # Rojo (KV Mechelen suele usar rojo)
        'Merida':                '#E31B23',   # Rojo (según equipación histórica)
        'Metz':                  '#006600',   # Verde (FC Metz usa verde)
        'MGladbach':             '#009900',   # Verde (Borussia M'Gladbach suele usar verde; variante)
        'Middlesbrough':         '#E60000',   # Rojo (Middlesbrough FC utiliza rojo)
        'Milan':                 '#EB0A1E',   # Rojo (oficial en el ejemplo)
        'Molde':                 '#0000FF',   # Azul (Molde FK utiliza azul)
        'Monaco':                '#CD212A',   # Rojo (oficial en el ejemplo)
        'Montpellier':           '#FF0000',   # Rojo (Montpellier HSC suele usar rojo)
        'Monza':                 '#E31B23',   # Rojo (color aproximado)
        'Moss':                  '#003399',   # Azul (según equipación local)
        'Motherwell':            '#FF0000',   # Rojo (Motherwell FC utiliza rojo)
        'Mouscron':              '#E31B23',   # Rojo (según equipación histórica belga)
        'Munich 1860':           '#0080FF',   # Azul (TSV 1860 München suele usar azul)
        'Nancy':                 '#003399',   # Azul (AS Nancy-Lorraine utiliza azul)
        'Nantes':                '#009900',   # Verde (FC Nantes es conocido por su verde)
        'Napoli':                '#1C8DFF',   # Azul (Napoli suele usar azul celeste)
        'Newcastle':             '#000000',   # Negro (Newcastle United utiliza negro y blanco)
        'Nice':                  '#0000FF',   # Azul (OGC Nice utiliza azul)
        'Nijmegen':              '#FF0000',   # Rojo (Vitesse Arnhem y otros equipos de la región suelen usar rojo)
        'Nimes':                 '#E60000',   # Rojo (Nîmes Olympique utiliza rojo)
        'Niort':                 '#003399',   # Azul (Chamois Niortais utiliza azul)
        'Norrkoeping':           '#E31B23',   # Rojo (color aproximado para equipos suecos)
        'Norwich':               '#FFCC00',   # Amarillo (Norwich City es conocido por el amarillo)
        'Nottm Forest':          '#FD8500',   # Naranja (Nottingham Forest suele usar naranja)
        'Noworossisk':           '#E31B23',   # Rojo (según equipación local en Rusia)
        'Numancia':              '#E31B23',   # Rojo (CD Numancia utiliza rojo)
        'Nurnberg':              '#E60000',   # Rojo (1. FC Nürnberg es conocido por el rojo)
        'Oberhausen':            '#003399',   # Azul (según equipación histórica)
        'Odd Grenland':          '#0000FF',   # Azul (Odd, club noruego, utiliza azul)
        'Odense':                '#FFCC00',   # Amarillo (Odense Boldklub utiliza amarillo)
        'Odra Wodzislaw':        '#E31B23',   # Rojo (según equipación histórica)
        'Oerebro':               '#003399',   # Azul (color aproximado para equipos suecos)
        'Oergryte':              '#006600',   # Verde (Orebro SK, similar a Oerebro, usa verde)
        'Offenbach':             '#E31B23',   # Rojo (según equipación histórica)
        'OFI':                   '#0000FF',   # Azul (OFI Creta utiliza azul)
        'Olympiakos':            '#FF0000',   # Rojo (Olympiakos FC es conocido por su rojo)
        'Onesti':                '#003399',   # Azul (color aproximado para equipos rumanos)
        'Osasuna':               '#E60000',   # Rojo (CA Osasuna utiliza rojo)
        'Otelul Galati':         '#0000FF',   # Azul (Oțelul Galați suele usar azul)
        'Oviedo':                '#006600',   # Verde (Real Oviedo utiliza verde)
        'Panahaiki':             '#E31B23',   # Rojo (color aproximado para clubes griegos)
        'Panathinaikos':         '#009933',   # Verde (Panathinaikos FC es famoso por su verde)
        'Paniliakos':            '#E31B23',   # Rojo (según equipación histórica griega)
        'Panionios':             '#0000FF',   # Azul (Panionios utiliza azul)
        'PAOK':                  '#000000',   # Negro (PAOK utiliza negro y blanco)
        'Paris SG':              '#004170',   # Azul (oficial en el ejemplo)
        'Parma':                 '#0000FF',   # Azul (Parma FC tradicionalmente usa azul)
        'Perugia':               '#E31B23',   # Rojo (según equipación histórica)
        'Pescara':               '#E60000',   # Rojo (Pescara Calcio utiliza rojo)
        'Petrolul Ploiesti':     '#E31B23',   # Rojo (color aproximado para clubes rumanos)
        'Piacenza':              '#0000FF',   # Azul (según equipación histórica)
        'Piatra Neamt':          '#E31B23',   # Rojo (color representativo aproximado)
        'Pistoiese':             '#006600',   # Verde (según equipación italiana de divisiones inferiores)
        'Plock':                 '#FFCC00',   # Amarillo (color aproximado para equipos polacos)
        'Pogon':                 '#E31B23',   # Rojo (según equipación histórica)
        'Polonia Warszawa':      '#E60000',   # Rojo (tradicional en equipos polacos)
        'Port Vale':             '#0000FF',   # Azul (Port Vale utiliza azul y blanco)
        'Porto':                 '#0000FF',   # Azul (FC Porto es conocido por su azul)
        'Portsmouth':            '#FF0000',   # Rojo (Portsmouth FC utiliza rojo)
        'Progresul':             '#E31B23',   # Rojo (color aproximado para equipos rumanos)
        'Proodeftiki':           '#003399',   # Azul (según equipación griega)
        'PSV Eindhoven':         '#E60000',   # Rojo (PSV suele usar rojo y blanco; se elige el rojo)
        'QPR':                   '#FFFFFF',   # Blanco (Queens Park Rangers utiliza blanco y azul, se elige el blanco)
        'Radzionkow':            '#E31B23',   # Rojo (según equipación histórica)
        'Rangers':               '#0000FF',   # Azul (Rangers FC es conocido por su azul)
        'Rapid Bucuresti':       '#E31B23',   # Rojo (Rapid suele usar rojo)
        'Rapid Wien':            '#003399',   # Azul (Rapid Viena utiliza azul)
        'Ravenna':               '#E60000',   # Rojo (color aproximado)
        'Real Madrid':           '#C4C4C4',   # Gris (oficial en el ejemplo)
        'Recreativo':            '#E31B23',   # Rojo (según equipación histórica andaluza)
        'Reggina':               '#0000FF',   # Azul (Reggina Calcio suele usar azul)
        'Rennes':                '#E31B23',   # Rojo (según equipación actual)
        'Resita':                '#006600',   # Verde (color representativo aproximado)
        'Ried':                  '#0000FF',   # Azul (SV Ried utiliza azul)
        'Rio Ave':               '#006600',   # Verde (Rio Ave FC suele usar verde)
        'Rocar Bucuresti':       '#E31B23',   # Rojo (color aproximado)
        'Roda':                  '#0000FF',   # Azul (Roda JC utiliza azul)
        'Roma':                  '#8B0000',   # Rojo oscuro (oficial en el ejemplo)
        'Rosenborg':             '#008000',   # Verde (Rosenborg BK es conocido por el verde)
        'Rostov':                '#003399',   # Azul (FC Rostov utiliza azul)
        'Rotor Volgograd':       '#E31B23',   # Rojo (según equipación histórica)
        'Ruch':                  '#E31B23',   # Rojo (color aproximado para equipos polacos)
        'Salamanca':             '#E31B23',   # Rojo (según equipación histórica)
        'Salernitana':           '#E60000',   # Rojo (Salernitana utiliza rojo)
        'Salgueiros':            '#006600',   # Verde (color representativo aproximado)
        'Salzburg':              '#FF0000',   # Rojo (FC Red Bull Salzburg utiliza rojo y blanco; se elige el rojo)
        'Sampdoria':             '#0000FF',   # Azul (Sampdoria es conocido por su azul)
        'Samsunspor':            '#E60000',   # Rojo (según equipación turca)
        'Santa Clara':           '#0000FF',   # Azul (CD Santa Clara utiliza azul)
        'Santander':             '#0066CC',   # Azul (CD Santander utiliza azul)
        'Saturn Ramenskoje':     '#E31B23',   # Rojo (según equipación histórica)
        'Savoia':                '#0000FF',   # Azul (color aproximado)
        'Schalke 04':            '#1C2C5B',   # Azul oscuro (oficial en el ejemplo)
        'Sedan':                 '#003399',   # Azul (CS Sedan utiliza azul)
        'Setubal':               '#FF0000',   # Rojo (Setúbal suele usar rojo)
        'Sevilla':               '#CD212A',   # Rojo (oficial en el ejemplo)
        'Sheffield United':      '#EE2737',   # Rojo (Sheffield United utiliza rojo)
        'Sheffield Weds':        '#000000',   # Negro (por la historia del club)
        'Silkeborg':             '#006600',   # Verde (color aproximado)
        'Sochaux':               '#003399',   # Azul (FC Sochaux utiliza azul)
        'Sociedad':              '#0066CC',   # Azul (Real Sociedad es conocido por su azul)
        'Southampton':           '#D71920',   # Rojo (Southampton FC utiliza rojo)
        'Sp Braga':              '#FF0000',   # Rojo (Sporting Braga es conocido por el rojo)
        'Sp Gijon':              '#006600',   # Verde (Real Sporting de Gijón utiliza verde)
        'Sp Lisbon':             '#0066CC',   # Azul (Sport Lisboa e Benfica suele usar azul y rojo; se elige el azul)
        'Sparta Rotterdam':      '#E31B23',   # Rojo (Sparta Rotterdam utiliza rojo)
        'Spartak Moskva':        '#E31B23',   # Rojo (Spartak de Moscú utiliza rojo)
        'St Etienne':            '#E31B23',   # Rojo (AS Saint-Étienne es conocido por el rojo)
        'St Johnstone':          '#006600',   # Verde (color aproximado para el club escocés)
        'St Pauli':              '#000000',   # Negro (St. Pauli es famoso por su negro)
        'St Truiden':            '#003399',   # Azul (color representativo aproximado)
        'Stabaek':               '#006600',   # Verde (Stabæk Fotball utiliza verde)
        'Standard':              '#E60000',   # Rojo (Standard de Liège suele usar rojo)
        'Start':                 '#0000FF',   # Azul (IK Start utiliza azul)
        'Steaua':                '#E31B23',   # Rojo (FCSB, anteriormente Steaua, utiliza rojo)
        'Stockport':             '#FF0000',   # Rojo (según equipación histórica)
        'Stomil':                '#003399',   # Azul (color representativo aproximado)
        'Strasbourg':            '#E60000',   # Rojo (RC Strasbourg utiliza rojo y azul; se elige el rojo)
        'Sturm Graz':            '#0000FF',   # Azul (Sturm Graz es conocido por su azul)
        'Stuttgart':             '#E31B23',   # Rojo (VfB Stuttgart suele usar rojo)
        'Sunderland':            '#FF0000',   # Rojo (Sunderland utiliza rojo)
        'Sundsvall':             '#006600',   # Verde (color aproximado para equipos suecos)
        'Swindon':               '#FF0000',   # Rojo (Swindon Town utiliza rojo)
        'TeBe':                  '#E31B23',   # Rojo (según equipación histórica)
        'Tenerife':              '#0066CC',   # Azul (CD Tenerife utiliza azul)
        'Ternana':               '#E31B23',   # Rojo (color aproximado)
        'Toledo':                '#0000FF',   # Azul (CD Toledo utiliza azul)
        'Torino':                '#800000',   # Granate (Torino FC es conocido por este color)
        'Torpedo Moskva':        '#E31B23',   # Rojo (según equipación histórica)
        'Tottenham':             '#132257',   # Azul oscuro (Tottenham Hotspur utiliza azul oscuro)
        'Toulouse':              '#0000FF',   # Azul (Toulouse FC utiliza azul)
        'Trabzonspor':           '#800000',   # Granate oscuro (Trabzonspor suele usar granate)
        'Tranmere':              '#E31B23',   # Rojo (según equipación histórica)
        'Trelleborg':            '#003399',   # Azul (color aproximado para equipos suecos)
        'Treviso':               '#0066CC',   # Azul (según equipación histórica)
        'Trikala':               '#E31B23',   # Rojo (color aproximado para clubes griegos)
        'Tromso':                '#0000FF',   # Azul (Tromsø IL utiliza azul)
        'Troyes':                '#E60000',   # Rojo (ESTAC Troyes utiliza rojo)
        'Twente':                '#FF0000',   # Rojo (FC Twente es conocido por el rojo)
        'Udinese':               '#000000',   # Negro (Udinese utiliza negro y verde; se elige el negro)
        'Ulm':                   '#006600',   # Verde (color representativo aproximado)
        'Unterhaching':          '#0000FF',   # Azul (SpVgg Unterhaching utiliza azul)
        'Uralan Elista':         '#E31B23',   # Rojo (según equipación histórica rusa)
        'Utrecht':               '#FF0000',   # Rojo (FC Utrecht utiliza rojo)
        'Vaestra':               '#003399',   # Azul (color aproximado)
        'Valence':               '#E60000',   # Rojo (Valencia CF utiliza rojo y naranja; se elige el rojo)
        'Valencia':              '#FF9B00',   # Naranja (oficial en el ejemplo)
        'Valerenga':             '#E31B23',   # Rojo (color aproximado para equipos noruegos)
        'Valladolid':            '#6600CC',   # Púrpura (Real Valladolid suele usar púrpura)
        'Vallecano':             '#FF0000',   # Rojo (Rayo Vallecano utiliza rojo y blanco)
        'Vanspor':               '#E60000',   # Rojo (color aproximado para clubes turcos)
        'Vejle':                 '#003399',   # Azul (Vejle Boldklub utiliza azul)
        'Venezia':               '#000000',   # Negro (Venezia FC tradicionalmente usa negro y verde; se elige el negro)
        'Verona':                '#8B0000',   # Rojo oscuro (Hellazzurra, color de la camiseta del Verona)
        'Viborg':                '#006600',   # Verde (Viborg FF utiliza verde)
        'Vicenza':               '#0000FF',   # Azul (Vicenza Calcio utiliza azul)
        'Viking':                '#0000FF',   # Azul (Viking FK utiliza azul)
        'Villarreal':            '#FEC131',   # Amarillo (Villarreal CF es conocido por su amarillo)
        'Vitesse':               '#0000FF',   # Azul (Vitesse utiliza azul)
        'Waalwijk':              '#E31B23',   # Rojo (color aproximado para el club)
        'Wacker Innsbruck':      '#003399',   # Azul (Wacker Innsbruck utiliza azul)
        'Walsall':               '#E31B23',   # Rojo (Walsall FC utiliza rojo)
        'Wasquehal':             '#003399',   # Azul (color aproximado)
        'Watford':               '#FBEE23',   # Amarillo (Watford FC utiliza amarillo y negro; se elige el amarillo)
        'Werder Bremen':         '#39B54A',   # Verde (Werder Bremen es conocido por su verde)
        'West Brom':             '#122F67',   # Azul oscuro (West Bromwich Albion utiliza azul oscuro)
        'West Ham':              '#7A263A',   # Granate (West Ham United utiliza granate)
        'Westerlo':              '#003399',   # Azul (K.V.C. Westerlo utiliza azul)
        'Widzew':                '#E31B23',   # Rojo (Widzew Łódź utiliza rojo)
        'Willem II':             '#FF0000',   # Rojo (Willem II suele usar rojo)
        'Wimbledon':             '#1C7ECF',   # Azul (Wimbledon utiliza azul)
        'Wisla':                 '#E60000',   # Rojo (Wisła Kraków utiliza rojo)
        'Wolfsburg':             '#009933',   # Verde (VW Wolfsburg utiliza verde)
        'Wolves':                '#FDB913',   # Amarillo (Wolverhampton Wanderers es conocido por su amarillo)
        'Wurzburger Kickers':     '#E31B23',   # Rojo (según equipación histórica)
        'Xanthi':                '#E60000',   # Rojo (club griego, se asigna rojo)
        'Zaragoza':              '#E60000',   # Rojo (Real Zaragoza utiliza rojo)
        'Zenit':                 '#004170',   # Azul (Zenit San Petersburgo utiliza azul)
        'Admira':                '#003399',   # Azul (color aproximado para equipos austriacos)
        'Ahlen':                 '#E31B23',   # Rojo (según equipación histórica)
        'Ancona':                '#003399',   # Azul (A.C. Ancona utiliza azul)
        'Angers':                '#003399',   # Azul (Angers SCO utiliza azul)
        'Antwerp':               '#E31B23',   # Rojo (Royal Antwerp suele usar rojo)
        'Athinaikos':            '#E31B23',   # Rojo (color aproximado para clubes griegos)
        'Aves':                  '#006600',   # Verde (CD Aves utiliza verde)
        'Beauvais':              '#003399',   # Azul (según equipación histórica)
        'Burnley':               '#99DDEE',   # Celeste (Burnley utiliza celeste y blanco)
        'Cittadella':            '#E31B23',   # Rojo (color aproximado)
        'Crotone':               '#E60000',   # Rojo (FC Crotone utiliza rojo)
        'Dunfermline':           '#0000FF',   # Azul (Dunfermline Athletic utiliza azul)
        'Ferrol':                '#E31B23',   # Rojo (según equipación histórica)
        'Foresta Suceava':       '#006600',   # Verde (color representativo aproximado)
        'Gaz Metan':             '#E31B23',   # Rojo (según equipación de clubes rumanos)
        'Giannina':              '#E60000',   # Rojo (PAS Giannina utiliza rojo)
        'Gillingham':            '#E31B23',   # Rojo (Gillingham FC utiliza rojo)
        'Groningen':             '#006600',   # Verde (FC Groningen utiliza verde)
        'Jaen':                  '#E31B23',   # Rojo (Real Jaén utiliza rojo)
        'Katowice':              '#E60000',   # Rojo (según equipación de clubes polacos)
        'Louvieroise':           '#003399',   # Azul (color aproximado)
        'Martigues':             '#E31B23',   # Rojo (según equipación histórica)
        'Midtjylland':           '#003399',   # Azul (FC Midtjylland utiliza azul)
        'Murcia':                '#FF0000',   # Rojo (Real Murcia utiliza rojo)
        'NAC Breda':             '#FF0000',   # Rojo (NAC Breda utiliza rojo)
        'Osnabruck':             '#003399',   # Azul (VfL Osnabrück utiliza azul)
        'Pacos Ferreira':        '#006600',   # Verde (color aproximado para equipos portugueses)
        'Preston':               '#E31B23',   # Rojo (Preston North End utiliza rojo)
        'Reutlingen':            '#003399',   # Azul (según equipación histórica)
        'Rizespor':              '#E60000',   # Rojo (equipo turco, se asigna rojo)
        'Roosendaal':            '#006600',   # Verde (color aproximado)
        'Saarbrucken':           '#003399',   # Azul (1. FC Saarbrücken utiliza azul)
        'Siena':                 '#800000',   # Granate (A.C. Siena utiliza granate)
        'Siirt Jet-PA':          '#E60000',   # Rojo (color aproximado para equipos turcos)
        'Slask':                 '#E60000',   # Rojo (Śląsk Wrocław utiliza rojo)
        'SonderjyskE':           '#006600',   # Verde (color aproximado para equipos daneses)
        'St Mirren':             '#003399',   # Azul (St Mirren utiliza azul)
        'U.Las Palmas':          '#FFA500',   # Naranja (similar a Las Palmas)
        'Yozgatspor':            '#E60000',   # Rojo (color aproximado para equipos turcos)
        'Djurgarden':            '#0000FF',   # Azul (Djurgårdens IF utiliza azul)
        'FC Moskva':             '#E31B23',   # Rojo (color representativo aproximado)
        'Lyn Oslo':              '#0000FF',   # Azul (Lyn Oslo utiliza azul)
        'Malmoe':                '#006600',   # Verde (Malmö FF utiliza verde)
        'Sogndal':               '#003399',   # Azul (color aproximado)
        'Sokol Saratov':         '#E31B23',   # Rojo (según equipación histórica)
        'Stromsgodset':          '#006600',   # Verde (Stromsgodset IF utiliza verde)
        'Akratitos':             '#E31B23',   # Rojo (color aproximado para equipos griegos)
        'Babelsberg':            '#003399',   # Azul (color representativo aproximado)
        'Burgos':                '#E31B23',   # Rojo (Burgos CF utiliza rojo)
        'Como':                  '#0000FF',   # Azul (Como 1907 utiliza azul)
        'Diyarbakirspor':        '#E60000',   # Rojo (equipo turco, se asigna rojo)
        'Egaleo':                '#006600',   # Verde (color aproximado para equipos griegos)
        'Grenoble':              '#E60000',   # Rojo (Grenoble Foot utiliza rojo)
        'Istres':                '#003399',   # Azul (según equipación histórica)
        'Klagenfurt':            '#0000FF',   # Azul (FC Kärnten/agrupaciones austriacas suelen usar azul)
        'KSZO':                  '#E31B23',   # Rojo (color aproximado para equipos polacos)
        'Livingston':            '#003399',   # Azul (Livingston FC utiliza azul)
        'Malatyaspor':           '#E60000',   # Rojo (Malatyaspor utiliza rojo)
        'Messina':               '#E31B23',   # Rojo (según equipación histórica)
        'Millwall':              '#003399',   # Azul (Millwall utiliza azul oscuro)
        'Modena':                '#0000FF',   # Azul (Modena FC utiliza azul)
        'Molenbeek':             '#E31B23',   # Rojo (color aproximado para equipos belgas)
        'MyPa':                  '#006600',   # Verde (MyPa utiliza verde)
        'Palermo':               '#E31B23',   # Rojo (Palermo FC utiliza rojo)
        'Poli Ejido':            '#E31B23',   # Rojo (según equipación histórica)
        'Radomsko':             '#E60000',   # Rojo (color aproximado para equipos polacos)
        'Rotherham':             '#E31B23',   # Rojo (Rotherham United utiliza rojo)
        'Schweinfurt':           '#003399',   # Azul (color aproximado)
        'Sportul':               '#E31B23',   # Rojo (según equipación histórica rumana)
        'Tarragona':             '#E60000',   # Rojo (Tarragona FC utiliza rojo)
        'UM Timisoara':          '#E31B23',   # Rojo (UM Timișoara utiliza rojo)
        'Union Berlin':          '#E60000',   # Rojo (Union Berlin utiliza rojo)
        'Varzim':                '#006600',   # Verde (color aproximado para clubes portugueses)
        'Xerez':                 '#E31B23',   # Rojo (Xerez CD utiliza rojo)
        'Kalmar':                '#006600',   # Verde (Kalmar FF utiliza verde)
        'Landskrona':            '#0000FF',   # Azul (color aproximado)
        'Shinnik Jaroslawl':     '#E31B23',   # Rojo (equipo ruso, se asigna rojo)
        'Tampere':               '#003399',   # Azul (color aproximado para equipos finlandeses)
        'Academica':             '#006600',   # Verde (Académica de Coimbra utiliza verde)
        'Almeria':               '#E60000',   # Rojo (UD Almería utiliza rojo)
        'Ascoli':                '#0000FF',   # Azul (Ascoli Calcio utiliza azul)
        'Bergen':                '#003399',   # Azul (color representativo aproximado para clubes noruegos de Bergen)
        'Braunschweig':          '#E31B23',   # Rojo (Eintracht Braunschweig utiliza rojo)
        'Brighton':              '#00529F',   # Azul (Brighton & Hove Albion utiliza azul y blanco)
        'Burghausen':            '#E31B23',   # Rojo (SV Wacker Burghausen utiliza rojo)
        'Catania':               '#E60000',   # Rojo (Catania FC utiliza rojo)
        'Clermont':              '#003399',   # Azul (Clermont Foot utiliza azul)
        'Ein Trier':             '#E31B23',   # Rojo (color aproximado para equipos alemanes menores)
        'Elazigspor':            '#E60000',   # Rojo (equipo turco, se asigna rojo)
        'Excelsior':             '#0066CC',   # Azul (Excelsior utiliza azul)
        'Jaworzno':              '#E31B23',   # Rojo (color aproximado para equipos polacos)
        'Kalithea':              '#003399',   # Azul (color aproximado para clubes griegos)
        'Koge':                  '#006600',   # Verde (Køge Boldklub utiliza verde)
        'Leixoes':               '#003399',   # Azul (Leixões SC utiliza azul)
        'Livorno':               '#0000FF',   # Azul (Livorno utiliza azul)
        'Lubeck':                '#003399',   # Azul (color aproximado para equipos alemanes)
        'Moreirense':            '#006600',   # Verde (Moreirense FC utiliza verde)
        'Nacional':              '#FF0000',   # Rojo (CD Nacional suele usar rojo)
        'Nordsjaelland':         '#006600',   # Verde (FC Nordsjælland utiliza verde)
        'Partick':               '#0000FF',   # Azul (Partick Thistle utiliza azul)
        'Pasching':              '#E31B23',   # Rojo (color aproximado para equipos austriacos)
        'Reading':               '#0000FF',   # Azul (Reading FC utiliza azul)
        'Reims':                 '#E60000',   # Rojo (Stade de Reims utiliza rojo)
        'Stoke':                 '#E31B23',   # Rojo (Stoke City utiliza rojo)
        'Terrassa':              '#E60000',   # Rojo (color aproximado para equipos españoles menores)
        'Timisoara':             '#E31B23',   # Rojo (FC Politehnica Timișoara utiliza rojo)
        'Triestina':             '#0000FF',   # Azul (US Triestina utiliza azul)
        'UTA Arad':              '#E31B23',   # Rojo (color representativo aproximado)
        'Zwolle':                '#006600',   # Verde (PEC Zwolle utiliza verde)
        'Aalesund':              '#0000FF',   # Azul (Aalesunds FK utiliza azul)
        'Enkoeping':             '#003399',   # Azul (color aproximado para equipos suecos)
        'Oester':                '#006600',   # Verde (color aproximado)
        'Rubin Kazan':           '#E60000',   # Rojo (Rubin Kazán utiliza rojo)
        'Torpedo Metallurg ZIL': '#E31B23',   # Rojo (color aproximado para equipos rusos)
        'A. Sebatspor':          '#E60000',   # Rojo (equipo turco, se asigna rojo)
        'Albinoleffe':           '#003399',   # Azul (Albinoleffe utiliza azul)
        'Algeciras':             '#E31B23',   # Rojo (color aproximado)
        'Avellino':              '#E60000',   # Rojo (Avellino utiliza rojo)
        'Besancon':              '#003399',   # Azul (color aproximado para equipos franceses menores)
        'Cadiz':                 '#FFFF00',   # Amarillo (Cádiz CF utiliza amarillo y azul; se elige el amarillo)
        'Cardiff':               '#1C1C1C',   # Negro (Cardiff City utiliza negro y azul; se elige el negro)
        'Cercle Brugge':         '#0000FF',   # Azul (Cercle Brugge utiliza azul)
        'Chalkidona':            '#E31B23',   # Rojo (color aproximado para equipos griegos)
        'Ciudad de Murcia':      '#E60000',   # Rojo (Real Murcia y similares utilizan rojo)
        'Crisul Oradea':         '#006600',   # Verde (color aproximado para equipos rumanos)
        'Den Haag':              '#0066CC',   # Azul (ADO Den Haag utiliza azul)
        'Erzgebirge Aue':        '#E31B23',   # Rojo (Erzgebirge Aue utiliza rojo)
        'Frem':                  '#003399',   # Azul (color aproximado para equipos alemanes menores)
        'Gornik Leczna':         '#E60000',   # Rojo (color aproximado para equipos polacos)
        'Heusden Zolder':        '#003399',   # Azul (color representativo aproximado)
        'Konyaspor':             '#E60000',   # Rojo (Konyaspor utiliza rojo)
        'Malaga B':              '#0000FF',   # Azul (equipo filial, se asigna el mismo azul que el principal)
        'Mattersburg':           '#003399',   # Azul (color aproximado para equipos austriacos)
        'Mazowiecki':            '#E60000',   # Rojo (color aproximado para equipos polacos)
        'Polkowice':             '#006600',   # Verde (color aproximado)
        'Quevilly Rouen':        '#E31B23',   # Rojo (color aproximado para equipos franceses)
        'Regensburg':            '#003399',   # Azul (SSV Jahn Regensburg utiliza azul)
        'Unirea Alba Iulia':     '#E31B23',   # Rojo (color aproximado para equipos rumanos)
        'Volendam':              '#FF0000',   # Rojo (FC Volendam utiliza rojo)
        'Wigan':                 '#E31B23',   # Rojo (Wigan Athletic utiliza rojo)
        # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
        # La siguiente parte abarca clubes de divisiones y países menos “mediáticos”.
        'Allianssi':             '#006600',
        'Amkar Perm':            '#E60000',
        'Fredrikstad':           '#003399',
        'Ham-Kam':               '#006600',
        'Kuban':                 '#E60000',
        'Ankaraspor':            '#E60000',
        'Arezzo':                '#003399',
        'Brest':                 '#003399',
        'Catanzaro':             '#E31B23',
        'CFR Cluj':              '#006600',
        'Cracovia':              '#E60000',
        'Dijon':                 '#E60000',
        'Dresden':               '#003399',
        'Erfurt':                '#E31B23',
        'Ergotelis':            '#003399',
        'Essen':                 '#000000',
        'Estoril':               '#006600',
        'FC Brussels':           '#E60000',
        'Iasi':                  '#006600',
        'Inverness':             '#003399',
        'Kalamaria':             '#E31B23',
        'Kayserispor':           '#E60000',
        'Kerkyra':               '#003399',
        'Oostende':              '#003399',
        'Penafiel':              '#006600',
        'Plymouth Argyle':       '#000000',
        'Pontevedra':            '#006600',
        'Randers':               '#003399',
        'Sakaryaspor':           '#E60000',
        'Terek Grozny':          '#E60000',
        'Assyriska':             '#006600',
        'Gefle':                 '#003399',
        'Tomsk':                 '#E31B23',
        'Arka':                  '#E60000',
        'Atromitos':             '#003399',
        'Belchatow':             '#E60000',
        'Castellon':             '#E60000',
        'Cremonese':             '#0000FF',
        'Erciyesspor':           '#E60000',
        'Falkirk':               '#003399',
        'Heracles':              '#003399',
        'Hercules':              '#E31B23',
        'Horsens':               '#006600',
        'Hull':                  '#FF0000',
        'Jiul Petrosani':        '#E31B23',
        'Korona':                '#E60000',
        'Larisa':                '#E31B23',
        'Levadeiakos':           '#003399',
        'Lorca':                 '#E60000',
        'Luton':                 '#FDB913',
        'Manisaspor':            '#E60000',
        'Mantova':               '#003399',
        'Naval':                 '#006600',
        'Paderborn':             '#003399',
        'Pandurii':              '#E31B23',
        'Real Madrid B':         '#C4C4C4',
        'Rimini':                '#E60000',
        'Roeselare':             '#003399',
        'Sete':                  '#E31B23',
        'Siegen':                '#003399',
        'Sivasspor':             '#E60000',
        'Valenciennes':          '#E60000',
        'Vaslui':                '#E31B23',
        'Waregem':               '#003399',
        'Sandefjord':            '#006600',
        'Spartak Nalchik':       '#E60000',
        'Vladivostok':           '#003399',
        'Altach':                '#003399',
        'Atvidaberg':            '#006600',
        'Augsburg':              '#E60000',
        'Colchester':            '#003399',
        'CZ Jena':               '#E31B23',
        'Frosinone':             '#003399',
        'Gretna':                '#000000',
        'Koblenz':               '#003399',
        'Libourne':              '#E31B23',
        'Ponferradina':          '#006600',
        'Southend':              '#003399',
        'Spezia':                '#0000FF',
        'Tours':                 '#E60000',
        'Urziceni':              '#E31B23',
        'Vecindario':            '#006600',
        'Brommapojkarna':        '#006600',
        'FC Khimki':             '#E60000',
        'Asteras Tripolis':      '#003399',
        'Austria Kaernten':      '#003399',
        'Blackpool':             '#000000',
        'Boulogne':              '#003399',
        'Bristol City':          '#E31B23',
        'Buyuksehyr':            '#E60000',
        'Bytom':                 '#E60000',
        'Dender':                '#003399',
        'Gloria Buzau':          '#E31B23',
        'Granada 74':            '#E60000',
        'Grosseto':              '#003399',
        'Hacettepespor':         '#E60000',
        'Hoffenheim':            '#003399',
        'Jagiellonia':           '#E60000',
        'Kasimpasa':             '#E60000',
        'Mioveni':               '#E31B23',
        'Pisa':                  '#003399',
        'Scunthorpe':            '#E31B23',
        'Sevilla B':             '#CD212A',
        'Sosnowiec':             '#E60000',
        'Universitatea Cluj':    '#006600',
        'Veria':                 '#E31B23',
        'VVV Venlo':             '#FFCC00',
        'Wehen':                 '#003399',
        'Honka Espoo':           '#006600',
        'Ljungskile':            '#003399',
        'Alicante':              '#FF0000',
        'Doncaster':             '#E31B23',
        'Eskisehirspor':         '#E60000',
        'Frankfurt FSV':         '#003399',
        'Girona':                '#E60000',
        'Hamilton':              '#003399',
        'Huesca':                '#E60000',
        'Ingolstadt':            '#003399',
        'Kapfenberg':            '#003399',
        'Kortrijk':              '#E31B23',
        'Lechia':                '#006600',
        'Otopeni':               '#E31B23',
        'Panserraikos':          '#E31B23',
        'Panthrakikos':          '#E31B23',
        'Piast Gliwice':         '#E60000',
        'Queen of Sth':          '#003399',
        'Sassuolo':              '#0000FF',
        'Swansea':               '#FFFFFF',
        'Thrasyvoulos':          '#E31B23',
        'Trofense':              '#003399',
        'Tubize':                '#E31B23',
        'Vannes':                '#003399',
        'Inter Turku':           '#0000FF',
        'Lahti':                 '#006600',
        'Arles':                 '#E60000',
        'Cartagena':             '#E60000',
        'Curtea de Arges':       '#E31B23',
        'Fortuna Dusseldorf':    '#E31B23',
        'Gallipoli':             '#E60000',
        'HB Koge':               '#006600',
        'Olhanense':             '#E60000',
        'Padova':                '#0000FF',
        'Peterboro':             '#E31B23',
        'Real Union':            '#E60000',
        'Villarreal B':          '#FEC131',
        'Wiener Neustadt':       '#003399',
        'Honefoss':              '#006600',
        'Kongsvinger':           '#003399',
        'Mjaellby':              '#006600',
        'Novosibirsk':           '#E31B23',
        'TPS Turku':             '#006600',
        'Alcorcon':              '#E60000',
        'Barcelona B':           '#A50044',
        'Branesti':              '#E31B23',
        'Bucaspor':              '#E60000',
        'Eupen':                 '#003399',
        'Evian Thonon Gaillard': '#004170',
        'Granada':               '#E60000',
        'Karabukspor':           '#E60000',
        'Novara':                '#003399',
        'Portimonense':          '#006600',
        'Portogruaro':           '#003399',
        'Targu Mures':           '#E31B23',
        'Varese':                '#003399',
        'Volou':                 '#003399',
        'FC Krasnodar':          '#E60000',
        'Kuopio':                '#006600',
        'Sarpsborg':             '#006600',
        'Syrianska':             '#003399',
        'Volga':                 '#E31B23',
        'Alcoyano':              '#E60000',
        'Chiajna':               '#E31B23',
        'Feirense':              '#006600',
        'Guadalajara':           '#E60000',
        'Gubbio':                '#003399',
        'Juve Stabia':           '#E31B23',
        'Mersin Idman Yurdu':    '#E60000',
        'Nocerina':              '#E31B23',
        'Orduspor':              '#E60000',
        'Oud-Heverlee Leuven':   '#003399',
        'Podbeskidzie':          '#E60000',
        'Sabadell':              '#E60000',
        'Vointa Sibiu':          '#E31B23',
        'Doxa Dramas':           '#003399',
        'Panetolikos':           '#E31B23',
        'Jyvaeskylae':           '#006600',
        'Sandnes':               '#003399',
        'Aalen':                 '#E31B23',
        'Akhisar Belediyespor':  '#E60000',
        'Gazelec':               '#003399',
        'Lugo':                  '#006600',
        'Mirandes':              '#E60000',
        'Mordovia':              '#E31B23',
        'Platanias':             '#003399',
        'Pro Vercelli':          '#003399',
        'Ross County':           '#006600',
        'Sandhausen':            '#003399',
        'Turnu Severin':         '#E31B23',
        'Viitorul':              '#006600',
        'Virtus Lanciano':       '#E31B23',
        'Wolfsberg':             '#003399',
        'Mariehamn':             '#006600',
        'Arouca':                '#006600',
        'Botosani':              '#E31B23',
        'Bournemouth':           '#000000',
        'CA Bastia':             '#003399',
        'Carpi':                 '#E60000',
        'Corona Brasov':         '#E31B23',
        'Go Ahead Eagles':       '#003399',
        'Groedig':               '#003399',
        'Hodd':                  '#003399',
        'Kallonis':              '#E60000',
        'Latina':                '#003399',
        'Sageata':               '#E31B23',
        'Sverdlovsk':            '#E60000',
        'Trapani':               '#E31B23',
        'Vestsjaelland':         '#006600',
        'Yeovil':                '#E31B23',
        'Zawisza':               '#E60000',
        'Falkenbergs':           '#006600',
        'Rovaniemi':             '#003399',
        'Vaasa':                 '#006600',
        'Balikesirspor':         '#E60000',
        'Brentford':             '#E31B23',
        'Craiova':               '#E31B23',
        'Darmstadt':             '#003399',
        'Dordrecht':             '#006600',
        'Heidenheim':            '#E60000',
        'Hobro':                 '#003399',
        'Llagostera':            '#E60000',
        'Niki Volos':            '#E31B23',
        'Orleans':               '#003399',
        'RB Leipzig':            '#000000',
        'St Poelten':            '#003399',
        'Tula':                  '#E31B23',
        'Ufa':                   '#E60000',
        'Virtus Entella':        '#003399',
        'Mjondalen':             '#006600',
        'Seinajoki':             '#006600',
        'Ath Bilbao B':          '#DB001B',
        'Bourg Peronnas':        '#003399',
        'Milton Keynes Dons':    '#FFCC00',
        'Nieciecza':             '#E60000',
        'Paris FC':              '#004170',
        'Red Star':              '#E60000',
        'Tondela':               '#006600',
        'Uniao Madeira':         '#006600',
        'Voluntari':             '#E31B23',
        'Joenkoeping':           '#003399',
        'Ostersund':             '#006600',
        'Alanyaspor':            '#E60000',
        'Benevento':             '#E60000',
        'Burton':                '#E31B23',
        'Chaves':                '#006600',
        'Orenburg':              '#E60000',
        'Reus Deportiu':         '#E60000',
        'Spal':                  '#003399',
        'UCAM Murcia':           '#E60000',
        'Eskilstuna':            '#006600',
        'IK Sirius':             '#006600',
        'Kristiansund':          '#003399',
        'St. Gilloise':          '#003399',
        'Foggia':                '#E60000',
        'Helsingor':             '#003399',
        'Holstein Kiel':         '#003399',
        'Juventus Bucuresti':    '#000000',
        'Khabarovsk':            '#E60000',
        'Lamia':                 '#E31B23',
        'Leonesa':               '#E60000',
        'Sandecja Nowy Sacz':    '#E60000',
        'Sepsi':                 '#E31B23',
        'Tosno':                 '#E31B23',
        'Dalkurd':               '#003399',
        'Ilves Tampere':         '#006600',
        'Ranheim':               '#003399',
        'Beziers':               '#E60000',
        'Dunarea Calarasi':      '#E31B23',
        'Erzurum BB':            '#E60000',
        'FC Emmen':              '#006600',
        'Hartberg':              '#003399',
        'Hermannstadt':          '#E31B23',
        'Magdeburg':             '#003399',
        'Miedz Legnica':         '#E60000',
        'Rayo Majadahonda':      '#E60000',
        'Vendsyssel':            '#006600',
        'Yenisey':               '#E60000',
        'Chambly':               '#003399',
        'Chindia Targoviste':    '#E31B23',
        'Clinceni':              '#E31B23',
        'Famalicao':             '#006600',
        'Fuenlabrada':           '#E60000',
        'NFC Volos':             '#E31B23',
        'Pordenone':             '#003399',
        'Rakow':                 '#E60000',
        'Rodez':                 '#003399',
        'Sochi':                 '#E60000',
        'Tambov':                '#E60000',
        'Wattens':               '#003399',
        'Varbergs':              '#006600',
        'Dunkerque':             '#003399',
        'Hatayspor':             '#E60000',
        'Karagumruk':            '#E60000',
        'Pau FC':                '#003399',
        'Stal Mielec':           '#E60000',
        'Warta':                 '#E60000',
        'Wycombe':               '#003399',
        'Reggiana':              '#003399',
        'Degerfors':             '#006600',
        'Ad. Demirspor':         '#E60000',
        'Alessandria':           '#003399',
        'Amorebieta':            '#E31B23',
        'Giresunspor':           '#E60000',
        'Ibiza':                 '#FF0000',
        'Nizhny Novgorod':       '#E60000',
        'Radomiak':              '#E60000',
        'Seraing':               '#003399',
        'Sociedad B':            '#0066CC',
        'Vizela':                '#006600',
        'Jerv':                  '#003399',
        'Varnamo':               '#006600',
        'Andorra CF':            '#E60000',
        'Annecy':                '#003399',
        'Casa Pia':              '#006600',
        'Sudtirol':              '#000000',
        'Umraniyespor':          '#E60000',
        'Almere City':           '#003399',
        'Baltika':               '#E60000',
        'BW Linz':               '#003399',
        'Concarneau':            '#006600',
        'Eldense':               '#E60000',
        'Elversberg':            '#003399',
        'Feralpisalo':           '#E60000',
        'Hvidovre':              '#006600',
        'Kifisias':              '#003399',
        'Lecco':                 '#003399',
        'Pendikspor':            '#E60000',
        'Plymouth':              '#000000',
        'Puszcza Niepolomice':   '#E60000',
        'KFUM Oslo':             '#003399',
        'Vaesteras':             '#006600',
        'Akron Togliatti':       '#E60000',
        'AVS':                   '#E60000',
        'Bodrumspor':            '#E60000',
        'Carrarese':             '#003399',
        'Corvinul Hunedoara':    '#E31B23',
        'Dynamo Makhachkala':    '#E60000',
        'Eyupspor':              '#E60000',
        'Motor Lublin':          '#E60000',
        'Oxford':                '#003399',
        'Preussen Munster':      '#003399',
        'Unirea Slobozia':       '#E31B23'
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