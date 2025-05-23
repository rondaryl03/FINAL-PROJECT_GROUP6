import requests

API_URL = "http://localhost:5000/api/plants"

def list_plants():
    response = requests.get(API_URL)
    if response.status_code == 200:
        plants = response.json()
        if not plants:
            print("No plants found.")
        for plant in plants:
            print(f"{plant['id']}: {plant['name']} ({plant['species']})")
    else:
        print("Failed to fetch plants.")

def view_plant():
    plant_id = input("Enter Plant ID to view: ")
    response = requests.get(f"{API_URL}/{plant_id}")
    if response.status_code == 200:
        plant = response.json()
        for key, value in plant.items():
            print(f"{key.capitalize()}: {value}")
    else:
        print("Plant not found.")

def add_plant():
    name = input("Name: ")
    species = input("Species: ")
    water_frequency = input("Water Frequency (days): ")
    last_watered = input("Last Watered Date (YYYY-MM-DD) [optional]: ")
    sunlight = input("Sunlight Requirements [optional]: ")
    photo_url = input("Photo URL [optional]: ")

    data = {
        "name": name,
        "species": species,
        "water_frequency": int(water_frequency),
        "last_watered": last_watered or None,
        "sunlight_requirements": sunlight,
        "photo_url": photo_url
    }

    response = requests.post(API_URL, json=data)
    if response.status_code == 201:
        print("Plant added successfully.")
    else:
        print("Error adding plant:", response.json().get('error', 'Unknown error'))

def update_plant():
    plant_id = input("Enter Plant ID to update: ")
    print("Leave fields empty to skip updating them.")
    name = input("New Name: ")
    species = input("New Species: ")
    water_frequency = input("New Water Frequency (days): ")
    last_watered = input("New Last Watered Date (YYYY-MM-DD): ")
    sunlight = input("New Sunlight Requirements: ")
    photo_url = input("New Photo URL: ")

    data = {}
    if name: data["name"] = name
    if species: data["species"] = species
    if water_frequency: data["water_frequency"] = int(water_frequency)
    if last_watered: data["last_watered"] = last_watered
    if sunlight: data["sunlight_requirements"] = sunlight
    if photo_url: data["photo_url"] = photo_url

    response = requests.put(f"{API_URL}/{plant_id}", json=data)
    if response.status_code == 200:
        print("Plant updated successfully.")
    else:
        print("Error updating plant:", response.json().get('error', 'Unknown error'))

def delete_plant():
    plant_id = input("Enter Plant ID to delete: ")
    response = requests.delete(f"{API_URL}/{plant_id}")
    if response.status_code == 200:
        print("Plant deleted.")
    else:
        print("Error deleting plant:", response.json().get('error', 'Unknown error'))

def menu():
    while True:
        print("\n--- Plant Care Tracker ---")
        print("1. List Plants")
        print("2. View Plant Details")
        print("3. Add New Plant")
        print("4. Update Plant")
        print("5. Delete Plant")
        print("0. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            list_plants()
        elif choice == '2':
            view_plant()
        elif choice == '3':
            add_plant()
        elif choice == '4':
            update_plant()
        elif choice == '5':
            delete_plant()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    menu()