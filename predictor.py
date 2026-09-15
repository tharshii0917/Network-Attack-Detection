
import pandas as pd
import joblib

# Load trained model
model = joblib.load("cyber_attack_model.pkl")

# Load feature columns
feature_columns = joblib.load("feature_columns.pkl")


def calculate_risk(attack_probability):

    risk_score = round(attack_probability * 100, 2)

    if risk_score <= 30:
        risk_level = "LOW"
    elif risk_score <= 60:
        risk_level = "MEDIUM"
    elif risk_score <= 80:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    return risk_score, risk_level


def forecast_risk(risk_history):

    if len(risk_history) < 2:
        return {
            "forecasted_risk": risk_history[-1],
            "trend": "INSUFFICIENT DATA"
        }

    changes = []

    for i in range(1, len(risk_history)):
        changes.append(
            risk_history[i] - risk_history[i - 1]
        )

    average_change = sum(changes) / len(changes)

    forecasted_risk = risk_history[-1] + average_change

    forecasted_risk = max(
        0,
        min(100, forecasted_risk)
    )

    if average_change > 2:
        trend = "INCREASING"
    elif average_change < -2:
        trend = "DECREASING"
    else:
        trend = "STABLE"

    return {
        "forecasted_risk": round(forecasted_risk, 2),
        "trend": trend
    }


def analyze_encoded_data(input_data, risk_history):

    # Prediction
    prediction = model.predict(input_data)[0]

    # Probability
    probability = model.predict_proba(input_data)[0]

    normal_probability = round(probability[0] * 100, 2)
    attack_probability = round(probability[1] * 100, 2)

    # Risk calculation
    risk_score, risk_level = calculate_risk(
        probability[1]
    )

    # Forecast
    forecast = forecast_risk(risk_history)

    # Alert
    if risk_level == "CRITICAL":
        alert = "CRITICAL SECURITY ALERT"
    elif risk_level == "HIGH":
        alert = "HIGH RISK DETECTED"
    elif risk_level == "MEDIUM":
        alert = "SUSPICIOUS ACTIVITY DETECTED"
    else:
        alert = "NETWORK STATUS NORMAL"

    return {
        "prediction": "ATTACK" if prediction == 1 else "NORMAL",
        "normal_probability": normal_probability,
        "attack_probability": attack_probability,
        "current_risk": risk_score,
        "risk_level": risk_level,
        "forecasted_risk": forecast["forecasted_risk"],
        "trend": forecast["trend"],
        "alert": alert
    }
    
