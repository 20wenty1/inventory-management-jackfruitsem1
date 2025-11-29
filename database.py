import sqlite3

con = sqlite3.connect("supermarket.db")
cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT ,
        price REAL  ,
        stock INTEGER ,
        category TEXT 
    )
""")

items = [
    ("Apple", 120, 50, "Fruit"),
    ("Banana", 40, 100, "Fruit"),
    ("Orange", 90, 60, "Fruit"),
    ("Grapes", 150, 40, "Fruit"),
    ("Pineapple", 75, 30, "Fruit"),
    ("Mango", 200, 25, "Fruit"),
    ("Papaya", 60, 35, "Fruit"),
    ("Pomegranate", 180, 20, "Fruit"),
    ("Guava", 50, 45, "Fruit"),
    ("Watermelon", 120, 15, "Fruit"),

    ("Potato", 30, 200, "Vegetable"),
    ("Onion", 55, 180, "Vegetable"),
    ("Tomato", 35, 150, "Vegetable"),
    ("Carrot", 45, 100, "Vegetable"),
    ("Cabbage", 40, 70, "Vegetable"),
    ("Cauliflower", 55, 65, "Vegetable"),
    ("Spinach", 25, 80, "Vegetable"),
    ("Beans", 60, 60, "Vegetable"),
    ("Peas", 70, 50, "Vegetable"),
    ("Capsicum", 80, 45, "Vegetable"),

    ("Turmeric Powder", 90, 60, "Spice"),
    ("Red Chilli Powder", 110, 50, "Spice"),
    ("Coriander Powder", 95, 55, "Spice"),
    ("Garam Masala", 140, 45, "Spice"),
    ("Black Pepper", 160, 35, "Spice"),
    ("Cumin Seeds", 120, 65, "Spice"),
    ("Mustard Seeds", 70, 75, "Spice"),
    ("Cardamom", 350, 30, "Spice"),
    ("Cloves", 360, 25, "Spice"),
    ("Fenugreek Seeds", 85, 50, "Spice"),

    ("Milk 1L", 60, 100, "Dairy"),
    ("Curd 1kg", 75, 60, "Dairy"),
    ("Paneer 500g", 190, 40, "Dairy"),
    ("Butter 500g", 250, 30, "Dairy"),
    ("Cheese Slices Pack", 280, 25, "Dairy"),

    ("Whole Wheat Bread", 45, 70, "Bakery"),
    ("Butter Cookies", 120, 60, "Bakery"),
    ("Muffins Pack", 150, 40, "Bakery"),
    ("Cream Roll", 25, 90, "Bakery"),
    ("Chocolate Cake", 300, 20, "Bakery"),

    ("Basmati Rice", 90, 120, "Grain"),
    ("Sona Masoori Rice", 75, 150, "Grain"),
    ("Brown Rice", 110, 100, "Grain"),
    ("Wheat Flour", 45, 200, "Grain"),
    ("Maida", 40, 160, "Grain"),
    ("Ragi Flour", 55, 90, "Grain"),
    ("Jowar Flour", 50, 80, "Grain"),
    ("Moong Dal", 85, 130, "Grain"),
    ("Toor Dal", 92, 110, "Grain"),
    ("Urad Dal", 88, 100, "Grain")
]

for item in items:
    try:
        cur.execute("INSERT INTO products (name, price, stock, category) VALUES (?, ?, ?, ?)", item)
    except sqlite3.IntegrityError:
        pass

con.commit()
con.close()
