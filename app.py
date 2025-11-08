import streamlit as st
import csv, json, os, joblib, re

# --------------------------------------------------------
# STREAMLIT CONFIG
# --------------------------------------------------------
st.set_page_config(page_title="AI Math Proof Verifier", layout="wide")
st.title("🤖 AI Math Proof Verifier (Balanced ML + Rules)")
st.write("Hybrid system: Machine Learning for large datasets + Rule-based reasoning for quick checks.")

# --------------------------------------------------------
# LOAD MODEL
# --------------------------------------------------------
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

# --------------------------------------------------------
# RULE-BASED LOGIC CHECK (used for short inputs only)
# --------------------------------------------------------
def rule_based_check(proof_text):
    text = proof_text.lower()
    valid_patterns = [
        "assume", "therefore", "hence", "thus", "proved", "q.e.d",
        "let", "for all", "induction", "contradiction"
    ]
    invalid_patterns = [
        "2=1", "divide by zero", "false proof", "all numbers are equal",
        "random", "feels right", "wrong"
    ]
    if any(p in text for p in invalid_patterns):
        return "❌ Invalid", 0.95
    if any(p in text for p in valid_patterns):
        return "✅ Valid", 0.85
    return None, None

# --------------------------------------------------------
# HYBRID VERIFIER (smart switch)
# --------------------------------------------------------
def verify_with_model(proof_text, use_rules=True):
    text_len = len(proof_text.strip().split())

    # Only use rule-based logic if the text is short (< 20 words)
    if use_rules and text_len < 20:
        verdict, conf = rule_based_check(proof_text)
        if verdict:
            return verdict, conf

    # Otherwise use ML model
    if not vec or not model:
        return "Error loading model", 0.0
    X = vec.transform([proof_text])
    probs = model.predict_proba(X)[0]
    p_invalid, p_valid = probs
    verdict = "✅ Valid" if p_valid >= 0.5 else "❌ Invalid"
    confidence = max(p_invalid, p_valid)
    return verdict, confidence

# --------------------------------------------------------
# SINGLE PROOF ANALYSIS
# --------------------------------------------------------
st.subheader("✍️ Verify a Single Proof")

proof_text = st.text_area("Enter your proof text:")

if st.button("🔍 Verify Proof"):
    if proof_text.strip():
        verdict, confidence = verify_with_model(proof_text, use_rules=True)
        color = "green" if "Valid" in verdict else "red"
        st.markdown(f"### <span style='color:{color}'>{verdict}</span>", unsafe_allow_html=True)
        st.markdown(f"**Confidence:** {confidence:.2f}")
        if "Valid" in verdict:
            st.success("This proof demonstrates consistent logical reasoning.")
        else:
            st.error("The proof appears logically inconsistent or incomplete.")
    else:
        st.warning("Please enter a proof to analyze.")

# --------------------------------------------------------
# BATCH ANALYSIS (CSV UPLOAD)
# --------------------------------------------------------
st.subheader("📂 Upload a CSV File for Bulk Proof Verification")
uploaded_file = st.file_uploader("Upload a CSV file (must contain 'proof_text' column)", type=["csv"])

if uploaded_file is not None:
    try:
        reader = csv.DictReader(uploaded_file.read().decode("utf-8").splitlines())
        results = []
        for i, row in enumerate(reader, start=1):
            text = row.get("proof_text", "").strip()
            if not text:
                continue
            # ML model only for dataset
            verdict, conf = verify_with_model(text, use_rules=False)
            results.append({
                "id": i,
                "proof_text": text[:150] + ("..." if len(text) > 150 else ""),
                "verdict": verdict,
                "confidence": round(conf, 2)
            })

        if results:
            st.success(f"✅ Processed {len(results)} proofs.")
            st.dataframe(results)

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
            st.warning("No proofs found in the uploaded file.")

    except Exception as e:
        st.error(f"Error processing file: {e}")

# --------------------------------------------------------
# FOOTER
# --------------------------------------------------------
st.markdown("---")
st.caption("Hackathon Prototype · AI Math Proof Verifier · Hybrid ML + Rules (CSV uses ML only)")
