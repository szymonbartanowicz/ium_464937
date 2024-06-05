import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tensorflow as tf
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, mean_squared_error
from math import sqrt
import mlflow


mlflow.set_tracking_uri("http://localhost:5000")


def main():
    data = pd.read_csv('../openpowerlifting.csv')
    data = data[['Sex', 'Age', 'BodyweightKg', 'TotalKg']].dropna()
    data['Age'] = pd.to_numeric(data['Age'], errors='coerce')
    data['BodyweightKg'] = pd.to_numeric(data['BodyweightKg'], errors='coerce')
    data['TotalKg'] = pd.to_numeric(data['TotalKg'], errors='coerce')
    features = data[['Sex', 'Age', 'BodyweightKg']]
    target = data['TotalKg']
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    with mlflow.start_run() as run:
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), ['Age', 'BodyweightKg']),
                ('cat', OneHotEncoder(), ['Sex'])
            ],
        )

        model = Sequential([
            Dense(64, activation='relu', input_dim=5),
            Dense(64, activation='relu'),
            Dense(1)
        ])

        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model)
        ])

        X_train_excluded = X_train.iloc[1:]
        y_train_excluded = y_train.iloc[1:]
        pipeline.fit(X_train_excluded, y_train_excluded, model__epochs=int(sys.argv[1]), model__validation_split=0.1)
        pipeline['model'].save('powerlifting_model.h5')
        loaded_model = tf.keras.models.load_model('powerlifting_model.h5')

        test_data = pd.read_csv('openpowerlifting.csv')
        test_data = test_data[['Sex', 'Age', 'BodyweightKg', 'TotalKg']].dropna()
        test_data['Age'] = pd.to_numeric(test_data['Age'], errors='coerce')
        test_data['BodyweightKg'] = pd.to_numeric(test_data['BodyweightKg'], errors='coerce')
        test_data['TotalKg'] = pd.to_numeric(test_data['TotalKg'], errors='coerce')
        test_features = test_data[['Sex', 'Age', 'BodyweightKg']]
        test_target = test_data['TotalKg']

        X_test_transformed = preprocessor.transform(test_features)
        predictions = loaded_model.predict(X_test_transformed)
        predictions_df = pd.DataFrame(predictions, columns=['predicted_TotalKg'])
        predictions_df['actual_TotalKg'] = test_target.reset_index(drop=True)
        predictions_df.to_csv('powerlifting_test_predictions.csv', index=False)

        data = pd.read_csv('powerlifting_test_predictions.csv')
        y_pred = data['predicted_TotalKg']
        y_test = data['actual_TotalKg']
        rmse = sqrt(mean_squared_error(y_test, y_pred))


        mlflow.log_param("epochs", int(sys.argv[1]))
        mlflow.log_metric("rmse", rmse)


if __name__ == '__main__':
    main()