# client.py

# Импорты
import requests


def get_car_price():
    """Отправка POST-запроса на сервер с параметрами
    для предсказания стоимости автомобиля.
    Year - год выпуска
    Driven(km) - пробег в киллометрах
    Transmission - тип трансмиссии: 0 - механика, 1 - автомат
    Engine(CC) - рабочий объем двигателя в см.куб
    Power(hp) - мощность двигателя в лошадиных силах
    Seats - количество сидений"""

    r = requests.post('http://0.0.0.0:5000/car_price',
                      json={'Year': 2009, 'Driven(km)': 300000,
                            'Transmission': 1, 'Engine(cc)': 1000,
                            'Power(hp)': 75, 'Seats': 5})
    return r.text


if __name__ == '__main__':
    print(get_car_price())
