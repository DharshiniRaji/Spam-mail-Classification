import numpy as np
import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def train_model():
    spam = pd.read_csv("C:\DATA SCIENCE\mail_data.csv")
    data = spam.where(pd.notnull(spam), '')
    data.loc[data['Category']=='spam','Category',]=0
    data.loc[data['Category']=='ham','Category',]=1
    x = data['Message']
    y = data['Category']

    # Convert categorical labels to numerical values
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    # Train-test split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=3)

    # Feature extraction
    feature_extraction=TfidfVectorizer(min_df=1,stop_words='english',lowercase=True)
    x_train_features=feature_extraction.fit_transform(x_train)
    x_test_features=feature_extraction.transform(x_test)

    y_train=y_train.astype('int')
    y_test=y_test.astype('int')
    # Train Logistic Regression model
    lg_model = LogisticRegression(C=100, solver='liblinear')
    lg_model.fit(x_train_features, y_train)

    return feature_extraction, lg_model, label_encoder



def predict_email_type(input_mail, feature_extraction, lg_model):
    input_data = feature_extraction.transform([input_mail])
    prediction = lg_model.predict(input_data)
    return prediction
