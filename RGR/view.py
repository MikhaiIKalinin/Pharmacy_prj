class View:
    def show_message(self, msg):
        print(f"\n>>> {msg}")

    def get_input(self, prompt):
        return input(prompt)

    def get_int(self, prompt, min_val=None, max_val=None):
        while True:
            try:
                v = int(input(prompt))
                if min_val is not None and v < min_val:
                    print("Value too small.")
                    continue
                if max_val is not None and v > max_val:
                    print("Value too large.")
                    continue
                return v
            except Exception:
                print("Invalid integer. Try again.")

    def get_float(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except Exception:
                print("Invalid float. Try again.")

    # simple show functions
    def show_error(self, err_code):
        if err_code == "FK_ERROR":
            print("\n[!] ПОМИЛКА: Неможливо видалити або додати запис.")
            print("    Причина: Порушення цілісності даних (Foreign Key).")
            print("    Якщо видаляєте: Спочатку видаліть залежні дані в інших таблицях.")
            print("    Якщо додаєте: Перевірте правильність ID батьківського запису.")

        elif err_code == "NOT_FOUND":
            print("\n[!] ПОМИЛКА: Запис із таким ID не знайдено.")
            print("    Нічого не було видалено.")

        else:
            print(f"\n[!] Error: {err_code}")

    def get_date(self, prompt):
        while True:
            val = input(prompt + " (YYYY-MM-DD): ")
            try:
                return val  # PostgreSQL прийме рядок 'YYYY-MM-DD', або можна парсити в datetime
            except ValueError:
                print("Invalid date format.")

    def show_pharmacies(self, rows):
        if not rows:
            print("No pharmacies.")
            return
        for r in rows:
            print(f"Id: {r[0]} | Name: {r[1]} | Adress: {r[2]}")

    def show_phonetypes(self, rows):
        if not rows:
            print("No phonetypes.")
            return
        for r in rows:
            print(f"Id: {r[0]} | Name: {r[1]}")

    def show_phones(self, rows):
        if not rows:
            print("No phones.")
            return
        for r in rows:
            print(f"Id: {r[0]} | Name: {r[1]} | PharmacyId: {r[2]} | PhoneTypeId: {r[3]}")

    def show_manufacturers(self, rows):
        if not rows:
            print("No manufacturers.")
            return
        for r in rows:
            print(f"Id: {r[0]} | Name: {r[1]}")

    def show_drugs(self, rows):
        if not rows:
            print("No drugs.")
            return
        for r in rows:
            print(f"Id: {r[0]} | Name: {r[1]} | ManufacturerId: {r[2]} | Price: {r[3]}")

    def show_availabilities(self, rows):
        if not rows:
            print("No availabilities.")
            return
        for r in rows:
            print(f"PharmacyId: {r[0]} | DrugId: {r[1]} | Quantity: {r[2]} | UpdatedAt: {r[3]}")

    def show_custom_results(self, title, headers, rows):
        print(f"\n--- {title} ---")
        if not rows:
            print("No results found.")
            return

        # Виводимо заголовки
        header_str = " | ".join(headers)
        print(header_str)
        print("-" * len(header_str))

        # Виводимо дані
        for r in rows:
            # Перетворюємо всі елементи в стрічки для друку
            row_str = " | ".join(str(x) for x in r)
            print(row_str)