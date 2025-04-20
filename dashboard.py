import streamlit as st

# ---------- Scoring Functions (Updated & Fair) ----------

def score_credit_score(cs):
    return (cs - 300) / 550 * 100

def score_income(income):
    income = max(income, 20000)
    raw = (income - 20000) / (150000 - 20000)
    return raw * 80 + 20  # Score range: 20 to 100

def score_employment(emp_years):
    raw_score = (emp_years / 30) * 100
    return max(raw_score, 20)  # Min employment score = 20

def score_existing_loans(loans):
    return max((5 - loans) / 5 * 100, 0)  # 0 loans = 100, 5 loans = 0

def score_age(age):
    if 25 <= age <= 55:
        return 100
    elif 21 <= age < 25:
        return 90
    elif 18 <= age < 21:
        return 75
    else:
        return 50

# ---------- Risk Classification Logic ----------
def classify_risk(score):
    if score >= 80:
        return "Low Risk"
    elif score >= 60:
        return "Medium Risk"
    else:
        return "High Risk"

# ---------- Streamlit App ----------
def main():
    st.set_page_config(page_title="Credit Health Risk Evaluator", layout="centered")
    st.title("Credit Health Risk Evaluator")
    st.markdown("Answer a few questions and we'll estimate your credit risk level.")

    with st.form("risk_form"):
        age = st.slider("Your Age", 18, 70, 30)
        income = st.number_input("Annual Income (in USD)", min_value=20000, max_value=150000, value=60000)
        credit_score = st.slider("Credit Score", 300, 850, 700)
        employment_length = st.slider("Years of Employment", 0, 30, 5)
        existing_loans = st.slider("Number of Existing Loans", 0, 5, 1)
        submitted = st.form_submit_button("Evaluate Risk")

    if submitted:
        # Score each input
        scores = {
            'credit_score': score_credit_score(credit_score),
            'income': score_income(income),
            'employment': score_employment(employment_length),
            'loans': score_existing_loans(existing_loans),
            'age': score_age(age)
        }

        # Feature weights
        weights = {
            'credit_score': 0.4,
            'income': 0.2,
            'employment': 0.15,
            'loans': 0.15,
            'age': 0.1
        }

        # Compute weighted total score
        total_score = sum(scores[k] * weights[k] for k in scores)
        risk_level = classify_risk(total_score)

        # Results
        st.subheader("Risk Evaluation Result")
        st.write(f"🧮 **Total Score**: {total_score:.2f} / 100")
        st.write(f"📊 **Risk Level**: {risk_level}")
        st.progress(min(int(total_score), 100))

        # Detailed Breakdown
        st.markdown("---")
        st.subheader("Score Breakdown")
        for k in scores:
            label = k.replace('_', ' ').title()
            st.write(f"**{label}**: {scores[k]:.1f} (Weight: {weights[k]*100:.0f}%)")

if __name__ == "__main__":
    main()
