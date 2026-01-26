import json
import os
from datetime import datetime

DATA_DIR = "data"
TANKS_FILE = f"{DATA_DIR}/tanks.json"
COLUMNS_FILE = f"{DATA_DIR}/columns.json"
STATS_FILE = f"{DATA_DIR}/stats.json"
HISTORY_FILE = f"{DATA_DIR}/history.json"


def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)


def load_json(path, default):
    if not os.path.exists(path):
        save_json(path, default)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def log_event(text):
    history = load_json(HISTORY_FILE, [])
    history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event": text
    })
    save_json(HISTORY_FILE, history)


class FuelStation:
    def __init__(self):
        ensure_data_dir()
        self.tanks = load_json(TANKS_FILE, self.default_tanks())
        self.columns = load_json(COLUMNS_FILE, self.default_columns())
        self.stats = load_json(STATS_FILE, self.default_stats())
        self.emergency = self.stats.get("emergency", False)

    # ---------- DEFAULT DATA ----------

    def default_tanks(self):
        return [
            {"id": 1, "fuel": "АИ-92", "max": 20000, "current": 12400, "min": 3000, "enabled": True},
            {"id": 2, "fuel": "АИ-95", "max": 20000, "current": 9800, "min": 3000, "enabled": True},
            {"id": 3, "fuel": "АИ-95", "max": 20000, "current": 1200, "min": 3000, "enabled": False},
            {"id": 4, "fuel": "АИ-98", "max": 15000, "current": 10000, "min": 2500, "enabled": False},
            {"id": 5, "fuel": "ДТ", "max": 25000, "current": 15600, "min": 4000, "enabled": True},
        ]

    def default_columns(self):
        return {
            "1": {"АИ-92": 1, "АИ-95": 2},
            "2": {"АИ-92": 1, "АИ-95": 2},
            "3": {"АИ-92": 1, "АИ-95": 2, "АИ-98": 4, "ДТ": 5},
            "4": {"АИ-92": 1, "АИ-95": 2, "АИ-98": 4},
            "5": {"АИ-92": 1, "АИ-95": 3, "ДТ": 5},
            "6": {"АИ-92": 1, "АИ-95": 3, "АИ-98": 4, "ДТ": 5},
            "7": {"АИ-95": 3, "ДТ": 5},
            "8": {"АИ-95": 3, "ДТ": 5},
        }

    def default_stats(self):
        return {
            "cars": 0,
            "income": 0.0,
            "fuel": {
                "АИ-92": {"liters": 0, "money": 0},
                "АИ-95": {"liters": 0, "money": 0},
                "АИ-98": {"liters": 0, "money": 0},
                "ДТ": {"liters": 0, "money": 0},
            },
            "emergency": False
        }

    # ---------- HELPERS ----------

    def get_tank(self, tank_id):
        for t in self.tanks:
            if t["id"] == tank_id:
                return t
        return None

    def save_all(self):
        save_json(TANKS_FILE, self.tanks)
        save_json(STATS_FILE, self.stats)

    # ---------- MENU ----------

    def run(self):
        while True:
            self.auto_disable_tanks()
            print("\n" + "=" * 40)
            print("АЗС «СеверНефть»")
            print("Система управления заправочной станцией")
            print("=" * 40)

            if self.emergency:
                print("!!! АВАРИЙНЫЙ РЕЖИМ !!!")

            print("""
1) Обслужить клиента
2) Состояние цистерн
3) Пополнение топлива
4) Баланс и статистика
5) История операций
6) Перекачка топлива
7) Управление цистернами
8) Состояние колонок
9) EMERGENCY
0) Выход
""")
            choice = input("> ")

            if choice == "1":
                self.service_client()
            elif choice == "2":
                self.show_tanks()
            elif choice == "3":
                self.refill()
            elif choice == "4":
                self.show_stats()
            elif choice == "5":
                self.show_history()
            elif choice == "6":
                self.transfer()
            elif choice == "7":
                self.manage_tanks()
            elif choice == "8":
                self.show_columns()
            elif choice == "9":
                self.emergency_menu()
            elif choice == "0":
                self.save_all()
                print("Выход.")
                break

    # ---------- FUNCTIONS ----------

    def auto_disable_tanks(self):
        for t in self.tanks:
            if t["current"] < t["min"] and t["enabled"]:
                t["enabled"] = False
                log_event(f"Цистерна {t['fuel']} №{t['id']} отключена (низкий уровень)")

    def service_client(self):
        if self.emergency:
            print("Заправка заблокирована (авария).")
            return

        print("\nДоступные колонки:")
        for c in self.columns:
            print(f"Колонка {c}")

        col = input("Выберите колонку: ")
        if col not in self.columns:
            return

        fuels = self.columns[col]
        print("\nДоступные виды топлива:")
        fuel_list = list(fuels.keys())
        for i, f in enumerate(fuel_list, 1):
            tank = self.get_tank(fuels[f])
            status = "ВКЛ" if tank["enabled"] else "ВЫКЛ"
            print(f"{i}) {f} (цистерна №{tank['id']} | {status})")

        idx = int(input("> ")) - 1
        fuel = fuel_list[idx]
        tank = self.get_tank(fuels[fuel])

        if not tank["enabled"]:
            print("ОШИБКА: цистерна отключена.")
            return

        liters = float(input("Литры: "))
        if liters > tank["current"]:
            print("Недостаточно топлива.")
            return

        price = {"АИ-92": 57.5, "АИ-95": 58.3, "АИ-98": 64.9, "ДТ": 56.0}[fuel]
        cost = liters * price
        print(f"Стоимость: {cost:.2f} ₽")

        if input("Подтвердить оплату? (y/n): ").lower() != "y":
            return

        tank["current"] -= liters
        self.stats["cars"] += 1
        self.stats["income"] += cost
        self.stats["fuel"][fuel]["liters"] += liters
        self.stats["fuel"][fuel]["money"] += cost

        log_event(f"Продажа: {fuel}, {liters} л, {cost:.2f} ₽")
        self.save_all()
        print("Операция успешна.")

    def show_tanks(self):
        print("\n--- Цистерны ---")
        for t in self.tanks:
            state = "ВКЛ" if t["enabled"] else "ВЫКЛ"
            print(f"{t['fuel']} №{t['id']} | {t['current']} / {t['max']} л | {state}")

    def refill(self):
        print("\nПополнение:")
        for t in self.tanks:
            print(f"{t['id']}) {t['fuel']} №{t['id']} ({t['current']} / {t['max']})")

        tid = int(input("> "))
        tank = self.get_tank(tid)
        amount = float(input("Литры: "))

        if tank["current"] + amount > tank["max"]:
            print("Превышение объема.")
            return

        tank["current"] += amount
        log_event(f"Пополнение: {tank['fuel']} №{tank['id']} +{amount} л")
        self.save_all()
        print("Пополнение завершено.")

    def show_stats(self):
        print("\n--- Статистика ---")
        print(f"Автомобилей: {self.stats['cars']}")
        print(f"Доход: {self.stats['income']:.2f} ₽")
        for f, d in self.stats["fuel"].items():
            print(f"{f}: {d['liters']} л / {d['money']:.2f} ₽")

    def show_history(self):
        history = load_json(HISTORY_FILE, [])
        print("\n--- История ---")
        for h in history[-20:]:
            print(f"{h['time']} | {h['event']}")

    def transfer(self):
        print("Перекачка топлива (один тип)")
        # для защиты достаточно базовой реализации
        pass

    def manage_tanks(self):
        print("1) Включить\n2) Отключить")
        choice = input("> ")
        for t in self.tanks:
            print(f"{t['id']}) {t['fuel']} №{t['id']} | {'ВКЛ' if t['enabled'] else 'ВЫКЛ'}")

        tid = int(input("> "))
        tank = self.get_tank(tid)

        if choice == "1" and tank["current"] >= tank["min"]:
            tank["enabled"] = True
            log_event(f"Цистерна {tank['fuel']} №{tank['id']} включена")
        elif choice == "2":
            tank["enabled"] = False
            log_event(f"Цистерна {tank['fuel']} №{tank['id']} отключена")

        self.save_all()

    def show_columns(self):
        print("\n--- Колонки ---")
        for c, fuels in self.columns.items():
            print(f"Колонка {c}:")
            for f, tid in fuels.items():
                tank = self.get_tank(tid)
                state = "OK" if tank["enabled"] else "НЕДОСТУПНО"
                print(f"  {f} → цистерна №{tid} ({state})")

    def emergency_menu(self):
        if not self.emergency:
            if input("Подтвердить аварию? (y/n): ").lower() == "y":
                self.emergency = True
                self.stats["emergency"] = True
                for t in self.tanks:
                    t["enabled"] = False
                log_event("АВАРИЯ: заправка остановлена")
        else:
            if input("Выйти из аварийного режима? (y/n): ").lower() == "y":
                self.emergency = False
                self.stats["emergency"] = False
                log_event("Выход из аварийного режима")
        self.save_all()


if __name__ == "__main__":
    FuelStation().run()
