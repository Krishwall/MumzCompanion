import json
import sys
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
            
            refused_match = res.refused == case["expected_refused"]
            lang_match = res.input_language == case["expected_language"]
            
            if refused_match and lang_match:
                score += 1
                print(f"✅ Case {case['id']} Passed")
            else:
                print(f"❌ Case {case['id']} Failed: Refused({res.refused} vs {case['expected_refused']}), Lang({res.input_language} vs {case['expected_language']})")
                
        except Exception as e:
            print(f"❌ Case {case['id']} Errored: {e}")

    print(f"\nFinal Score: {score}/{total}")

if __name__ == "__main__":
    run_evals()
