# ============================================================
# HYDROSCAN WATER QUALITY - ML MODEL TRAINING
# ============================================================

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# ============================================================
# 1. LOAD DATASET
# ============================================================

DATASET_PATH = "dataset\HydroScan Water Quality.csv"

df = pd.read_csv(DATASET_PATH)

print("\nDataset Loaded Successfully!")
print("Dataset Shape:", df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())


# ============================================================
# 2. CLEAN COLUMN NAMES
# ============================================================

df.columns = df.columns.str.strip()

# Remove missing values
df = df.dropna()

print("\nAfter Removing Missing Values:")
print(df.shape)


# ============================================================
# 3. DEFINE INPUT FEATURES
# ============================================================

FEATURES = [
    "pH",
    "Turbidity_NTU",
    "TDS_mg_L",
    "Temperature_C"
]

TARGET = "Label"


# ============================================================
# 4. CHECK REQUIRED COLUMNS
# ============================================================

for column in FEATURES + [TARGET]:
    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' not found in dataset.\n"
            f"Available columns: {df.columns.tolist()}"
        )


# ============================================================
# 5. INPUT AND OUTPUT
# ============================================================

X = df[FEATURES]
y = df[TARGET]


# ============================================================
# 6. ENCODE LABEL
# ============================================================

label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)

print("\nLabel Mapping:")

for index, label in enumerate(label_encoder.classes_):
    print(index, "=", label)


# ============================================================
# 7. SPLIT DATASET
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))


# ============================================================
# 8. FEATURE SCALING
# ============================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ============================================================
# 9. TRAIN RANDOM FOREST MODEL
# ============================================================

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train_scaled, y_train)


# ============================================================
# 10. MODEL PREDICTION
# ============================================================

y_pred = model.predict(X_test_scaled)


# ============================================================
# 11. MODEL ACCURACY
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

print("\n======================================")
print("MODEL TRAINING COMPLETED")
print("======================================")

print(f"\nAccuracy: {accuracy * 100:.2f}%")


# ============================================================
# 12. CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )
)


# ============================================================
# 13. CONFUSION MATRIX
# ============================================================

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ============================================================
# 14. FEATURE IMPORTANCE
# ============================================================

print("\nFeature Importance:")

for feature, importance in zip(
    FEATURES,
    model.feature_importances_
):
    print(
        f"{feature}: {importance:.4f}"
    )


# ============================================================
# 15. SAVE MODEL
# ============================================================

joblib.dump(
    model,
    "hydroscan_water_quality_model.pkl"
)

# Save scaler
joblib.dump(
    scaler,
    "hydroscan_scaler.pkl"
)

# Save label encoder
joblib.dump(
    label_encoder,
    "hydroscan_label_encoder.pkl"
)


# ============================================================
# 16. SAVE FEATURE NAMES
# ============================================================

joblib.dump(
    FEATURES,
    "hydroscan_features.pkl"
)


print("\n======================================")
print("FILES SAVED SUCCESSFULLY")
print("======================================")

print("1. hydroscan_water_quality_model.pkl")
print("2. hydroscan_scaler.pkl")
print("3. hydroscan_label_encoder.pkl")
print("4. hydroscan_features.pkl")