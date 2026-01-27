import pika
import json
import numpy as np
import cv2
import requests
import time

# Funkcja wykonująca analizę (Twoja stara logika)
def process_image(url):
    print(f" [...] Pobieram obraz: {url}")
    try:
        response = requests.get(url, stream=True).raw
        image_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # Wykrywanie
        rects, weights = hog.detectMultiScale(image, winStride=(4,4), padding=(8,8), scale=1.05)
        
        # Rysowanie prostokątów (opcjonalne w workerze, chyba że zapisujesz plik)
        # for (x, y, w, h) in rects:
        #    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
        return len(rects)
    except Exception as e:
        print(f" [!] Błąd przetwarzania obrazu: {e}")
        return None

# Funkcja callback - uruchamiana, gdy przyjdzie wiadomość z RabbitMQ
def callback(ch, method, properties, body):
    data = json.loads(body)
    image_url = data['image_url']
    
    print(f" [x] Odebrano zadanie dla: {image_url}")
    
    # Symulacja ciężkiej pracy (analiza)
    num_people = process_image(image_url)
    
    if num_people is not None:
        print(f" [V] SUKCES: Wykryto osób: {num_people}")
        # TUTAJ w przyszłości dodasz kod: zapisz_wynik_do_bazy(image_url, num_people)
    else:
        print(f" [!] NIEPOWODZENIE dla: {image_url}")

    # Potwierdzenie wykonania zadania (RabbitMQ usunie je z kolejki dopiero teraz)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    # Konfiguracja połączenia
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='image_analysis_queue')

    # QOS: Worker bierze tylko 1 zadanie na raz (nie bierze nowych, dopóki nie skończy obecnego)
    channel.basic_qos(prefetch_count=1)
    
    channel.basic_consume(queue='image_analysis_queue', on_message_callback=callback)

    print(' [*] Worker uruchomiony. Czekam na zadania. Naciśnij CTRL+C aby wyjść.')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        start_worker()
    except KeyboardInterrupt:
        print('Przerwano działanie workera')