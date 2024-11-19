import random
import csv
import os
from pydub import AudioSegment
from pydub.playback import play

# Abrimos archivo de ruido blanco
white_noise = AudioSegment.from_file("white_noise_1s.wav")  

# Reproducimos el sonido a una distancia sin repetición
def play_sound_for_distance(distances):
    actual_distance = distances.pop(0)  # Toma la primera distancia disponible y la saca de la lista
    print(f"Colocá la fuente a la distancia de {actual_distance} metros.")
    
    # Esperar a que se presione Enter para reproducir el sonido
    input("Presioná Enter cuando la fuente esté colocada en la distancia indicada...")
    
    print(f"Reproduciendo sonido para la distancia de {actual_distance} metros.")
    play(white_noise)  
    return actual_distance

# Verificar si el participante ya ha realizado el experimento
def participant_exists(participant_id, file_name):
    if os.path.isfile(file_name):
        with open(file_name, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Participant ID'] == participant_id:
                    return True
    return False

# Guardamos en CSV
def save_to_csv(participant_id, trials_data):
    file_name = 'percepcion_a_distancia.csv'
    
    # Si aún no existe, crear el archivo CSV y escribir el encabezado
    file_exists = os.path.isfile(file_name)
    with open(file_name, 'a', newline='') as csvfile:
        fieldnames = ['Participant ID', 'Trial', 'Actual Distance (m)', 'Estimated Distance (m)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()  # Solo escribir el encabezado si el archivo es nuevo
            
        # Guardar los datos de la sesión
        for trial, data in enumerate(trials_data, 1):
            writer.writerow({
                'Participant ID': participant_id,
                'Trial': trial,
                'Actual Distance (m)': data[0],
                'Estimated Distance (m)': data[1]
            })

# Pedimos datos del participante
participant_id = input("Ingresá el ID del participante: ")

# Verificar si el participante ya ha realizado el experimento
if participant_exists(participant_id, 'percepcion_a_distancia.csv'):
    print(f"El participante {participant_id} ya ha realizado el experimento. Ingrese otro número")
else:
    # Configuramos las distancias y las aleatorizamos
    distances = [1, 2, 3, 4, 5, 6]
    random.shuffle(distances)  # Aleatoriza las distancias

    # Número de pruebas
    num_trials = 6

    # Lista para almacenar los resultados
    trials_data = []

    # Iniciamos experimento
    for trial in range(num_trials):
        actual_distance = play_sound_for_distance(distances)
        estimated_distance = input(f"Ingresá la distancia estimada por el participante (en metros): ")
        
        # Almacenamos los datos
        trials_data.append((actual_distance, estimated_distance))

    # Guardamos los datos en un archivo CSV
    save_to_csv(participant_id, trials_data)

    print(f"Los datos del experimento con el participante {participant_id} fueron guardados.")
4