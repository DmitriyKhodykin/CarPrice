# Car Price Prediction
## Предсказание стоимости автомобиля в USD в зависимости от года выпуска, пробега в км, типа трансмиссии, мощности и объема двигателя, а также и количества сидений

### 1. Данные для модели машинного обучения
https://www.kaggle.com/avikasliwal/used-cars-price-prediction

* Вид исходных данных:

 ```
    index | Year   | Kilometers_Driven    | Transmission   | Engine  | Power     | Seats   | Price  | ...
    ------------------------------------------------------------------------------------------------------
    0     | 2014   | 40929                | Manual         | 998 CC  | 58.2 bhp  | 4.0     | 1.75   | ...
    1     | 2016   | 54493                | Automatic      | 796 CC  | 47.3 bhp  | 5.0     | 12.5   | ...
    2     | 2017   | 34000                | Manual         | 2393 CC | 147.8 bhp | 7.0     | 4.5    | ...
 ```

### 2. Подготовка данных и построение модели
Предобработка данных и построение модели реализовано в `carprice.py` в директории `model`

* Гиперпараметры модели:

```
RANDOM_SEED = 42
VERSION = 11
VAL_SIZE = 0.33
N_FOLDS = 5
ITERATIONS = 2000
LR = 0.05
```

* Обучение модели:

```
  model = CatBoostRegressor(
      iterations=ITERATIONS, 
      learning_rate=LR, 
      random_seed=RANDOM_SEED,
      eval_metric='MAPE', 
      custom_metric=['R2', 'MAE']
      )
  
  model.fit(
      X_train, y_train, 
      cat_features=cat_features_ids,
      eval_set=(X_test, y_test), 
      verbose_eval=100, 
      use_best_model=True, 
      plot=True
      )
```

* Оценка модели (MAPE - Mean Absolute Percent Error):

```
bestTest = 0.222457398
bestIteration = 1861
```

* Сериализация модели:

Сериализация модели реализована с помощью модуля `pickle`, сериализованная модель `pickled_model.pkl` находится в директории `model` 

### 3. Развертка сервиса в продакшн на виртуальном сервере

Конфигурация развертки предобученной модели машинного обучения – Car Price Prediction (CatBoostReg): nginx + uwsgi + Flask на виртуальном сервере под управлением Ubuntu 20.04. Файлы конфигурации в директориях `home/carprice` и `/etc`

Принципиальная схема конфигурации:

![](/service/carprice_service.png)

### 4. Использование сервиса

`/carprice` - GET. Возвращает предсказание стоимости автомобиля в USD в зависимости от года выпуска, пробега в км, типа трансмиссии, мощности и объема двигателя, а также количества сидений

* Пример запроса:

```
import requests
import json


def get_car_price():
    """Отправка POST-запроса на сервер с параметрами
    для предсказания стоимости автомобиля.
    Year - год выпуска
    Driven(km) - пробег в киллометрах
    Transmission - тип трансмиссии: 0 - механика, 1 - автомат
    Engine(CC) - рабочий объем двигателя в см.куб
    Power(hp) - мощность двигателя в лошадиных силах
    Seats - количество сидений"""

    r = requests.request("GET", "http://0.0.0.0:80/carprice",
                         data='''{
                         "Year": 2011, 
                         "Driven(km)": 300000,
                         "Transmission": 1, 
                         "Engine(cc)": 1000,
                         "Power(hp)": 275, 
                         "Seats": 5
                         }''')
    return json.loads(r.text.encode('utf8'))
```

* Пример ответа:

```
{'Predict Car Price, USD': 18978.3}
```
