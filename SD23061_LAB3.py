import streamlit as st

# -----------------------------
# RULES (unchanged)
# -----------------------------
RULES_JSON = [
    {
        "name": "Top merit candidate",
        "priority": 100,
        "conditions": [
            ["cgpa", ">=", 3.7],
            ["co_curricular_score", ">=", 80],
            ["family_income", "<=", 8000],
            ["disciplinary_actions", "==", 0]
        ],
        "action": {
            "decision": "AWARD_FULL",
            "reason": "Excellent academic & co-curricular performance, with acceptable need"
        }
    },
    {
        "name": "Good candidate - partial scholarship",
        "priority": 80,
        "conditions": [
            ["cgpa", ">=", 3.3],
            ["co_curricular_score", ">=", 60],
            ["family_income", "<=", 12000],
            ["disciplinary_actions", "<=", 1]
        ],
        "action": {
            "decision": "AWARD_PARTIAL",
            "reason": "Good academic & involvement record with moderate need"
        }
    },
    {
        "name": "Need-based review",
        "priority": 70,
        "conditions": [
            ["cgpa", ">=", 2.5],
            ["family_income", "<=", 4000]
        ],
        "action": {
            "decision": "REVIEW",
            "reason": "High need but borderline academic score"
        }
    },
    {
        "name": "Low CGPA – not eligible",
        "priority": 95,
        "conditions": [
            ["cgpa", "<", 2.5]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "CGPA below minimum scholarship requirement"
        }
    },
    {
        "name": "Serious disciplinary record",
        "priority": 90,
        "conditions": [
            ["disciplinary_actions", ">=", 2]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "Too many disciplinary records"
        }
    }
]


# -----------------------------
# EVALUATOR
# -----------------------------
def evaluate_rule(rule, facts):
    for cond in rule["conditions"]:
        field, operator, value = cond
        fact_value = facts.get(field)

        # if a fact is missing, treat as non-matching
        if fact_value is None:
            return False

        if operator == ">=" and not (fact_value >= value):
            return False
        if operator == "<=" and not (fact_value <= value):
            return False
        if operator == ">" and not (fact_value > value):
            return False
        if operator == "<" and not (fact_value < value):
            return False
        if operator == "==" and not (fact_value == value):
            return False
        if operator == "!=" and not (fact_value != value):
            return False

    return True


def evaluate_scholarship(facts):
    matched = []
    for rule in RULES_JSON:
        if evaluate_rule(rule, facts):
            matched.append(rule)

    if not matched:
        return {"decision": "NO_MATCH", "reason": "No rules matched."}

    best_rule = max(matched, key=lambda r: r["priority"])
    return {
        "rule_name": best_rule["name"],
        "decision": best_rule["action"]["decision"],
        "reason": best_rule["action"]["reason"],
        "priority": best_rule["priority"]
    }


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="Scholarship Decision Support", layout="centered")
st.title("🎓 Scholarship Decision Support System")
st.write("A simple rule-based system for lab report 3")

st.header("Applicant Information")

# CGPA: float
cgpa = st.number_input("CGPA (0.00 - 4.00)", min_value=0.0, max_value=4.0, step=0.01, format="%.2f")

# Family income: integer (RM)
family_income = st.number_input("Family Income (RM)", min_value=0, step=1, format="%d")

# Co-curricular score: integer slider 0-100
co_curricular = st.slider("Co-curricular Score (0-100)", 0, 100, 50)

# Disciplinary actions: integer
disciplinary = st.number_input("Number of Disciplinary Actions", min_value=0, max_value=10, step=1, format="%d")

if st.button("Evaluate Scholarship"):
    # Ensure types: cgpa float, others ints
    student_facts = {
        "cgpa": float(cgpa),
        "family_income": int(family_income),
        "co_curricular_score": int(co_curricular),
        "disciplinary_actions": int(disciplinary)
    }

    result = evaluate_scholarship(student_facts)

    st.subheader("Decision Result")
    st.write(f"**Rule Triggered:** {result.get('rule_name', 'None')}")
    st.write(f"**Decision:** {result['decision']}")
    st.write(f"**Reason:** {result['reason']}")
    st.write(f"**Priority:** {result.get('priority', '-')}")


