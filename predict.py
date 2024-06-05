import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

loaded_model = tf.keras.models.load_model('powerlifting_model.h5')

data = pd.read_csv('openpowerlifting.csv')
data = data[['Sex', 'Age', 'BodyweightKg', 'TotalKg']].dropna()
features = data[['Sex', 'Age', 'BodyweightKg']]
target = data['TotalKg']

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['Age', 'BodyweightKg']),
        ('cat', OneHotEncoder(), ['Sex'])
    ]
)
X_test_transformed = preprocessor.fit_transform(X_test)

predictions = loaded_model.predict(X_test_transformed)
predictions_df = pd.DataFrame(predictions, columns=['predicted_TotalKg'])
predictions_df.to_csv('powerlifting_test_predictions.csv', index=False)
