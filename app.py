import streamlit as st
import csv, json, os, joblib

st.set_page_config(page_title="AI Math Proof Verifier", layout="wide")
st.title("🤖 AI Math Proof Verifier")
st.write("Upload a dataset or enter a proof to check validity using the trained ML model.")

# Load model safely
@st.cache_resource
def load_model():
    try:
        vec = joblib.load("vectorizer.pkl")
        model = joblib.load("model.pkl")
        return vec, model
    except Exception as e:
        st.error(f"⚠️ Could not load ML model: {e}")
        return None, None

vec, model = load_model()

def verify_with_model(proof_text):
    if not vec or not model:
        return "Error", 0.0
    X = vec.transform([proof_text])
    probs = model.predict_proba(X)[0]
    p_invalid, p_valid = probs
    verdict = "✅ Valid" if p_valid >= 0.5 else "❌ Invalid"
    confidence = max(p_invalid, p_valid)
    return verdict, confidence

# --- Section 1: Manual Proof Entry ---
st.subheader("🔹 Verify a Single Proof")

proof_text = st.text_area("✍️ Enter your proof text:")

if st.button("🔍 Verify Proof"):
    if proof_text.strip():
        verdict, confidence = verify_with_model(proof_text)
        st.markdown(f"### {verdict}")
        st.markdown(f"**Confidence:** {confidence:.2f}")
        if verdict.startswith("✅"):
            st.success("Proof shows structured logical reasoning.")
        else:
            st.error("Proof seems logically inconsistent or incomplete.")
    else:
        st.warning("Please enter a proof to analyze.")

# --- Section 2: Upload CSV and Batch Analyze ---
st.subheader("📂 Upload CSV for Bulk Proof Verification")
uploaded_file = st.file_uploader("Upload a CSV file (must contain 'proof_text' column)", type=["csv"])

if uploaded_file is not None:
    try:
        reader = csv.DictReader(uploaded_file.read().decode("utf-8").splitlines())
        results = []
        for i, row in enumerate(reader, start=1):
            text = row.get("proof_text", "").strip()
            if text:
                verdict, conf = verify_with_model(text)
                results.append({
                    "id": i,
                    "proof_text": text[:100] + ("..." if len(text) > 100 else ""),
                    "verdict": verdict,
                    "confidence": round(conf, 2)
                })

        if results:
            st.success(f"✅ Processed {len(results)} proofs.")
            st.dataframe(results)

            # Save downloadable results
            output_file = "verified_results.csv"
            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)

            with open(output_file, "r", encoding="utf-8") as f:
                st.download_button(
                    label="⬇️ Download Results as CSV",
                    data=f.read(),
                    file_name="verified_results.csv",
                    mime="text/csv"
                )

        else:
            st.warning("No valid proofs found in the uploaded file.")

    except Exception as e:
        st.error(f"Error reading file: {e}")
