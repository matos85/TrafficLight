import time
import random
from threading import Thread
from queue import Queue  # Изменено с threading на queue

# Класс события, используемого для передачи информации между светофорами.
class TrafficEvent:
    def __init__(self, id_sender, traffic_count):  # Изменено с init на __init__
        self.id_sender = id_sender  # Идентификатор отправителя светофора
        self.traffic_count = traffic_count  # Количество ожидающих автомобилей

# Класс светофора
class TrafficLight(Thread):
    def __init__(self, light_id):  # Изменено с init на __init__
        super().__init__()  # Исправлено на правильный вызов super
        self.light_id = light_id  # Идентификатор светофора
        self.traffic_light_state = 'красный'  # Начальное состояние светофора
        self.event_queue = Queue()  # Очередь для обработки событий
        self.event_interval = 5  # Интервал опроса в секундах
        self.current_traffic_count = 0  # Текущее количество автомобилей
        self.is_running = True  # Флаг для управления работой потока

    # Метод для изменения состояния светофора
    def change_state(self, new_state):
        self.traffic_light_state = new_state  # Изменяем состояние светофора
        print(f"Светофор {self.light_id} изменил состояние на {self.traffic_light_state}\n")

    # Метод для отправки события другим светофорам
    def send_event(self, traffic_count):
        event = TrafficEvent(self.light_id, traffic_count)  # Создание события
        for light in traffic_lights:
            if light.light_id != self.light_id:  # Не отправляем событие самому себе
                light.event_queue.put(event)  # Помещаем событие в очередь

    # Основной метод выполнения потока
    def run(self):
        while self.is_running:
            time.sleep(self.event_interval)  # Ожидание интервала опроса
            self.current_traffic_count = random.randint(0, 10)  # Имитация количества автомобилей
            self.send_event(self.current_traffic_count)  # Отправка события
            self.process_events()  # Обработка полученных событий

    # Метод для обработки событий из очереди
    def process_events(self):
        while not self.event_queue.empty():  # Пока есть события в очереди
            event = self.event_queue.get()  # Получаем событие из очереди
            print(f"Светофор {self.light_id} получил событие от {event.id_sender}: {event.traffic_count}")
            # Изменение состояния в зависимости от количества автомобилей
            if event.traffic_count > 5:
                self.change_state('зелёный')  # Если много машин - зеленый свет
                time.sleep(10)  # Задержка для зеленого света
                self.change_state('жёлтый')  # Переход на желтый свет
                time.sleep(2)  # Задержка для желтого света
                self.change_state('красный')  # Переход на красный свет
            else:
                self.change_state('красный')  # Если мало машин - остаемся на красном


# Создаем несколько светофоров
traffic_lights = [
    TrafficLight(light_id=1),
    TrafficLight(light_id=2),
    TrafficLight(light_id=3),
    TrafficLight(light_id=4),
]

# Запускаем светофоры
for light in traffic_lights:
    light.start()

# Имитация работы светоферов на протяжении 30 секунд
time.sleep(30)

# Остановка всех светофоров
for light in traffic_lights:
    light.is_running = False  # Устанавливаем флаг остановки
    light.join()  # Ожидаем завершения потока

print("Моделирование работы светофоров завершено.")