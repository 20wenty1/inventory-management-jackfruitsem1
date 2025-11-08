import csv
import random
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Load data
file_path = "math_proof_verifier_dataset_14000_13.csv"

texts, labels = [], []

print("Loading dataset...")
with open(file_path, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        proof = row.get("proof_text", "").strip()
        if not proof:
            continue
        try:
            label = int(row.get("is_correct", 0))
        except ValueError:
            continue
        texts.append(proof)
        labels.append(label)

print(f"Loaded {len(texts)} samples.")

# ✅ Normalize labels (ensure 1 = Valid, 0 = Invalid)
X_valid = [(t, l) for t, l in zip(texts, labels) if l == 1]
X_invalid = [(t, l) for t, l in zip(texts, labels) if l == 0]

min_count = min(len(X_valid), len(X_invalid))
balanced_data = random.sample(X_valid, min_count) + random.sample(X_invalid, min_count)
random.shuffle(balanced_data)

texts, labels = zip(*balanced_data)
print(f"Balanced dataset: {len(X_valid)} valid + {len(X_invalid)} invalid → {len(texts)} total")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# TF-IDF + Logistic Regression
vec = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
X_train_vec = vec.fit_transform(X_train)
X_test_vec = vec.transform(X_test)

model = LogisticRegression(max_iter=200)
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc:.3f}")
print(classification_report(y_test, y_pred, target_names=["Invalid", "Valid"]))

# Save model
joblib.dump(model, "model.pkl")
joblib.dump(vec, "vectorizer.pkl")
print("✅ Model retrained and saved successfully!")

