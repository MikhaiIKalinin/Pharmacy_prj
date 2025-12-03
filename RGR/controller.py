from model import Model
from view import View


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def main_run(self):
        while True:
            self.view.show_message("\n=== MAIN MENU ===")
            self.view.show_message("1. Show data")
            self.view.show_message("2. Add data")
            self.view.show_message("3. Update data")
            self.view.show_message("4. Delete data")
            self.view.show_message("5. Generate data")
            self.view.show_message("6. SEARCH & ANALYTICS (Lab Task)")  # Добавлено
            self.view.show_message("7. Quit")

            choice = self.view.get_int("Enter choice: ", min_val=1, max_val=7)
            if choice == 1:
                self.show_menu()
            elif choice == 2:
                self.add_menu()
            elif choice == 3:
                self.update_menu()
            elif choice == 4:
                self.delete_menu()
            elif choice == 5:
                self.generate_menu()
            elif choice == 6:
                self.search_menu()
            elif choice == 7:
                self.view.show_message("Goodbye!")
                self.model.close()
                break

    # ---------------- show ----------------
    def show_menu(self):
        while True:
            self.view.show_message("\n-- SHOW MENU --")
            self.view.show_message("1. Pharmacies")
            self.view.show_message("2. PhoneTypes")
            self.view.show_message("3. Phones")
            self.view.show_message("4. Manufacturers")
            self.view.show_message("5. Drugs")
            self.view.show_message("6. Availabilities")
            self.view.show_message("7. Back")
            choice = self.view.get_int("Enter choice: ", 1, 7)
            if choice == 1:
                print("\n--- VIEW MODES ---")
                print("1. Show limit 50 (default)")
                print("2. Show ALL")
                print("3. Show ONE by ID")
                mode = self.view.get_int("Select mode: ", 1, 3)

                if mode == 1:
                    rows = self.model.get_pharmacies_limited()
                    self.view.show_pharmacies(rows)
                elif mode == 2:
                    rows = self.model.get_pharmacies()
                    self.view.show_pharmacies(rows)
                elif mode == 3:
                    id_val = self.view.get_int("Enter Pharmacy ID: ")
                    rows = self.model.get_pharmacy_by_id(id_val)
                    if rows:
                        self.view.show_pharmacies(rows)
                    else:
                        self.view.show_message("Pharmacy with this ID not found.")
            elif choice == 2:
                rows = self.model.get_phonetypes()
                self.view.show_phonetypes(rows)
            elif choice == 3:
                rows = self.model.get_phones()
                self.view.show_phones(rows)
            elif choice == 4:
                rows = self.model.get_manufacturers()
                self.view.show_manufacturers(rows)
            elif choice == 5:
                rows = self.model.get_drugs()
                self.view.show_drugs(rows)
            elif choice == 6:
                rows = self.model.get_availabilities()
                self.view.show_availabilities(rows)
            elif choice == 7:
                break

    # ---------------- add ----------------
    def add_menu(self):
        while True:
            self.view.show_message("\n-- ADD MENU --")
            self.view.show_message("1. Add Pharmacy")
            self.view.show_message("2. Add PhoneType")
            self.view.show_message("3. Add Phone")
            self.view.show_message("4. Add Manufacturer")
            self.view.show_message("5. Add Drug")
            self.view.show_message("6. Add Availability")
            self.view.show_message("7. Back")
            choice = self.view.get_int("Enter choice: ", 1, 7)

            status = None

            if choice == 1:
                name = self.view.get_input("Pharmacy name: ")
                addr = self.view.get_input("Address: ")
                status = self.model.add_pharmacy(name, addr)
            elif choice == 2:
                name = self.view.get_input("PhoneType name: ")
                status = self.model.add_phonetype(name)
            elif choice == 3:
                name = self.view.get_input("Phone name/label: ")
                pharmacy_id = self.view.get_int("PharmacyId: ")
                phonetype_id = self.view.get_int("PhoneTypeId: ")
                status = self.model.add_phone(name, pharmacy_id, phonetype_id)
            elif choice == 4:
                name = self.view.get_input("Manufacturer name: ")
                status = self.model.add_manufacturer(name)
            elif choice == 5:
                name = self.view.get_input("Drug name: ")
                manuf_id = self.view.get_int("ManufacturerId: ")
                price = self.view.get_float("Price: ")
                status = self.model.add_drug(name, manuf_id, price)
            elif choice == 6:
                pharmacy_id = self.view.get_int("PharmacyId: ")
                drug_id = self.view.get_int("DrugId: ")
                qty = self.view.get_int("Quantity: ")
                status = self.model.add_availability(pharmacy_id, drug_id, qty)
            elif choice == 7:
                break

            if status:
                if status == "OK":
                    self.view.show_message("Added successfully!")
                else:
                    self.view.show_error(status)

    # ---------------- update ----------------
    def update_menu(self):
        while True:
            self.view.show_message("\n-- UPDATE MENU --")
            self.view.show_message("1. Update Pharmacy")
            self.view.show_message("2. Update PhoneType")
            self.view.show_message("3. Update Phone")
            self.view.show_message("4. Update Manufacturer")
            self.view.show_message("5. Update Drug")
            self.view.show_message("6. Update Availability")
            self.view.show_message("7. Back")
            choice = self.view.get_int("Enter choice: ", 1, 7)
            if choice == 1:
                id_ = self.view.get_int("Pharmacy Id to update: ")
                name = self.view.get_input("New name: ")
                addr = self.view.get_input("New address: ")
                self.model.update_pharmacy(id_, name, addr)
            elif choice == 2:
                id_ = self.view.get_int("PhoneType Id to update: ")
                name = self.view.get_input("New name: ")
                self.model.update_phonetype(id_, name)
            elif choice == 3:
                id_ = self.view.get_int("Phone Id to update: ")
                name = self.view.get_input("New name: ")
                pharmacy_id = self.view.get_int("New PharmacyId: ")
                phonetype_id = self.view.get_int("New PhoneTypeId: ")
                self.model.update_phone(id_, name, pharmacy_id, phonetype_id)
            elif choice == 4:
                id_ = self.view.get_int("Manufacturer Id to update: ")
                name = self.view.get_input("New name: ")
                self.model.update_manufacturer(id_, name)
            elif choice == 5:
                id_ = self.view.get_int("Drug Id to update: ")
                name = self.view.get_input("New name: ")
                manuf_id = self.view.get_int("New ManufacturerId: ")
                price = self.view.get_float("New price: ")
                self.model.update_drug(id_, name, manuf_id, price)
            elif choice == 6:
                pharmacy_id = self.view.get_int("Availability: PharmacyId: ")
                drug_id = self.view.get_int("Availability: DrugId: ")
                qty = self.view.get_int("New quantity: ")
                self.model.update_availability(pharmacy_id, drug_id, qty)
            elif choice == 7:
                break

    # ---------------- delete ----------------
    def delete_menu(self):
        while True:
            self.view.show_message("\n-- DELETE MENU --")
            self.view.show_message("1. Delete Pharmacy (by Id)")
            self.view.show_message("2. Delete PhoneType (by Id)")
            self.view.show_message("3. Delete Phone (by Id)")
            self.view.show_message("4. Delete Manufacturer (by Id)")
            self.view.show_message("5. Delete Drug (by Id)")
            self.view.show_message("6. Delete Availability")
            self.view.show_message("7. Back")

            choice = self.view.get_int("Enter choice: ", 1, 7)
            table_map = {
                1: ("Pharmacies", "Id"),
                2: ("PhoneTypes", "Id"),
                3: ("Phones", "Id"),
                4: ("Manufacturers", "Id"),
                5: ("Drugs", "Id")
            }

            if choice in table_map:
                table, col = table_map[choice]
                id_ = self.view.get_int(f"{table} ID to delete: ")
                status = self.model.delete_by_id(table, col, id_)
                if status == "OK":
                    self.view.show_message("Deleted successfully.")
                else:
                    self.view.show_error(status)

            elif choice == 6:
                pharmacy_id = self.view.get_int("PharmacyId: ")
                drug_id = self.view.get_int("DrugId: ")
                self.model.delete_availability(pharmacy_id, drug_id)
                self.view.show_message("Deleted (if existed).")

            elif choice == 7:
                break

    # ---------------- generate ----------------
    def generate_menu(self):
        while True:
            self.view.show_message("\n-- GENERATE MENU --")
            self.view.show_message("1. Generate PhoneTypes (defaults)")
            self.view.show_message("2. Generate Pharmacies")
            self.view.show_message("3. Generate Manufacturers")
            self.view.show_message("4. Generate Drugs")
            self.view.show_message("5. Generate Phones")
            self.view.show_message("6. Generate Availabilities")
            self.view.show_message("7. Back")
            choice = self.view.get_int("Enter choice: ", 1, 7)
            if choice == 1:
                self.model.ensure_default_phonetypes()
            elif choice == 2:
                n = self.view.get_int("How many pharmacies to generate: ", 1, 10000)
                self.model.generate_pharmacies(n)
            elif choice == 3:
                n = self.view.get_int("How many manufacturers to generate: ", 1, 10000)
                self.model.generate_manufacturers(n)
            elif choice == 4:
                n = self.view.get_int("How many drugs to generate: ", 1, 10000)
                self.model.generate_drugs(n)
            elif choice == 5:
                n = self.view.get_int("How many phones to generate: ", 1, 10000)
                self.model.generate_phones(n)
            elif choice == 6:
                n = self.view.get_int("How many availability rows to generate: ", 1, 10000)
                self.model.generate_availabilities(n)
            elif choice == 7:
                break

    # ---------------- SEARCH ----------------
    def search_menu(self):
        while True:
            self.view.show_message("\n-- SEARCH & ANALYTICS --")
            self.view.show_message("1. Find Drugs (Price Range + Name)")
            self.view.show_message("2. Find Available Drugs in Pharmacies (Stock check)")
            self.view.show_message("3. Analyze Updates by Date Range")
            self.view.show_message("4. Back")

            choice = self.view.get_int("Enter choice: ", 1, 4)

            if choice == 1:
                min_p = self.view.get_float("Min Price: ")
                max_p = self.view.get_float("Max Price: ")
                name = self.view.get_input("Drug name part (or empty): ")
                rows = self.model.search_drug_stats(min_p, max_p, name)
                self.view.show_custom_results("Drug Search Results", ["Drug", "Manufacturer", "Price"], rows)

            elif choice == 2:
                name = self.view.get_input("Drug name part: ")
                min_q = self.view.get_int("Minimum quantity: ")
                rows = self.model.search_pharmacy_stock(name, min_q)
                self.view.show_custom_results("Stock Availability", ["Pharmacy", "Drug", "Quantity"], rows)

            elif choice == 3:
                d1 = self.view.get_date("Start Date")
                d2 = self.view.get_date("End Date")
                rows = self.model.search_updates_by_date(d1, d2)
                self.view.show_custom_results("Update Activity", ["Pharmacy", "Updates Count"], rows)

            elif choice == 4:
                break