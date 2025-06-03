import customtkinter as ctk
from tkinter import messagebox
from itertools import combinations

ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("green")  
class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class ScoredMenuItem(MenuItem):
    def __init__(self, name, price, score):
        super().__init__(name, price)
        self.score = score

menu_items = [
    #BURGERS (15 ITEMS)
    MenuItem("Big Mac", 6.99),
    MenuItem("Quarter Pounder with Cheese", 6.99),
    MenuItem("Double Quarter Pounder with Cheese", 7.99),
    MenuItem("Bacon Quarter Pounder with Cheese", 7.69),
    MenuItem("Quarter Pounder with Cheese Deluxe", 7.29),
    MenuItem("Double Quarter Pounder with Cheese Deluxe", 8.59),
    MenuItem("Double Bacon Quarter Pounder with Cheese", 9.19),
    MenuItem("Cheeseburger", 2.99),
    MenuItem("Double Cheeseburger", 3.89),
    MenuItem("Triple Cheeseburger", 4.89),
    MenuItem("Bacon Double Cheeseburger", 4.39),
    MenuItem("Hamburger", 2.79),
    MenuItem("Double Hamburger", 3.59),
    MenuItem("McDouble", 3.69),
    MenuItem("Bacon McDouble", 4.59),

    #CHICKEN (12 ITEMS)
    MenuItem("McCrispy Strips (3p)", 6.99),
    MenuItem("McCrispy Strips (4p)", 7.99),
    MenuItem("McCrispy", 6.79),
    MenuItem("Deluxe McCrispy", 6.99),
    MenuItem("Spicy McCrispy", 6.79),
    MenuItem("Deluxe Spicy McCrispy", 7.09),
    MenuItem("Chicken McNuggets (4p)", 2.89),
    MenuItem("Chicken McNuggets (6p)", 3.99),
    MenuItem("Chicken McNuggets (10p)", 6.39),
    MenuItem("Chicken McNuggets (20p)", 8.49),
    MenuItem("Chicken McNuggets (40p)", 14.79),
    MenuItem("McChicken", 3.69),

    #FISH (3 ITEMS)
    MenuItem("Filet-O-Fish", 5.79),
    MenuItem("Double Filet-O-Fish", 7.39),
    MenuItem("2 Filet-O-Fish", 7.00),
    
    #FRIES (3 ITEMS)
    MenuItem("Small French Fries", 2.19),
    MenuItem("Medium French Fries", 3.99),
    MenuItem("Large French Fries", 4.99),

    #HAPPY MEAL (3 ITEMS)
    MenuItem("Hamburger Happy Meal", 5.29),
    MenuItem("Chicken McNugget (4p) Happy Meal", 5.49),
    MenuItem("Chicken McNugget (6p) Happy Meal", 6.29),

    #DESSERT/SHAKES (15 ITEMS)
    MenuItem("Chocolate Shake", 4.79),
    MenuItem("Strawberry Shake", 4.79),
    MenuItem("Vanilla Shake", 4.79),
    MenuItem("M&M McFlurry", 4.99),
    MenuItem("OREO McFlurry", 4.99),
    MenuItem("Caramel Sundae", 4.49),
    MenuItem("Hot Fudge Sundae", 4.49),
    MenuItem("Plain Sundae", 4.49),
    MenuItem("3 Pack of Cookies", 2.99),
    MenuItem("13 Cookie Tots", 5.99),
    MenuItem("Apple Pie", 1.89),
    MenuItem("Strawberry & Creme Pie", 2.29),
    MenuItem("2 Apple Pies", 2.99),
    MenuItem("2 Strawberry & Creme Pies", 3.29),
    MenuItem("Vanilla Cone", 2.59)
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

    output.configure(state="normal")
    output.delete("1.0", "end")
    if best_combo:
        output.insert("end", "Best Combo:\n")
        for item in best_combo:
            output.insert("end", f"{item.name} - ${item.price:.2f} | Score: {item.score}\n")
        total_price = sum(i.price for i in best_combo)
        total_score = sum(i.score for i in best_combo)
        output.insert("end", f"\nTotal Price: ${total_price:.2f}\nTotal Score: {total_score}")
    else:
        output.insert("end", "No valid combo under your budget.")
    output.configure(state="disabled")

# ----- CustomTkinter UI -----
root = ctk.CTk()
root.title("McDonald's Order Optimizer")
root.geometry("700x750")

ctk.CTkLabel(root, text="Enter your budget ($):", font=ctk.CTkFont(size=16)).pack(pady=5)
budget_entry = ctk.CTkEntry(root)
budget_entry.pack(pady=5)

scroll_frame = ctk.CTkScrollableFrame(root, width=680, height=400)
scroll_frame.pack(pady=10)

score_entries = []

for item in menu_items:
    row = ctk.CTkFrame(scroll_frame)
    row.pack(fill="x", pady=2)
    ctk.CTkLabel(row, text=f"{item.name} - ${item.price:.2f}", width=400, anchor='w').pack(side="left", padx=10)
    ctk.CTkLabel(row, text="Score (0–10):").pack(side="left")
    score_entry = ctk.CTkEntry(row, width=50)
    score_entries.append(score_entry)
    score_entry.pack(side="left", padx=5)

ctk.CTkButton(root, text="Find Best Combo", command=calculate).pack(pady=15)

output = ctk.CTkTextbox(root, height=200, width=680)
output.pack()
output.configure(state="disabled")

root.mainloop()