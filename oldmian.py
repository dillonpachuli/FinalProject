import tkinter as tk
from tkinter import messagebox
from itertools import combinations

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class ScoredMenuItem(MenuItem):
    def __init__(self, name, price, score):
        super().__init__(name, price)
        self.score = score

menu_items = [
    MenuItem("McCrispy", 7.49),
    MenuItem("Deluxe McCrispy", 8.29),
    MenuItem("Spicy McCrispy", 7.09),
    MenuItem("Spicy Deluxe McCrispy", 8.29),
    MenuItem("Filet-O-Fish", 5.99),
    MenuItem("McChicken", 3.10),
    MenuItem("Big Mac", 7.29),
    MenuItem("Quarter Pounder with Cheese", 7.39),
    MenuItem("Double Quarter Pounder with Cheese", 9.29),
    MenuItem("Quarter Pounder with Cheese Deluxe", 8.29),
    MenuItem("McDouble", 3.65),
    MenuItem("Bacon Quarter Pounder with Cheese", 9.79),
    MenuItem("Cheeseburger", 2.39),
    MenuItem("Double Cheeseburger", 4.19),
    MenuItem("Hamburger", 2.19),
    MenuItem("Chicken McNuggets (4 pc)", 2.89),
    MenuItem("Chicken McNuggets (6 pc)", 3.89),
    MenuItem("Chicken McNuggets (10 pc)", 5.60),
    MenuItem("Chicken McNuggets (20 pc)", 10.69),
    MenuItem("Small Fries", 1.89),
    MenuItem("Medium Fries", 2.99),
    MenuItem("Large Fries", 3.79),
]

def find_best_combo(items, budget):
    best_combo = []
    best_score = 0
    for r in range(1, len(items) + 1):
        for subset in combinations(items, r):
            total_price = sum(item.price for item in subset)
            total_score = sum(item.score for item in subset)
            if total_price <= budget and total_score > best_score:
                best_score = total_score
                best_combo = subset
    return best_combo

# ----- UI Logic -----
def calculate():
    try:
        budget = float(budget_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid budget.")
        return

    scored_items = []
    for i, entry in enumerate(score_entries):
        score_text = entry.get().strip()
        if score_text == "":
            continue
        try:
            score = int(score_text)
            if not 0 <= score <= 10:
                raise ValueError
            if score > 0:
                item = menu_items[i]
                scored_items.append(ScoredMenuItem(item.name, item.price, score))
        except ValueError:
            messagebox.showerror("Invalid Input", f"Enter a score 0–10 for {menu_items[i].name}")
            return

    if len(scored_items) == 0:
        messagebox.showwarning("No Items", "Please score at least one item (1–10).")
        return

    best_combo = find_best_combo(scored_items, budget)

    output.delete("1.0", tk.END)
    if best_combo:
        output.insert(tk.END, "Best Combo:\n")
        for item in best_combo:
            output.insert(tk.END, f"{item.name} - ${item.price:.2f} | Score: {item.score}\n")
        total_price = sum(i.price for i in best_combo)
        total_score = sum(i.score for i in best_combo)
        output.insert(tk.END, f"\nTotal Price: ${total_price:.2f}\nTotal Score: {total_score}")
    else:
        output.insert(tk.END, "No valid combo under your budget.")

# ----- Tkinter UI -----
root = tk.Tk()
root.title("McDonald's Combo Optimizer")

tk.Label(root, text="Enter your budget ($):").pack()
budget_entry = tk.Entry(root)
budget_entry.pack()

frame = tk.Frame(root)
frame.pack()

score_entries = []

for item in menu_items:
    row = tk.Frame(frame)
    row.pack(anchor='w')
    tk.Label(row, text=f"{item.name} - ${item.price:.2f}", width=40, anchor='w').pack(side='left')
    tk.Label(row, text="Score (0–10):").pack(side='left')
    score_entry = tk.Entry(row, width=5)
    score_entries.append(score_entry)
    score_entry.pack(side='left')

tk.Button(root, text="Find Best Combo", command=calculate).pack(pady=10)

output = tk.Text(root, height=12, width=60)
output.pack()

root.mainloop()
