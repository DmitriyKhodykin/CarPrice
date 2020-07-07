# carprice.py

# Установить либы:
# pip install -r requirements.txt

# Импорты
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor

# Установки
RANDOM_SEED = 42
VERSION = 11
VAL_SIZE = 0.33
N_FOLDS = 5
ITERATIONS = 2000
LR = 0.05


class CatModel:
    """Возвращает обученную модель Cat Boost Regressor на тестовых данных"""

    def __init__(self, df_input):
        self.df_input = df_input

    def data_prep(self):
        """Подготовка данных для модели"""
        df_output = self.df_input.copy()
        df_output['Transmission'] = df_output['Transmission'].apply(lambda x: 1 if x == 'Automatic' else 0)

        df_output['Engine'] = df_output['Engine'].apply(lambda x: str(x)[0:-3])
        df_output['Engine'] = df_output['Engine'].apply(lambda x: 1200 if x == '' else x).astype(int)

        df_output['Power'] = df_output['Power'].fillna('75 bhp')
        df_output['Power'] = df_output['Power'].apply(lambda x: '75 bhp' if x == 'null bhp' else x)
        df_output['Power'] = df_output['Power'].apply(lambda x: str(x)[0:-4]).astype(float).astype(int)

        df_output['Seats'] = df_output['Seats'].fillna(5).astype(int)

        df_output.drop([
            'Unnamed: 0',
            'Name',
            'Location',
            'Fuel_Type',
            'Owner_Type',
            'Mileage',
            'New_Price'],
            axis=1,
            inplace=True)

        return df_output

    def train_model(self):
        """Обучает модель регрессии"""
        train_preproc = self.data_prep()
        # Разделение датасета на тренировочные и тестовые наборы
        X = train_preproc.drop(['Price'], axis=1,)
        y = train_preproc['Price'].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=VAL_SIZE, shuffle=True,
            random_state=RANDOM_SEED
        )

        # Указание категориальных признаков
        cat_features_ids = np.where(X_train.apply(pd.Series.nunique) < 3000)[0].tolist()

        # Обучение модели
        model = CatBoostRegressor(
            iterations=ITERATIONS, learning_rate=LR, random_seed=RANDOM_SEED,
            eval_metric='MAPE', custom_metric=['R2', 'MAE']
        )

        model.fit(
            X_train, y_train, cat_features=cat_features_ids,
            eval_set=(X_test, y_test), verbose_eval=100, use_best_model=True, plot=True
        )

        return model


# Запуск, обучения и сериализация обученной модели
if __name__ == '__main__':
    model = CatModel(pd.read_csv('train-data.csv')).train_model()
    with open('pickled_model.pkl', 'wb') as output:
        pickle.dump(model, output)
