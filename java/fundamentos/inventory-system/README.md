# ☕ Product Inventory

> Java Fundamentals • Oracle Learning Project

A simple Java console application created while following the **Oracle Java Fundamentals** learning path.

The purpose of this project is to practice the core concepts of **Object-Oriented Programming (OOP)** by modeling products using classes, constructors, encapsulation, and object methods.

---

# 📚 Learning Objectives

This project was developed to reinforce:

- Classes and Objects
- Constructors
- Encapsulation
- Getters and Setters
- Method Overriding
- Object Instantiation
- Console Output
- Java Syntax

---

# 📂 Project Structure

```text
product-inventory/
│
├── src/
│   ├── Product.java
│   └── ProductTester.java
│
├── README.md
└── .gitignore
```

---

# 🚀 Features

- Create products using the default constructor.
- Create products using parameterized constructors.
- Store information such as:
  - Product ID
  - Product name
  - Stock quantity
  - Unit price
- Display product information using the overridden `toString()` method.

---

# 🧱 Class Design

## Product

Represents a product stored in the inventory.

### Attributes

- ID
- Name
- Units in stock
- Unit Price

### Methods

- Default constructor
- Parameterized constructor
- Getters
- Setters
- `toString()`

---

## ProductTester

Creates multiple `Product` objects and prints their information to the console.

This class demonstrates how constructors and object methods work in Java.

---

# ▶️ Example Output

```text
=== Product 1 ===

Item Number : 42312
Name : Phone Screen
Quantity in stock : 15
Price : 20000
```

---

# 🧠 Concepts Practiced

- Object-Oriented Programming (OOP)
- Constructors
- Encapsulation
- Access Modifiers
- Instance Fields
- Object Creation
- Method Overriding
- Java Classes

---

# 📈 Future Improvements

- [ ] Add product search by ID
- [ ] Update product stock
- [ ] Delete products
- [ ] Store products in an ArrayList
- [ ] Read and save inventory from files
- [ ] Interactive console menu

---

# 🎓 Credits

This project was developed as part of the **Oracle Java Fundamentals** learning path and adapted as a personal practice project.

---

# 📄 License

Part of **Cyber-Dev-Lab**.