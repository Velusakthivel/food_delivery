# Food Delivery Backend System 🍔🚚

A backend Food Delivery Management System developed using the Frappe Framework.

This project supports:
- Restaurant Management
- Menu Management
- Food Ordering
- Delivery Tracking
- Delivery Agent Assignment
- Customer Order History
- Restaurant Order Confirmation

---

# 🚀 Features

- Nearby Restaurant API
- Restaurant Menu API
- Food Ordering API
- Delivery Fee Calculation
- Auto Delivery Agent Assignment
- Order Tracking Lifecycle
- Delivery Status Updates
- Customer Order History

---

# 🛠️ Tech Stack

- Frappe Framework
- Python
- MariaDB
- Bench
- Ubuntu

---

# 📂 Implemented DocTypes

| DocType | Type |
|---|---|
| Restaurant | Normal DocType |
| Customer | Normal DocType |
| Menu Item | Normal DocType |
| Delivery Agent | Normal DocType |
| Food Order | Normal DocType |
| Order Item | Child Table |

---

# 🔗 API Endpoints

## Get Nearby Restaurants

```python
food_delivery.api.get_nearby_restaurants
```

## Get Restaurant Menu

```python
food_delivery.api.get_restaurant_menu
```

## Place Food Order

```python
food_delivery.api.place_order
```

## Track Order

```python
food_delivery.api.track_order
```

## Confirm Order

```python
food_delivery.api.confirm_order
```

## Reject Order

```python
food_delivery.api.reject_order
```

## Accept Delivery

```python
food_delivery.api.accept_delivery
```

## Update Delivery Status

```python
food_delivery.api.update_delivery_status
```

## Customer Order History

```python
food_delivery.api.get_customer_orders
```

---

# 🔄 Workflow

1. Customer searches nearby restaurants
2. Customer views menu items
3. Customer places order
4. System calculates delivery fee
5. System assigns nearest delivery agent
6. Restaurant confirms/rejects order
7. Delivery agent accepts delivery
8. Delivery status updated
9. Order delivered successfully

---

# 📸 Screenshots

## Restaurant DocType

![Restaurant](screenshots/restaurant.png)

---

## Customer DocType

![Customer](screenshots/customer.png)

---

## Food Order DocType

![Food Order](screenshots/food_order.png)

---

## Delivery Agent DocType

![Delivery Agent](screenshots/delivery_agent.png)

---

# ▶️ Run Project

```bash
bench start
```

---

# 📦 GitHub Repository

https://github.com/Velusakthivel/food_delivery

---

# 👨‍💻 Developer

Velumani S
