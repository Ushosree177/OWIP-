import csv
from smart_link_opener import identify_official_website
from urllib.parse import urlparse

tp = fp = fn = total = 0

def normalize(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower().replace("www.", "")
    return domain

def is_match(predicted, true):
    # ✅ Main logic: domain-level + partial match
    if predicted == true:
        return True
    if true in predicted:
        return True
    if predicted in true:
        return True
    return False

with open("dataset.csv", "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        query = row["query"]
        true_link = row["official_link"]

        print(f"\n🔍 Testing: {query}")

        try:
            result = identify_official_website(query)
            predicted_link = result.get("link", "")

            if predicted_link:
                predicted = normalize(predicted_link)
                true = normalize(true_link)

                if is_match(predicted, true):
                    print("✅ Correct (TP)")
                    tp += 1
                else:
                    print(f"❌ Wrong (FP) → {predicted}")
                    fp += 1
                    fn += 1
            else:
                print("❌ No link detected (FN)")
                fn += 1

        except Exception as e:
            print(f"⚠️ Error: {e}")
            fn += 1

        total += 1

# ===============================
# 📊 Metrics
# ===============================
precision = tp / (tp + fp) if (tp + fp) else 0
recall = tp / (tp + fn) if (tp + fn) else 0
f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0
accuracy = tp / total if total else 0

print("\n==============================")
print("📊 FINAL RESULTS")
print("==============================")

print(f"Total Samples : {total}")
print(f"TP : {tp} | FP : {fp} | FN : {fn}")

print("\n--- Metrics ---")
print(f"🎯 Accuracy : {accuracy:.3f}")
print(f"🎯 Precision: {precision:.3f}")
print(f"🎯 Recall   : {recall:.3f}")
print(f"🎯 F1 Score : {f1:.3f}")