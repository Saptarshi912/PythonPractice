import json
from abc import ABC, abstractmethod
from typing import Dict, Optional


# Product: The complex object to be built
class Computer:
    def __init__(self, computer_type: str):
        self.computer_type = computer_type
        self.cpu = None
        self.motherboard = None
        self.ram = None
        self.storage = None
        self.graphics_card = None
        self.power_supply = None
        self.cooling_system = None
        self.price = 0.0

    def __str__(self):
        return (f"{self.computer_type} Configuration:\n"
                f"  CPU: {self.cpu or 'Not specified'}\n"
                f"  Motherboard: {self.motherboard or 'Not specified'}\n"
                f"  RAM: {self.ram or 'Not specified'}\n"
                f"  Storage: {self.storage or 'Not specified'}\n"
                f"  Graphics Card: {self.graphics_card or 'Not specified'}\n"
                f"  Power Supply: {self.power_supply or 'Not specified'}\n"
                f"  Cooling System: {self.cooling_system or 'Not specified'}\n"
                f"  Total Price: ${self.price:.2f}")

    def to_dict(self) -> Dict:
        return {
            "computer_type": self.computer_type,
            "cpu": self.cpu,
            "motherboard": self.motherboard,
            "ram": self.ram,
            "storage": self.storage,
            "graphics_card": self.graphics_card,
            "power_supply": self.power_supply,
            "cooling_system": self.cooling_system,
            "price": self.price
        }


# Abstract Builder: Defines the interface for building computers
class ComputerBuilder(ABC):
    def __init__(self, computer_type: str):
        self.computer = Computer(computer_type)
        self.component_prices = {
            "Intel Core i9-13900K": 600.00,
            "AMD Ryzen 7 5800X": 350.00,
            "Intel Core i5-12400": 200.00,
            "ASUS ROG Z790": 400.00,
            "Gigabyte B550": 150.00,
            "ASUS TUF B660": 180.00,
            "32GB DDR5": 200.00,
            "16GB DDR4": 80.00,
            "8GB DDR4": 40.00,
            "1TB NVMe SSD": 100.00,
            "2TB HDD": 60.00,
            "512GB SSD": 50.00,
            "NVIDIA RTX 4090": 1500.00,
            "AMD Radeon RX 6700 XT": 400.00,
            "850W PSU": 120.00,
            "650W PSU": 80.00,
            "Liquid Cooling": 150.00,
            "Air Cooling": 50.00
        }

    @abstractmethod
    def set_cpu(self, cpu: str):
        pass

    @abstractmethod
    def set_motherboard(self, motherboard: str):
        pass

    @abstractmethod
    def set_ram(self, ram: str):
        pass

    @abstractmethod
    def set_storage(self, storage: str):
        pass

    @abstractmethod
    def set_graphics_card(self, graphics_card: Optional[str]):
        pass

    @abstractmethod
    def set_power_supply(self, power_supply: str):
        pass

    @abstractmethod
    def set_cooling_system(self, cooling_system: str):
        pass

    def build(self):
        return self.computer

    def save_to_file(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(self.computer.to_dict(), f, indent=4)
        print(f"Configuration saved to {filename}")


# Concrete Builder: Desktop Computer Builder
class DesktopBuilder(ComputerBuilder):
    def __init__(self):
        super().__init__("Desktop")

    def set_cpu(self, cpu: str):
        if cpu not in ["Intel Core i9-13900K", "AMD Ryzen 7 5800X", "Intel Core i5-12400"]:
            raise ValueError(f"Unsupported CPU: {cpu}")
        self.computer.cpu = cpu
        self.computer.price += self.component_prices.get(cpu, 0)
        return self

    def set_motherboard(self, motherboard: str):
        compatible_motherboards = {
            "Intel Core i9-13900K": ["ASUS ROG Z790", "ASUS TUF B660"],
            "AMD Ryzen 7 5800X": ["Gigabyte B550"],
            "Intel Core i5-12400": ["ASUS TUF B660"]
        }
        cpu = self.computer.cpu
        if cpu and motherboard not in compatible_motherboards.get(cpu, []):
            raise ValueError(f"Motherboard {motherboard} is not compatible with CPU {cpu}")
        self.computer.motherboard = motherboard
        self.computer.price += self.component_prices.get(motherboard, 0)
        return self

    def set_ram(self, ram: str):
        if ram not in ["32GB DDR5", "16GB DDR4", "8GB DDR4"]:
            raise ValueError(f"Unsupported RAM: {ram}")
        self.computer.ram = ram
        self.computer.price += self.component_prices.get(ram, 0)
        return self

    def set_storage(self, storage: str):
        if storage not in ["1TB NVMe SSD", "2TB HDD", "512GB SSD"]:
            raise ValueError(f"Unsupported storage: {storage}")
        self.computer.storage = storage
        self.computer.price += self.component_prices.get(storage, 0)
        return self

    def set_graphics_card(self, graphics_card: Optional[str]):
        if graphics_card and graphics_card not in ["NVIDIA RTX 4090", "AMD Radeon RX 6700 XT"]:
            raise ValueError(f"Unsupported graphics card: {graphics_card}")
        self.computer.graphics_card = graphics_card
        if graphics_card:
            self.computer.price += self.component_prices.get(graphics_card, 0)
        return self

    def set_power_supply(self, power_supply: str):
        if power_supply not in ["850W PSU", "650W PSU"]:
            raise ValueError(f"Unsupported power supply: {power_supply}")
        self.computer.power_supply = power_supply
        self.computer.price += self.component_prices.get(power_supply, 0)
        return self

    def set_cooling_system(self, cooling_system: str):
        if cooling_system not in ["Liquid Cooling", "Air Cooling"]:
            raise ValueError(f"Unsupported cooling system: {cooling_system}")
        self.computer.cooling_system = cooling_system
        self.computer.price += self.component_prices.get(cooling_system, 0)
        return self


# Concrete Builder: Laptop Computer Builder
class LaptopBuilder(ComputerBuilder):
    def __init__(self):
        super().__init__("Laptop")

    def set_cpu(self, cpu: str):
        if cpu not in ["Intel Core i5-12400"]:
            raise ValueError(f"Unsupported CPU for laptop: {cpu}")
        self.computer.cpu = cpu
        self.computer.price += self.component_prices.get(cpu, 0)
        return self

    def set_motherboard(self, motherboard: str):
        if motherboard != "ASUS TUF B660":
            raise ValueError(f"Unsupported motherboard for laptop: {motherboard}")
        self.computer.motherboard = motherboard
        self.computer.price += self.component_prices.get(motherboard, 0)
        return self

    def set_ram(self, ram: str):
        if ram not in ["16GB DDR4", "8GB DDR4"]:
            raise ValueError(f"Unsupported RAM for laptop: {ram}")
        self.computer.ram = ram
        self.computer.price += self.component_prices.get(ram, 0)
        return self

    def set_storage(self, storage: str):
        if storage not in ["512GB SSD"]:
            raise ValueError(f"Unsupported storage for laptop: {storage}")
        self.computer.storage = storage
        self.computer.price += self.component_prices.get(storage, 0)
        return self

    def set_graphics_card(self, graphics_card: Optional[str]):
        # Laptops typically have integrated graphics
        self.computer.graphics_card = graphics_card or "Integrated Graphics"
        if graphics_card and graphics_card != "Integrated Graphics":
            raise ValueError("Laptops only support integrated graphics")
        return self

    def set_power_supply(self, power_supply: str):
        if power_supply != "Built-in Battery":
            raise ValueError(f"Unsupported power supply for laptop: {power_supply}")
        self.computer.power_supply = power_supply
        self.computer.price += 100.00  # Fixed cost for built-in battery
        return self

    def set_cooling_system(self, cooling_system: str):
        if cooling_system != "Air Cooling":
            raise ValueError(f"Unsupported cooling system for laptop: {cooling_system}")
        self.computer.cooling_system = cooling_system
        self.computer.price += self.component_prices.get(cooling_system, 0)
        return self


# Director: Provides predefined configurations
class ComputerDirector:
    @staticmethod
    def build_high_end_desktop(builder: ComputerBuilder):
        return (builder
                .set_cpu("Intel Core i9-13900K")
                .set_motherboard("ASUS ROG Z790")
                .set_ram("32GB DDR5")
                .set_storage("1TB NVMe SSD")
                .set_graphics_card("NVIDIA RTX 4090")
                .set_power_supply("850W PSU")
                .set_cooling_system("Liquid Cooling")
                .build())

    @staticmethod
    def build_budget_desktop(builder: ComputerBuilder):
        return (builder
                .set_cpu("Intel Core i5-12400")
                .set_motherboard("ASUS TUF B660")
                .set_ram("8GB DDR4")
                .set_storage("512GB SSD")
                .set_graphics_card(None)
                .set_power_supply("650W PSU")
                .set_cooling_system("Air Cooling")
                .build())

    @staticmethod
    def build_standard_laptop(builder: ComputerBuilder):
        return (builder
                .set_cpu("Intel Core i5-12400")
                .set_motherboard("ASUS TUF B660")
                .set_ram("16GB DDR4")
                .set_storage("512GB SSD")
                .set_graphics_card(None)
                .set_power_supply("Built-in Battery")
                .set_cooling_system("Air Cooling")
                .build())


# Client code: Interactive CLI for building computers
def interactive_builder():
    print("Welcome to the Custom Computer Builder!")
    computer_type = input("Choose computer type (desktop/laptop): ").lower()

    if computer_type == "desktop":
        builder = DesktopBuilder()
    elif computer_type == "laptop":
        builder = LaptopBuilder()
    else:
        print("Invalid computer type. Defaulting to Desktop.")
        builder = DesktopBuilder()

    print("\nAvailable configurations: high_end_desktop, budget_desktop, standard_laptop, custom")
    config_type = input("Choose a configuration or 'custom' to build manually: ").lower()

    try:
        if config_type == "high_end_desktop" and isinstance(builder, DesktopBuilder):
            computer = ComputerDirector.build_high_end_desktop(builder)
        elif config_type == "budget_desktop" and isinstance(builder, DesktopBuilder):
            computer = ComputerDirector.build_budget_desktop(builder)
        elif config_type == "standard_laptop" and isinstance(builder, LaptopBuilder):
            computer = ComputerDirector.build_standard_laptop(builder)
        elif config_type == "custom":
            print("\nCustom Configuration:")
            if isinstance(builder, DesktopBuilder):
                cpu = input("Enter CPU (Intel Core i9-13900K, AMD Ryzen 7 5800X, Intel Core i5-12400): ")
                motherboard = input("Enter Motherboard (ASUS ROG Z790, Gigabyte B550, ASUS TUF B660): ")
                ram = input("Enter RAM (32GB DDR5, 16GB DDR4, 8GB DDR4): ")
                storage = input("Enter Storage (1TB NVMe SSD, 2TB HDD, 512GB SSD): ")
                graphics = input("Enter Graphics Card (NVIDIA RTX 4090, AMD Radeon RX 6700 XT, or None): ")
                power_supply = input("Enter Power Supply (850W PSU, 650W PSU): ")
                cooling = input("Enter Cooling System (Liquid Cooling, Air Cooling): ")
            else:  # Laptop
                cpu = input("Enter CPU (Intel Core i5-12400): ")
                motherboard = input("Enter Motherboard (ASUS TUF B660): ")
                ram = input("Enter RAM (16GB DDR4, 8GB DDR4): ")
                storage = input("Enter Storage (512GB SSD): ")
                graphics = input("Enter Graphics Card (Integrated Graphics): ")
                power_supply = input("Enter Power Supply (Built-in Battery): ")
                cooling = input("Enter Cooling System (Air Cooling): ")

            computer = (builder
                        .set_cpu(cpu)
                        .set_motherboard(motherboard)
                        .set_ram(ram)
                        .set_storage(storage)
                        .set_graphics_card(None if graphics.lower() == "none" else graphics)
                        .set_power_supply(power_supply)
                        .set_cooling_system(cooling)
                        .build())
        else:
            raise ValueError("Invalid configuration for the selected computer type.")

        print("\nFinal Configuration:")
        print(computer)
        save = input("\nSave configuration to file? (yes/no): ").lower()
        if save == "yes":
            filename = input("Enter filename (e.g., config.json): ")
            builder.save_to_file(filename)

    except ValueError as e:
        print(f"Error: {e}")


# Example usage
if __name__ == "__main__":
    # Run interactive builder
    interactive_builder()

    # Example programmatic usage
    print("\nProgrammatic Example:")
    desktop_builder = DesktopBuilder()
    laptop_builder = LaptopBuilder()

    print("\nHigh-End Desktop:")
    high_end_desktop = ComputerDirector.build_high_end_desktop(desktop_builder)
    print(high_end_desktop)
    desktop_builder.save_to_file("high_end_desktop.json")

    print("\nStandard Laptop:")
    standard_laptop = ComputerDirector.build_standard_laptop(laptop_builder)
    print(standard_laptop)
    laptop_builder.save_to_file("standard_laptop.json")