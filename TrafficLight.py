import time
import threading

class TrafficLight:
    def __init__(self, id):
        self.id = id  # Уникальный идентификатор светофора
        self.timer = None  # Таймер для отправки событий
        self.event_queue = []  # Очередь событий для обработки

    def handle_event(self, event):
        # Обработка событий из очереди
        print(f"Traffic light {self.id} handling event: {event}")

    def send_event(self, event, target_id):
        # Отправка события другому светофору
        print(f"Traffic light {self.id} sending event to traffic light {target_id}: {event}")

    def update_state(self, state_info):
        # Обновление состояния светофора на основе данных о текущей ситуации
        print(f"Traffic light {self.id} updating state based on info: {state_info}")

    def start_timer(self, duration, event):
        # Запуск таймера для отправки события после заданной продолжительности
        print(f"Traffic light {self.id} starting timer for event: {event} after {duration} seconds")

        if self.timer:
            self.timer.cancel()  # Отменяем предыдущий таймер, если он был запущен

        self.timer = threading.Timer(duration, self.send_event, args=(event, self.id))
        self.timer.start()

    def run(self):
        while True:
            if self.event_queue:
                event = self.event_queue.pop(0)
                self.handle_event(event)

            time.sleep(0.1)  # Пауза для предотвращения блокировки потока

def main():
    # Создание объектов светофоров
    traffic_lights = [TrafficLight(id) for id in range(4)]

    # Запуск потоков для каждого светофора
    threads = [threading.Thread(target=tl.run) for tl in traffic_lights]
    for thread in threads:
        thread.start()

if __name__ == "__main__":
    main()

