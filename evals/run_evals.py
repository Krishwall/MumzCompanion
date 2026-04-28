import json
from agent.agent import run_agent


def run_evals():
    with open("d:/MumzCompanion/evals/test_cases.json", encoding="utf-8") as f:
        cases = json.load(f)

    score = 0
    total = len(cases)

    print("Running Evals...\n")

    for case in cases:
        try:
            res = run_agent(case["input"], case["date_input"])

            # -----------------------------
            # BASIC CHECKS
            # -----------------------------
            refused_match = res.refused == case.get("expected_refused", False)
            lang_match = res.input_language == case.get("expected_language", "en")

            # -----------------------------
            # PRODUCT CHECK
            # -----------------------------
            expected_products = case.get("min_products", 0)
            product_match = len(res.products) >= expected_products

            # -----------------------------
            # FALLBACK CHECK
            # -----------------------------
            fallback_expected = case.get("expect_fallback", False)
            fallback_triggered = len(res.products) == 0

            fallback_match = fallback_expected == fallback_triggered

            # -----------------------------
            # INSIGHT CHECK
            # -----------------------------
            insight_ok = bool(res.timeline_insight.headline and res.timeline_insight.body)

            # -----------------------------
            # FINAL DECISION
            # -----------------------------
            passed = all([
                refused_match,
                lang_match,
                product_match,
                fallback_match,
                insight_ok
            ])

            if passed:
                score += 1
                print(f"✅ Case {case['id']} Passed")
            else:
                print(f"❌ Case {case['id']} Failed")
                print(f"   Refused: {res.refused} (expected {case.get('expected_refused')})")
                print(f"   Language: {res.input_language} (expected {case.get('expected_language')})")
                print(f"   Products: {len(res.products)} (expected ≥ {expected_products})")
                print(f"   Fallback: {fallback_triggered} (expected {fallback_expected})")

        except Exception as e:
            print(f"❌ Case {case['id']} Errored: {e}")

    print(f"\nFinal Score: {score}/{total}")


if __name__ == "__main__":
    run_evals()