import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tensorflow as tf

data = pd.read_csv('./openpowerlifting2.csv')

data = data[['Sex', 'Age', 'BodyweightKg', 'TotalKg']].dropna()
data['Age'] = pd.to_numeric(data['Age'], errors='coerce')
data['BodyweightKg'] = pd.to_numeric(data['BodyweightKg'], errors='coerce')
data['TotalKg'] = pd.to_numeric(data['TotalKg'], errors='coerce')
features = data[['Sex', 'Age', 'BodyweightKg']]
target = data['TotalKg']

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['Age', 'BodyweightKg']),
        ('cat', OneHotEncoder(), ['Sex'])
    ],
)

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', Sequential([
        Dense(64, activation='relu', input_dim=4),
        Dense(64, activation='relu'),
        Dense(1)
    ]))
])

pipeline['model'].compile(optimizer='adam', loss='mse', metrics=['mae'])

X_train_excluded = X_train.iloc[1:]
y_train_excluded = y_train.iloc[1:]

pipeline.fit(X_train_excluded, y_train_excluded, model__epochs=int(10), model__validation_split=0.1)

pipeline['model'].save('powerlifting_model.h5')
