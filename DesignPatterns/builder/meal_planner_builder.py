import json
from abc import ABC, abstractmethod
from typing import Dict, Optional, List

# Product: The complex object to be built
class MealPlan:
    def __init__(self, plan_type: str):
        self.plan_type = plan_type
        self.dietary_preference = None
        self.breakfast = None
        self.lunch = None
        self.dinner = None
        self.snacks = []
        self.total_calories = 0
        self.macros = {"protein": 0, "carbs": 0, "fat": 0}

    def __str__(self):
        snacks_str = ", ".join(self.snacks) if self.snacks else "None"
        return (f"{self.plan_type} Meal Plan:\n"
                f"  Dietary Preference: {self.dietary_preference or 'Not specified'}\n"
                f"  Breakfast: {self.breakfast or 'Not specified'}\n"
                f"  Lunch: {self.lunch or 'Not specified'}\n"
                f"  Dinner: {self.dinner or 'Not specified'}\n"
                f"  Snacks: {snacks_str}\n"
                f"  Total Calories: {self.total_calories} kcal\n"
                f"  Macronutrients: Protein {self.macros['protein']}g, Carbs {self.macros['carbs']}g, Fat {self.macros['fat']}g")

    def to_dict(self) -> Dict:
        return {
            "plan_type": self.plan_type,
            "dietary_preference": self.dietary_preference,
            "breakfast": self.breakfast,
            "lunch": self.lunch,
            "dinner": self.dinner,
            "snacks": self.snacks,
            "total_calories": self.total_calories,
            "macros": self.macros
        }

# Abstract Builder: Defines the interface for building meal plans
class MealPlanBuilder(ABC):
    def __init__(self, plan_type: str):
        self.meal_plan = MealPlan(plan_type)
        self.meal_data = {
            "Vegan Oatmeal": {"calories": 300, "macros": {"protein": 8, "carbs": 50, "fat": 6}},
            "Grilled Chicken Salad": {"calories": 400, "macros": {"protein": 30, "carbs": 20, "fat": 15}},
            "Salmon with Quinoa": {"calories": 500, "macros": {"protein": 35, "carbs": 40, "fat": 20}},
            "Tofu Stir-Fry": {"calories": 350, "macros": {"protein": 15, "carbs": 30, "fat": 10}},
            "Keto Avocado Bowl": {"calories": 450, "macros": {"protein": 10, "carbs": 5, "fat": 40}},
            "Fruit Salad": {"calories": 150, "macros": {"protein": 2, "carbs": 35, "fat": 1}},
            "Nuts": {"calories": 200, "macros": {"protein": 5, "carbs": 10, "fat": 15}},
            "Protein Bar": {"calories": 250, "macros": {"protein": 20, "carbs": 15, "fat": 10}}
        }
        self.dietary_compatibility = {
            "vegan": ["Vegan Oatmeal", "Tofu Stir-Fry", "Fruit Salad"],
            "keto": ["Keto Avocado Bowl", "Nuts"],
            "gluten-free": ["Vegan Oatmeal", "Grilled Chicken Salad", "Salmon with Quinoa", "Tofu Stir-Fry", "Keto Avocado Bowl", "Fruit Salad", "Nuts"]
        }

    @abstractmethod
    def set_dietary_preference(self, preference: str):
        pass

    @abstractmethod
    def set_breakfast(self, breakfast: str):
        pass

    @abstractmethod
    def set_lunch(self, lunch: str):
        pass

    @abstractmethod
    def set_dinner(self, dinner: str):
        pass

    @abstractmethod
    def add_snack(self, snack: str):
        pass

    def build(self):
        return self.meal_plan

    def save_to_file(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(self.meal_plan.to_dict(), f, indent=4)
        print(f"Meal plan saved to {filename}")

    def _update_nutrition(self, meal: str):
        if meal in self.meal_data:
            self.meal_plan.total_calories += self.meal_data[meal]["calories"]
            for macro, value in self.meal_data[meal]["macros"].items():
                self.meal_plan.macros[macro] += value

    def _check_dietary_compatibility(self, meal: str, preference: str):
        if preference and meal not in self.dietary_compatibility.get(preference, []):
            raise ValueError(f"{meal} is not compatible with {preference} diet")

# Concrete Builder: Standard Meal Plan Builder
class StandardMealPlanBuilder(MealPlanBuilder):
    def __init__(self):
        super().__init__("Standard")

    def set_dietary_preference(self, preference: str):
        if preference not in ["vegan", "keto", "gluten-free", "none"]:
            raise ValueError(f"Unsupported dietary preference: {preference}")
        self.meal_plan.dietary_preference = preference if preference != "none" else None
        return self

    def set_breakfast(self, breakfast: str):
        if breakfast not in self.meal_data:
            raise ValueError(f"Unsupported breakfast: {breakfast}")
        self._check_dietary_compatibility(breakfast, self.meal_plan.dietary_preference)
        self.meal_plan.breakfast = breakfast
        self._update_nutrition(breakfast)
        return self

    def set_lunch(self, lunch: str):
        if lunch not in self.meal_data:
            raise ValueError(f"Unsupported lunch: {lunch}")
        self._check_dietary_compatibility(lunch, self.meal_plan.dietary_preference)
        self.meal_plan.lunch = lunch
        self._update_nutrition(lunch)
        return self

    def set_dinner(self, dinner: str):
        if dinner not in self.meal_data:
            raise ValueError(f"Unsupported dinner: {dinner}")
        self._check_dietary_compatibility(dinner, self.meal_plan.dietary_preference)
        self.meal_plan.dinner = dinner
        self._update_nutrition(dinner)
        return self

    def add_snack(self, snack: str):
        if snack not in self.meal_data:
            raise ValueError(f"Unsupported snack: {snack}")
        self._check_dietary_compatibility(snack, self.meal_plan.dietary_preference)
        self.meal_plan.snacks.append(snack)
        self._update_nutrition(snack)
        return self

# Concrete Builder: Premium Meal Plan Builder
class PremiumMealPlanBuilder(MealPlanBuilder):
    def __init__(self):
        super().__init__("Premium")

    def set_dietary_preference(self, preference: str):
        if preference not in ["vegan", "keto", "gluten-free"]:
            raise ValueError(f"Premium plans require a specific dietary preference: {preference}")
        self.meal_plan.dietary_preference = preference
        return self

    def set_breakfast(self, breakfast: str):
        if breakfast not in self.meal_data:
            raise ValueError(f"Unsupported breakfast: {breakfast}")
        self._check_dietary_compatibility(breakfast, self.meal_plan.dietary_preference)
        self.meal_plan.breakfast = breakfast
        self._update_nutrition(breakfast)
        return self

    def set_lunch(self, lunch: str):
        if lunch not in self.meal_data:
            raise ValueError(f"Unsupported lunch: {lunch}")
        self._check_dietary_compatibility(lunch, self.meal_plan.dietary_preference)
        self.meal_plan.lunch = lunch
        self._update_nutrition(lunch)
        return self

    def set_dinner(self, dinner: str):
        if dinner not in self.meal_data:
            raise ValueError(f"Unsupported dinner: {dinner}")
        self._check_dietary_compatibility(dinner, self.meal_plan.dietary_preference)
        self.meal_plan.dinner = dinner
        self._update_nutrition(dinner)
        return self

    def add_snack(self, snack: str):
        if len(self.meal_plan.snacks) >= 2:
            raise ValueError("Premium plan allows a maximum of 2 snacks")
        if snack not in self.meal_data:
            raise ValueError(f"Unsupported snack: {snack}")
        self._check_dietary_compatibility(snack, self.meal_plan.dietary_preference)
        self.meal_plan.snacks.append(snack)
        self._update_nutrition(snack)
        return self

# Director: Provides predefined meal plans
class MealPlanDirector:
    @staticmethod
    def build_vegan_plan(builder: MealPlanBuilder):
        return (builder
                .set_dietary_preference("vegan")
                .set_breakfast("Vegan Oatmeal")
                .set_lunch("Tofu Stir-Fry")
                .set_dinner("Tofu Stir-Fry")
                .add_snack("Fruit Salad")
                .build())

    @staticmethod
    def build_keto_plan(builder: MealPlanBuilder):
        return (builder
                .set_dietary_preference("keto")
                .set_breakfast("Keto Avocado Bowl")
                .set_lunch("Keto Avocado Bowl")
                .set_dinner("Keto Avocado Bowl")
                .add_snack("Nuts")
                .build())

    @staticmethod
    def build_gluten_free_plan(builder: MealPlanBuilder):
        return (builder
                .set_dietary_preference("gluten-free")
                .set_breakfast("Vegan Oatmeal")
                .set_lunch("Grilled Chicken Salad")
                .set_dinner("Salmon with Quinoa")
                .add_snack("Fruit Salad")
                .add_snack("Nuts")
                .build())

# Client code: Interactive CLI for building meal plans
def interactive_builder():
    print("Welcome to the Meal Planner!")
    plan_type = input("Choose plan type (standard/premium): ").lower()

    if plan_type == "standard":
        builder = StandardMealPlanBuilder()
    elif plan_type == "premium":
        builder = PremiumMealPlanBuilder()
    else:
        print("Invalid plan type. Defaulting to Standard.")
        builder = StandardMealPlanBuilder()

    print("\nAvailable configurations: vegan, keto, gluten-free, custom")
    config_type = input("Choose a configuration or 'custom' to build manually: ").lower()

    try:
        if config_type == "vegan":
            meal_plan = MealPlanDirector.build_vegan_plan(builder)
        elif config_type == "keto" and isinstance(builder, PremiumMealPlanBuilder):
            meal_plan = MealPlanDirector.build_keto_plan(builder)
        elif config_type == "gluten-free":
            meal_plan = MealPlanDirector.build_gluten_free_plan(builder)
        elif config_type == "custom":
            print("\nCustom Configuration:")
            if isinstance(builder, StandardMealPlanBuilder):
                preference = input("Enter dietary preference (vegan, keto, gluten-free, none): ")
            else:
                preference = input("Enter dietary preference (vegan, keto, gluten-free): ")
            breakfast = input("Enter breakfast (Vegan Oatmeal, Grilled Chicken Salad, Salmon with Quinoa, Tofu Stir-Fry, Keto Avocado Bowl): ")
            lunch = input("Enter lunch (Vegan Oatmeal, Grilled Chicken Salad, Salmon with Quinoa, Tofu Stir-Fry, Keto Avocado Bowl): ")
            dinner = input("Enter dinner (Vegan Oatmeal, Grilled Chicken Salad, Salmon with Quinoa, Tofu Stir-Fry, Keto Avocado Bowl): ")
            snacks = input("Enter snacks (comma-separated, e.g., Fruit Salad,Nuts; max 2 for premium): ").split(",")

            meal_plan = builder.set_dietary_preference(preference)
            meal_plan = meal_plan.set_breakfast(breakfast)
            meal_plan = meal_plan.set_lunch(lunch)
            meal_plan = meal_plan.set_dinner(dinner)
            for snack in [s.strip() for s in snacks if s.strip()]:
                meal_plan = meal_plan.add_snack(snack)
            meal_plan = meal_plan.build()
        else:
            raise ValueError("Invalid configuration for the selected plan type.")

        print("\nFinal Meal Plan:")
        print(meal_plan)
        save = input("\nSave meal plan to file? (yes/no): ").lower()
        if save == "yes":
            filename = input("Enter filename (e.g., meal_plan.json): ")
            builder.save_to_file(filename)

    except ValueError as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    # Run interactive builder
    interactive_builder()

    # Example programmatic usage
    print("\nProgrammatic Example:")
    standard_builder = StandardMealPlanBuilder()
    premium_builder = PremiumMealPlanBuilder()

    print("\nVegan Standard Plan:")
    vegan_plan = MealPlanDirector.build_vegan_plan(standard_builder)
    print(vegan_plan)
    standard_builder.save_to_file("vegan_plan.json")

    print("\nKeto Premium Plan:")
    keto_plan = MealPlanDirector.build_keto_plan(premium_builder)
    print(keto_plan)
    premium_builder.save_to_file("keto_plan.json")