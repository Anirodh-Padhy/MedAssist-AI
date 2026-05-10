import numpy as np

from sklearn.linear_model import LogisticRegression

# =========================================================
# DIABETES MODEL
# =========================================================

# Features:
# [glucose, blood_pressure, bmi, age]

X_diabetes = np.array([
    [85, 70, 22, 25],
    [90, 72, 24, 30],
    [120, 80, 28, 40],
    [150, 90, 35, 50],
    [180, 95, 38, 55],
    [200, 100, 42, 60]
])

y_diabetes = np.array([
    0,
    0,
    0,
    1,
    1,
    1
])

diabetes_model = LogisticRegression()

diabetes_model.fit(
    X_diabetes,
    y_diabetes
)

# =========================================================
# HEART DISEASE MODEL
# =========================================================

# Features:
# [cholesterol, blood_pressure, bmi, age]

X_heart = np.array([
    [150, 70, 22, 25],
    [170, 75, 24, 30],
    [190, 85, 28, 40],
    [220, 95, 34, 50],
    [250, 100, 38, 60],
    [280, 110, 42, 65]
])

y_heart = np.array([
    0,
    0,
    0,
    1,
    1,
    1
])

heart_model = LogisticRegression()

heart_model.fit(
    X_heart,
    y_heart
)

# =========================================================
# DIABETES PREDICTION
# =========================================================

def predict_diabetes(
    glucose,
    blood_pressure,
    bmi,
    age
):

    data = np.array([
        [
            glucose,
            blood_pressure,
            bmi,
            age
        ]
    ])

    prediction = diabetes_model.predict(
        data
    )[0]

    probability = diabetes_model.predict_proba(
        data
    )[0][1]

    return prediction, probability

# =========================================================
# HEART DISEASE PREDICTION
# =========================================================

def predict_heart_disease(
    cholesterol,
    blood_pressure,
    bmi,
    age
):

    data = np.array([
        [
            cholesterol,
            blood_pressure,
            bmi,
            age
        ]
    ])

    prediction = heart_model.predict(
        data
    )[0]

    probability = heart_model.predict_proba(
        data
    )[0][1]

    return prediction, probability

# =========================================================
# HEALTH SCORE
# =========================================================

def calculate_health_score(
    diabetes_risk,
    heart_risk
):

    avg_risk = (
        diabetes_risk + heart_risk
    ) / 2

    score = 100 - avg_risk

    return round(score, 2)