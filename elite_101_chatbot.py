"""
def greet_user():
    print("Hello! I'm FinBot. I can help you open a new bank account.")
first_name = input("What's your first name? ")
middle_name = input("What's your middle name? Enter N/A if none: ")
last_name = input("What's your last name? ")
email = input("Email (optional): ")
phone = input("Phone: ")
print(f"\n Thanks, {first_name}! I'll use this info to personalize your experience.")

return{
    "first_name": first_name,
    "middle_name":  middle_name or None,
    "last_name": last_name,
    "email": email or None,
    "phone": phone

}
"""

from datetime import datetime

#tiny helpers (simple, not fancy)

def clean_text(s):
    """Trim spaces and collapse inner spaces a bit."""
    return " ".join(s.strip().split())

def read_nonempty(prompt):
    """Ask until we get something non-empty."""
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("Please enter something.")

def read_int(prompt, min_val=None, max_val=None):
    while True:
        v = input(prompt).strip()
        if not v.isdigit():
            print("  Age must be a whole number (digits only).")
            continue
        n = int(v)
        if min_val is not None and n < min_val:
            print(f"  Must be at least {min_val}.")
            continue
        if max_val is not None and n > max_val:
            print(f"  Must be at most {max_val}.")
            continue
        return n

def read_float(prompt, min_val=None):
    while True:
        v = input(prompt).strip()
        try:
            n = float(v)
        except ValueError:
            print("  Please enter a number like 42000 or 42000.00")
            continue
        if min_val is not None and n < min_val:
            print(f"  Must be at least {min_val}.")
            continue
        return n

def yes_no(prompt):
    """Return True for yes, False for no."""
    v = input(prompt + " [y/N]: ").strip().lower()
    return v in ("y", "yes")

def normalize_phone(user_input):
    """
    - keep only digits
    - if we have 10 digits, assume US and format as +1##########
    - if we have 11–15 digits, just return with a leading + (international-ish)
    - otherwise, say it's invalid
    """
    digits = "".join(ch for ch in user_input if ch.isdigit())
    if len(digits) == 10: #normal US number
        return "+1" + digits
    elif 11 <= len(digits) <= 15: #maybe international?
        return "+" + digits
    else:
        return None
#bot greeting
def greet():
    print("Hello! I'm FinBot. I can help you open a new bank or credit card account.")

def collect_profile():
    print("\nLet's make a small profile first.")
    first = clean_text(read_nonempty("First name: "))
    middle = input("Middle name (type N/A if none): ").strip()
    if middle.lower() in ("n/a", "na", "none", ""):
        middle = None
    else:
        middle = clean_text(middle)
    last = clean_text(read_nonempty("Last name: "))

    email = input("Email (optional): ").strip() or None

    # super simple phone check
    while True:
        raw_phone = input("Phone: ").strip()
        phone = normalize_phone(raw_phone)
        if phone:
            break
        print("  Phone looks off. Try 10 digits (like 5125550123) or include country code.")

    age = read_int("How old are you? ", min_val=16, max_val=120)
    income = read_float("Approx annual income (pre-tax, e.g., 42000): ", min_val=0)

    student = yes_no("Are you a current student?")

    print("\nWhat’s your main goal right now?")
    print("  1. Everyday spending & bills")
    print("  2. Earn interest on savings")
    print("  3. Build/establish credit")
    print("  4. Rewards for travel")
    goals = {"1": "everyday_spend", "2": "save_interest", "3": "build_credit", "4": "travel_rewards"}
    goal_choice = ""
    while goal_choice not in goals:
        goal_choice = input("Choose 1–4: ").strip()
    goal = goals[goal_choice]

    print(f"\nThanks, {first}! I’ll use this info to personalize your experience.")
    return {
        "first_name": first,
        "middle_name": middle,
        "last_name": last,
        "email": email,
        "phone": phone,
        "age": age,
        "income": income,
        "is_student": student,
        "goal": goal,
    }

def recommend_products(profile):
    """
    - If student or under 18, Student Checking is good
    - Goal rules:
        everyday_spend, Checking (+ Cashback Card if income >= 20k else Secured Card)
        save_interest, High-Yield Savings (+ Checking if not student)
        build_credit, Secured Card (+ Student Checking if student else Checking)
        travel_rewards, cashback Card (as a stand-in) if income >= 20k, else Secured; + Checking
    """
    recs = []

    is_student = profile["is_student"] or profile["age"] < 18
    income = profile["income"]
    goal = profile["goal"]

    if is_student:
        recs.append(("Student Checking", "No monthly fees; made for students."))

    if goal == "everyday_spend":
        recs.append(("Checking", "No monthly fee with direct deposit; debit card; ATM access."))
        if income >= 20000:
            recs.append(("Cashback Credit Card", "1.5% back; no annual fee."))
        else:
            recs.append(("Secured Credit Card", "Helps build credit with refundable deposit."))
    elif goal == "save_interest":
        recs.append(("High-Yield Savings", "Earn more interest; no minimum to open."))
        if not is_student:
            recs.append(("Checking", "Pair with savings for easy transfers."))
    elif goal == "build_credit":
        recs.append(("Secured Credit Card", "Build/repair credit; reports to bureaus."))
        if is_student:
            recs.append(("Student Checking", "Fee-free and friendly for students."))
        else:
            recs.append(("Checking", "Everyday banking."))
    elif goal == "travel_rewards":
        if income >= 20000:
            recs.append(("Cashback Credit Card", "Simple rewards now; upgrade later."))
        else:
            recs.append(("Secured Credit Card", "Start here; move to rewards later."))
        recs.append(("Checking", "Keep spending and bills organized."))

    # remove duplicates while keeping order
    seen = set()
    unique = []
    for name, blurb in recs:
        if name not in seen:
            unique.append((name, blurb))
            seen.add(name)
    return unique

def show_recommendations(recs):
    print("\nBased on your answers, here are good fits:")
    for i, (name, blurb) in enumerate(recs, start=1):
        print(f"  {i}. {name} — {blurb}")

def choose(recs):
    while True:
        pick = input("Enter the number you want to start with: ").strip()
        if pick.isdigit():
            idx = int(pick)
            if 1 <= idx <= len(recs):
                return recs[idx - 1][0]  # return product name
        print("  Please choose a valid number from the list.")

def submit_application(profile, selected_product):
    # tiny summary
    print("\nApplication started!")
    print("Here’s your summary:")
    masked_email = profile["email"] if profile["email"] else "(none)"
    masked_phone = "***" + profile["phone"][-4:] if len(profile["phone"]) >= 4 else profile["phone"]
    full_name = (
        f"{profile['first_name']} "
        + (profile['middle_name'] + " " if profile['middle_name'] else "")
        + profile['last_name']
    )
    print("-" * 35)
    print("Name:          ", full_name)
    print("Email:         ", masked_email)
    print("Phone:         ", masked_phone)
    print("Age:           ", profile["age"])
    print("Income:        ", f"${profile['income']:.2f}")
    print("Student:       ", "Yes" if profile["is_student"] else "No")
    print("Goal:          ", profile["goal"])
    print("Selected:      ", selected_product)
    print("Created At:    ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("-" * 35) #to make it look like a receipt?
    print("A specialist may contact you if we need anything else. Thanks for choosing FinBot!")

def quick_math():
    try:
        a = float(input("First number: "))
        b = float(input("Second number: "))
        op = input("Operator (+, -, *, /): ").strip()
        if op == "+":
            print("Result:", a + b)
        elif op == "-":
            print("Result:", a - b)
        elif op == "*":
            print("Result:", a * b)
        elif op == "/":
            if b == 0:
                print("Cannot divide by zero.")
            else:
                print("Result:", a / b)
        else:
            print("Unknown operator.")
    except Exception as e:
        print("That didn’t work:", e)

def main_menu():
    greet()
    name = read_nonempty("\nWhat’s your name? ")
    try:
        age_preview = read_int("How old are you? ")
    except Exception:
        age_preview = None

    print(f"\nNice to meet you, {name}!{' You are ' + str(age_preview) + ' years old.' if age_preview else ''}")
    while True:
        print("\nHow can I help you today?")
        print("  1. Tell me a joke")
        print("  2. Get the current date/time")
        print("  3. Do a quick math problem")
        print("  4. Start new account/credit application")
        print("  5. Quit")
        choice = input("Enter a number of your choice: ").strip()

        if choice == "1":
            print("Why did the developer go broke? Because he used up all his cache! Ahahaha")
        elif choice == "2":
            print("Current date/time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")) #turns datetime into a clean string without yucky decimals
        elif choice == "3":
            quick_math()
        elif choice == "4":
            profile = collect_profile()
            recs = recommend_products(profile)
            show_recommendations(recs)
            picked = choose(recs)
            # tiny “disclosure”
            print("\nBefore we continue, please agree to electronic disclosures.")
            if yes_no("Do you agree?"):
                submit_application(profile, picked)
            else:
                print("No problem. You can come back anytime.")
        elif choice == "5":
            print(f"Goodbye, {name}!")
            break
        else:
            print("Please choose 1–5.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nSession canceled. Have a great day!")
