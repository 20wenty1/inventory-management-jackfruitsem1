from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import csv, joblib

texts, labels = [], []
with open("math_proof_verifier_dataset_14000_13.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        texts.append(r["proof_text"])
        labels.append(int(r["is_correct"]))

print("Loaded samples:", len(texts))
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

vec = TfidfVectorizer(max_features=5000)
X_train_vec = vec.fit_transform(X_train)
X_test_vec = vec.transform(X_test)

model = LogisticRegression(max_iter=1000)
print("Training model...")
model.fit(X_train_vec, y_train)

preds = model.predict(X_test_vec)
acc = accuracy_score(y_test, preds)
print("Accuracy:", acc)

joblib.dump(vec, "vectorizer.pkl")
joblib.dump(model, "model.pkl")
print("✅ Model and vectorizer saved successfully!")