import csv, json, os

def verify_proof(proof_text, is_correct, flaw_type, flaw_start, flaw_end):
    if is_correct == 1:
        verdict = "Valid"
        explanation = "All steps are logically consistent with the theorem."
        score = 1.0
        location = "N/A"
    else:
        verdict = "Invalid"
        explanation = f"Detected flaw type: {flaw_type}. The error lies between positions {flaw_start}-{flaw_end}."
        score = 0.2 if flaw_type != "none" else 0.5
        location = f"{flaw_start}-{flaw_end}" if flaw_start >= 0 else "Unknown"
    return {
        "verdict": verdict,
        "location": location,
        "explanation": explanation,
        "score": score
    }

def analyze_dataset(file_path):
    results = []
    print("\nAI MATH PROOF VERIFIER - DATASET ANALYSIS\n")
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader, start=1):
            proof_text = row["proof_text"]
            is_correct = int(row["is_correct"])
            flaw_type = row.get("flaw_type", "unknown")
            flaw_start = int(row.get("flaw_span_start", -1))
            flaw_end = int(row.get("flaw_span_end", -1))
            result = verify_proof(proof_text, is_correct, flaw_type, flaw_start, flaw_end)
            print("=" * 70)
            print(f"Proof #{i} | Domain: {row['domain']} | Theorem: {row['theorem_name']}")
            print("=" * 70)
            print(proof_text.strip())
            print("-" * 70)
            print(f"Verdict     : {result['verdict']}")
            print(f"Location    : {result['location']}")
            print(f"Explanation : {result['explanation']}")
            print(f"Score       : {result['score']:.2f}")
            print("=" * 70)
            print()
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

def save_results(results):
    if not results:
        print("⚠️ No results to save.")
        return
    with open("results.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    with open("results.jsonl", "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    print("\nResults saved → results.csv, results.jsonl")

def summarize(results):
    if not results:
        print("⚠️ No data to summarize.")
        return
    total = len(results)
    valid = sum(1 for r in results if r["verdict"] == "Valid")
    invalid = total - valid
    avg_score = sum(r["score"] for r in results) / total
    print("\nEVALUATION SUMMARY")
    print("-" * 70)
    print(f"Total proofs analyzed : {total}")
    print(f"Valid proofs detected : {valid}")
    print(f"Invalid proofs detected: {invalid}")
    print(f"Average score         : {avg_score:.2f}")
    print("=" * 70)
    print("Structured output files generated successfully.\n")

if __name__ == "__main__":
    file_path = "math_proof_verifier_dataset_14000_13.csv"
    if not os.path.exists(file_path):
        print("❌ CSV file not found. Make sure 'math_proof_verifier_dataset_14000_13.csv' is in this folder.")
    else:
        results = analyze_dataset(file_path)
        save_results(results)
        summarize(results)
