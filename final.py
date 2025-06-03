import customtkinter as ctk
from tkinter import messagebox
import random

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# ---------------- Menu Item Setup ----------------
class MenuItem:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

class ScoredMenuItem(MenuItem):
    def __init__(self, name, price, category, score):
        super().__init__(name, price, category)
        self.score = score

menu_items = [
    #BURGERS (15 ITEMS)
    MenuItem("Big Mac", 6.99, "burger"),
    MenuItem("Quarter Pounder with Cheese", 6.99, "burger"),
    MenuItem("Double Quarter Pounder with Cheese", 7.99, "burger"),
    MenuItem("Bacon Quarter Pounder with Cheese", 7.69, "burger"),
    MenuItem("Quarter Pounder with Cheese Deluxe", 7.29, "burger"),
    MenuItem("Double Quarter Pounder with Cheese Deluxe", 8.59, "burger"),
    MenuItem("Double Bacon Quarter Pounder with Cheese", 9.19, "burger"),
    MenuItem("Cheeseburger", 2.99, "burger"),
    MenuItem("Double Cheeseburger", 3.89, "burger"),
    MenuItem("Triple Cheeseburger", 4.89, "burger"),
    MenuItem("Bacon Double Cheeseburger", 4.39, "burger"),
    MenuItem("Hamburger", 2.79, "burger"),
    MenuItem("Double Hamburger", 3.59, "burger"),
    MenuItem("McDouble", 3.69, "burger"),
    MenuItem("Bacon McDouble", 4.59, "burger"),

    #CHICKEN (12 ITEMS)
    MenuItem("McCrispy Strips (3p)", 6.99, "chicken"),
    MenuItem("McCrispy Strips (4p)", 7.99, "chicken"),
    MenuItem("McCrispy", 6.79, "chicken"),
    MenuItem("Deluxe McCrispy", 6.99, "chicken"),
    MenuItem("Spicy McCrispy", 6.79, "chicken"),
    MenuItem("Deluxe Spicy McCrispy", 7.09, "chicken"),
    MenuItem("Chicken McNuggets (4p)", 2.89, "chicken"),
    MenuItem("Chicken McNuggets (6p)", 3.99, "chicken"),
    MenuItem("Chicken McNuggets (10p)", 6.39, "chicken"),
    MenuItem("Chicken McNuggets (20p)", 8.49, "chicken"),
    MenuItem("Chicken McNuggets (40p)", 14.79, "chicken"),
    MenuItem("McChicken", 3.69, "chicken"),

    #FISH (3 ITEMS)
    MenuItem("Filet-O-Fish", 5.79, "fish"),
    MenuItem("Double Filet-O-Fish", 7.39, "fish"),
    MenuItem("2 Filet-O-Fish", 7.00, "fish"),
    
    #FRIES (3 ITEMS)
    MenuItem("Small French Fries", 2.19, "fries"),
    MenuItem("Medium French Fries", 3.99, "fries"),
    MenuItem("Large French Fries", 4.99, "fries"),

    #HAPPY MEAL (3 ITEMS)
    MenuItem("Hamburger Happy Meal", 5.29, "happy_meal"),
    MenuItem("Chicken McNugget (4p) Happy Meal", 5.49, "happy_meal"),
    MenuItem("Chicken McNugget (6p) Happy Meal", 6.29, "happy_meal"),

    #DESSERT/SHAKES (15 ITEMS)
    MenuItem("Chocolate Shake", 4.79, "dessert/shakes"),
    MenuItem("Strawberry Shake", 4.79, "dessert/shakes"),
    MenuItem("Vanilla Shake", 4.79, "dessert/shakes"),
    MenuItem("M&M McFlurry", 4.99, "dessert/shakes"),
    MenuItem("OREO McFlurry", 4.99, "dessert/shakes"),
    MenuItem("Caramel Sundae", 4.49, "dessert/shakes"),
    MenuItem("Hot Fudge Sundae", 4.49, "dessert/shakes"),
    MenuItem("Plain Sundae", 4.49, "dessert/shakes"),
    MenuItem("3 Pack of Cookies", 2.99, "dessert/shakes"),
    MenuItem("13 Cookie Tots", 5.99, "dessert/shakes"),
    MenuItem("Apple Pie", 1.89, "dessert/shakes"),
    MenuItem("Strawberry & Creme Pie", 2.29, "dessert/shakes"),
    MenuItem("2 Apple Pies", 2.99, "dessert/shakes"),
    MenuItem("2 Strawberry & Creme Pies", 3.29, "dessert/shakes"),
    MenuItem("Vanilla Cone", 2.59, "dessert/shakes")
]

# ------------- App Logic -------------
def find_best_combo(items, budget):
    from itertools import combinations
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

# ------------- GUI Screens -------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("McDonald's Order Optimizer")
        self.geometry("650x540")

        self.selected_categories = {}
        self.budget = 0
        self.frames = {}

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        for F in (WelcomeScreen, BudgetScreen, CategoryScreen, ScoringScreen, ResultScreen):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomeScreen)

    def show_frame(self, screen_class):
        frame = self.frames[screen_class]
        frame.tkraise()

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Welcome to McDonald's Order Optimizer!", font=ctk.CTkFont(size=20)).pack(pady=50)
        ctk.CTkButton(self, text="Begin Choosing Order", command=lambda: controller.show_frame(BudgetScreen)).pack()

class BudgetScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ctk.CTkLabel(self, text="Enter your budget ($):", font=ctk.CTkFont(size=16)).pack(pady=20)
        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=10)
        ctk.CTkButton(self, text="Next", command=self.save_and_continue).pack(pady=20)

    def save_and_continue(self):
        try:
            self.controller.budget = float(self.entry.get())
            self.controller.show_frame(CategoryScreen)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

class CategoryScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.buttons = {}

        ctk.CTkLabel(self, text="Which of these do you feel like eating?", font=ctk.CTkFont(size=16)).pack(pady=10)
        categories = ["burger", "chicken", "fish", "fries", "happy_meal", "dessert/shakes"]
        for cat in categories:
            frame = ctk.CTkFrame(self)
            frame.pack(pady=5)
            ctk.CTkLabel(frame, text=cat.replace("_", " ").title(), width=200, anchor='w').pack(side="left", padx=10)
            yes_btn = ctk.CTkButton(frame, text="Yes", command=lambda c=cat: self.select(c, True))
            yes_btn.pack(side="left", padx=5)
            no_btn = ctk.CTkButton(frame, text="No", command=lambda c=cat: self.select(c, False))
            no_btn.pack(side="left", padx=5)
            self.buttons[cat] = (yes_btn, no_btn)

        ctk.CTkButton(self, text="Continue", command=self.save_and_continue).pack(pady=20)

    def select(self, category, value):
        self.controller.selected_categories[category] = value
        yes_btn, no_btn = self.buttons[category]
        if value:
            yes_btn.configure(state="disabled")
            no_btn.configure(state="disabled")
        else:
            yes_btn.configure(state="disabled")
            no_btn.configure(state="disabled")

    def save_and_continue(self):
        self.controller.frames[ScoringScreen].load_items()
        self.controller.show_frame(ScoringScreen)

class ScoringScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.index = 0
        self.items = []
        self.scores = {}
        self.timer_id = None
        self.time_left = 5

        self.label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=16), wraplength=600)
        self.label.pack(pady=30)

        self.timer_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.timer_label.pack()

        self.entry = ctk.CTkEntry(self, width=100)
        self.entry.pack(pady=10)

        self.next_button = ctk.CTkButton(self, text="Next", command=self.manual_score)
        self.next_button.pack(pady=20)

    def load_items(self):
        self.items = [item for item in menu_items if self.controller.selected_categories.get(item.category)]
        random.shuffle(self.items)
        self.index = 0
        self.scores = {}
        self.show_next_item()

    def show_next_item(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)

        if self.index < len(self.items):
            item = self.items[self.index]
            self.label.configure(text=f"{item.name}\nHow yummy does this sound? (0-10)")
            self.entry.delete(0, "end")
            self.time_left = 5
            self.update_timer()
        else:
            scored_items = []
            for item in self.items:
                score = self.scores.get(item.name, 0)
                if score > 0:
                    scored_items.append(ScoredMenuItem(item.name, item.price, item.category, score))

            # Limit to top 20 items by score to avoid combinatorial explosion
            scored_items.sort(key=lambda x: x.score, reverse=True)
            scored_items = scored_items[:20]

            self.controller.frames[ResultScreen].set_results(scored_items)
            self.controller.show_frame(ResultScreen) 

    def update_timer(self):
        self.timer_label.configure(text=f"Time left to rate: {self.time_left} seconds")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.after(1000, self.update_timer)
        else:
            self.auto_score()

    def manual_score(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)

        try:
            score = int(self.entry.get())
            if not 0 <= score <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a score between 0 and 10.")
            self.update_timer()
            return

        self.scores[self.items[self.index].name] = score
        self.index += 1
        self.show_next_item()

    def auto_score(self):
        self.scores[self.items[self.index].name] = 5  # default score
        self.index += 1
        self.show_next_item()

class ResultScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.textbox = ctk.CTkTextbox(self, width=650, height=500)
        self.textbox.pack(pady=20)
        self.textbox.configure(state="disabled")

    def set_results(self, scored_items):
        budget = self.controller.budget
        best_combo = find_best_combo(scored_items, budget)

        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")

        if best_combo:
            self.textbox.insert("end", "Best Combo:\n")
            for item in best_combo:
                self.textbox.insert("end", f"{item.name} - ${item.price:.2f} | Score: {item.score}\n")
            total_price = sum(i.price for i in best_combo)
            total_score = sum(i.score for i in best_combo)
            self.textbox.insert("end", f"\nTotal Price: ${total_price:.2f}\nTotal Score: {total_score}")
        else:
            self.textbox.insert("end", "No valid combo under your budget.")

        self.textbox.configure(state="disabled")

if __name__ == "__main__":
    app = App()
    app.mainloop()
