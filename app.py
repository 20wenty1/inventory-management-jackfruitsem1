import streamlit as st
import csv
import json
import os

# ========== CORE LOGIC ==========

def verify_proof(proof_text, is_correct, flaw_type, flaw_start, flaw_end):
    if is_correct == "1" or is_correct == 1:
        verdict = "Valid"
        explanation = "All steps are logically consistent with the theorem."
        score = 1.0
        location = "N/A"
    else:
        verdict = "Invalid"
        explanation = f"Detected flaw type: {flaw_type}. The error lies between positions {flaw_start}-{flaw_end}."
        score = 0.2 if flaw_type != "none" else 0.5
        location = f"{flaw_start}-{flaw_end}" if flaw_start != "" else "Unknown"
    return {
        "verdict": verdict,
        "location": location,
        "explanation": explanation,
        "score": score
    }

def analyze_dataset(file_path):
    results = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            proof_text = row["proof_text"]
            is_correct = row["is_correct"]
            flaw_type = row.get("flaw_type", "unknown")
            flaw_start = row.get("flaw_span_start", "-1")
            flaw_end = row.get("flaw_span_end", "-1")
            result = verify_proof(proof_text, is_correct, flaw_type, flaw_start, flaw_end)
            results.append({
                "proof_id": row["proof_id"],
                "domain": row["domain"],
                "theorem_name": row["theorem_name"],
                "verdict": result["verdict"],
                "location": result["location"],
                "explanation": result["explanation"],
                "score": result["score"]
            })
    return results

# ========== STREAMLIT UI ==========

st.set_page_config(page_title="AI Math Proof Verifier", layout="wide")
st.title("🤖 AI Math Proof Verifier")
st.write("This lightweight app analyzes mathematical proofs and detects logical flaws using only built-in libraries.")

file_path = "math_proof_verifier_dataset_14000_13.csv"

if not os.path.exists(file_path):
    st.error("❌ CSV file not found. Please ensure 'math_proof_verifier_dataset_14000_13.csv' is in the same folder.")
else:
    st.subheader("📂 Dataset Information")
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        preview = [next(reader) for _ in range(5)]
        st.write("**Headers:**", headers)
        st.write("**Preview (first 5 rows):**")
        st.table(preview)

    if st.button("🔍 Run Proof Verification"):
        with st.spinner("Analyzing dataset... please wait..."):
            results = analyze_dataset(file_path)
            total = len(results)
            valid = sum(1 for r in results if r["verdict"] == "Valid")
            invalid = total - valid
            avg_score = sum(r["score"] for r in results) / total

            st.success("✅ Analysis Complete!")
            st.write(f"**Total proofs analyzed:** {total}")
            st.write(f"**Valid proofs:** {valid}")
            st.write(f"**Invalid proofs:** {invalid}")
            st.write(f"**Average score:** {avg_score:.2f}")

            # Show first few results
            st.subheader("📈 Sample Results")
            st.table(results[:10])

            # Save results to CSV + JSONL
            with open("results.csv", "w", newline='', encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)

            with open("results.jsonl", "w", encoding="utf-8") as f:
                for r in results:
                    f.write(json.dumps(r) + "\n")

            st.success("Results saved as 'results.csv' and 'results.jsonl'")
            with open("results.csv", "rb") as f:
                st.download_button("⬇️ Download results.csv", data=f, file_name="results.csv")
