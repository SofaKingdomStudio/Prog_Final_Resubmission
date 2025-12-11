import os

# ==========================================
# CLASS 1: LibraryItem
# [cite: 1-8]
# ==========================================
class LibraryItem:
    def __init__(self, item_id, title, item_type, late_fee):
        self.id = item_id
        self.title = title
        self.item_type = item_type
        self.daily_late_fee = float(late_fee)

    def __str__(self):
        # Returns a string representation of the object 
        return f"[ID: {self.id}] {self.title} ({self.item_type}) - Late Fee: ${self.daily_late_fee:.2f}"

# ==========================================
# CLASS 2: CheckoutItem
# [cite: 9-13]
# ==========================================
class CheckoutItem:
    def __init__(self, library_item, days_borrowed=7):
        self.library_item = library_item # This is the object from the class above
        self.days_borrowed = int(days_borrowed)

    def calculate_fee(self, days_late):
        # Math logic for the fee
        if days_late <= 0:
            return 0.0
        return days_late * self.library_item.daily_late_fee

    def get_receipt_line(self, days_late):
        fee = self.calculate_fee(days_late)
        return f"{self.library_item.title} | Late: {days_late} days | Fee: ${fee:.2f}"

# ==========================================
# GLOBAL LISTS [cite: 14- 16]
# ==========================================
library_catalog = [] # Holds LibraryItems
my_cart = []         # Holds CheckoutItems

# ==========================================
# FILE I/O FUNCTIONS
# [cite: 17-22]]
# ==========================================
def load_catalog():
    # Reads the catalog.txt file
    if not os.path.exists("catalog.txt"):
        print("catalog.txt is missing. We have nothing, you nihilist.")
        return

    with open("catalog.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            # Create object and add to list
            new_item = LibraryItem(parts[0], parts[1], parts[2], parts[3])
            library_catalog.append(new_item)
    print("Catalog loaded. Prepare to be educated, pleb.")

def save_checkout_list():
    # Writes cart to my_checkouts.txt
    with open("my_checkouts.txt", "w") as file:
        for item in my_cart:
            # Save the ID and the days borrowed
            file.write(f"{item.library_item.id},{item.days_borrowed}\n")
    print("Checkout list saved. Don't lose it, or I'll fine you.")

def load_checkout_list():
    # Reads my_checkouts.txt and rebuilds the objects
    if not os.path.exists("my_checkouts.txt"):
        print("No save file found. Start fresh, lazybones.")
        return

    my_cart.clear() # Wipe current cart
    with open("my_checkouts.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            saved_id = parts[0]
            saved_days = parts[1]
            
            # We have the ID, but we need the full Object from the catalog
            found = False
            for catalog_item in library_catalog:
                if catalog_item.id == saved_id:
                    # Reconstruct the CheckoutItem
                    reloaded_item = CheckoutItem(catalog_item, saved_days)
                    my_cart.append(reloaded_item)
                    found = True
                    break
            if not found:
                print(f"Item ID {saved_id} no longer exists. The system purged it.")
    print("Checkout list loaded. Welcome back to your debt.")

# ==========================================
# MAIN PROGRAM LOGIC
# [cite: 23-38]
# ==========================================
def main():
    load_catalog()
    
    while True: # Infinite Loop 
        print("\n--- THE ANARCHIST LIBRARY ---")
        print("1. Donate (Add) an Item to the Catalog")
        print("2. Gaze upon the Forbidden Texts (View Catalog)")
        print("3. Steal... I mean, Checkout an Item")
        print("4. Return an Item (Submit to Authority)")
        print("5. View Receipt of Doom")
        print("6. Save my stash")
        print("7. Load my stash")
        print("8. Run Away (Exit)")
        
        choice = input("\nChoose your fate, maggot: ")

        # 1. Add Item (File I/O + Lists)
        if choice == "1":
            i_id = input("ID: ")
            i_title = input("Title: ")
            i_type = input("Type (Book/DVD): ")
            i_fee = input("Daily Late Fee: ")
            
            # Create and Add to memory
            new_item = LibraryItem(i_id, i_title, i_type, i_fee)
            library_catalog.append(new_item)
            
            # Append to file immediately
            with open("catalog.txt", "a") as file:
                file.write(f"\n{i_id},{i_title},{i_type},{i_fee}")
            print(f"'{i_title}' added. The revolution grows.")

        # 2. View Catalog (Looping through list)
        elif choice == "2":
            print("\n--- CATALOG ---")
            for item in library_catalog: # For Loop 
                print(item)

        # 3. Checkout (Searching logic)
        elif choice == "3":
            search_id = input("Enter the ID of the item you want: ")
            found_item = None
            
            # Find the item in the catalog
            for item in library_catalog:
                if item.id == search_id:
                    found_item = item
                    break
            
            if found_item:
                # Add to cart
                new_checkout = CheckoutItem(found_item)
                my_cart.append(new_checkout)
                print(f"You checked out '{found_item.title}'. Don't ruin the spine.")
            else:
                print("That ID doesn't exist. Learn to read.")

        # 4. Return Item (List Removal)
        elif choice == "4":
            remove_id = input("Enter ID to return: ")
            found = False
            for checkout in my_cart:
                if checkout.library_item.id == remove_id:
                    my_cart.remove(checkout) # List method 
                    print("Item returned. You are a compliant citizen.")
                    found = True
                    break
            if not found:
                print("You don't have that item. Are you hallucinating?")

        # 5. Receipt (Calculations + Loop)
        elif choice == "5":
            print("\n--- RECEIPT OF SHAME ---")
            total_fee = 0.0
            
            if not my_cart:
                print("You have nothing. Good day.")
            else:
                days_late_input = input("Be honest, how many days late is your stuff? (Enter number): ")
                try:
                    days_late = int(days_late_input)
                except:
                    days_late = 0 # Default if they type garbage
                
                # Apply Student Discount logic (Decision)
                is_student = input("Are you a broke student? (y/n): ")
                
                print("-" * 30)
                for checkout in my_cart:
                    # Calculate fee
                    fee = checkout.calculate_fee(days_late)
                    
                    # Logic: Apply discount if student
                    if is_student.lower() == 'y':
                        fee = fee * 0.80 # 20% off
                        
                    total_fee += fee
                    print(f"{checkout.library_item.title} | Fee: ${fee:.2f}")
                
                print("-" * 30)
                print(f"TOTAL OWED: ${total_fee:.2f}")
                if total_fee > 0:
                    print("Pay up or we take your kneecaps.")

        # 6. Save
        elif choice == "6":
            save_checkout_list()

        # 7. Load
        elif choice == "7":
            load_checkout_list()

        # 8. Exit
        elif choice == "8":
            print("Finally. Leave.")
            break # Break keyword 

        else:
            print("Invalid choice. Try harder.")
            #[cite: 38]

if __name__ == "__main__":
    main()
    #[cite: 39-41]]


