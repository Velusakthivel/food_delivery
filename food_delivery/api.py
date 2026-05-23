import frappe
from math import radians, cos, sin, asin, sqrt


def calculate_distance(lat1, lon1, lat2, lon2):

    lon1, lat1, lon2, lat2 = map(
        radians,
        [lon1, lat1, lon2, lat2]
    )

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * asin(sqrt(a))

    r = 6371

    return c * r


@frappe.whitelist(allow_guest=True)
def get_nearby_restaurants(latitude, longitude):

    latitude = float(latitude)
    longitude = float(longitude)

    restaurants = frappe.get_all(
        "Restaurant",
        filters={
            "status": "Active"
        },
        fields=[
            "name",
            "restaurant_name",
            "latitude",
            "longitude",
            "delivery_radius_km"
        ]
    )

    nearby_restaurants = []

    for restaurant in restaurants:

        distance = calculate_distance(
            latitude,
            longitude,
            restaurant.latitude,
            restaurant.longitude
        )

        if distance <= restaurant.delivery_radius_km:

            nearby_restaurants.append({
                "restaurant": restaurant.restaurant_name,
                "distance_km": round(distance, 2)
            })

    return nearby_restaurants


def calculate_delivery_fee(distance):

    base_fee = 20
    per_km_charge = 8

    return base_fee + (distance * per_km_charge)


def assign_delivery_agent(customer_lat, customer_lon):

    agents = frappe.get_all(
        "Delivery Agent",
        filters={
            "availability": "Available"
        },
        fields=[
            "name",
            "agent_name",
            "latitude",
            "longitude"
        ]
    )

    nearest_agent = None
    minimum_distance = 999999

    for agent in agents:

        distance = calculate_distance(
            customer_lat,
            customer_lon,
            agent.latitude,
            agent.longitude
        )

        if distance < minimum_distance:

            minimum_distance = distance
            nearest_agent = agent

    return nearest_agent


@frappe.whitelist(allow_guest=True)
def place_order(
    customer,
    restaurant,
    delivery_address,
    delivery_latitude,
    delivery_longitude,
    payment_mode,
    items
):

    import json

    items = json.loads(items)

    total_amount = 0

    for item in items:

        amount = item["quantity"] * item["price"]

        total_amount += amount

    restaurant_doc = frappe.get_doc(
        "Restaurant",
        restaurant
    )

    distance = calculate_distance(
        float(delivery_latitude),
        float(delivery_longitude),
        restaurant_doc.latitude,
        restaurant_doc.longitude
    )

    delivery_fee = calculate_delivery_fee(distance)

    grand_total = total_amount + delivery_fee

    assigned_agent = assign_delivery_agent(
        float(delivery_latitude),
        float(delivery_longitude)
    )

    order = frappe.get_doc({
        "doctype": "Food Order",
        "customer": customer,
        "restaurant": restaurant,
        "delivery_address": delivery_address,
        "delivery_latitude": delivery_latitude,
        "delivery_longitude": delivery_longitude,
        "payment_mode": payment_mode,
        "delivery_fee": delivery_fee,
        "total_amount": total_amount,
        "grand_total": grand_total,
        "delivery_agent": assigned_agent.name if assigned_agent else None,
        "order_status": "Placed"
    })

    for item in items:

        order.append("order_items", {
            "menu_item": item["menu_item"],
            "quantity": item["quantity"],
            "price": item["price"],
            "amount": item["quantity"] * item["price"]
        })

    order.insert(ignore_permissions=True)

    if assigned_agent:

        frappe.db.set_value(
            "Delivery Agent",
            assigned_agent.name,
            "availability",
            "Busy"
        )

    return {
        "status": "success",
        "order_id": order.name,
        "delivery_fee": delivery_fee,
        "grand_total": grand_total,
        "delivery_agent": assigned_agent.agent_name if assigned_agent else None
    }


@frappe.whitelist(allow_guest=True)
def update_order_status(order_id, status):

    frappe.db.set_value(
        "Food Order",
        order_id,
        "order_status",
        status
    )

    if status == "Delivered":

        order = frappe.get_doc(
            "Food Order",
            order_id
        )

        if order.delivery_agent:

            frappe.db.set_value(
                "Delivery Agent",
                order.delivery_agent,
                "availability",
                "Available"
            )

    return {
        "status": "success",
        "message": f"Order updated to {status}"
    }


@frappe.whitelist(allow_guest=True)
def track_order(order_id):

    order = frappe.get_doc(
        "Food Order",
        order_id
    )

    return {
        "order_id": order.name,
        "customer": order.customer,
        "restaurant": order.restaurant,
        "status": order.order_status,
        "delivery_agent": order.delivery_agent,
        "grand_total": order.grand_total
    }
@frappe.whitelist(allow_guest=True)
def get_restaurant_menu(restaurant):

    menu_items = frappe.get_all(
        "Menu Item",
        filters={
            "restaurant": restaurant,
            "is_available": 1
        },
        fields=[
            "name",
            "item_name",
            "category",
            "price"
        ]
    )

    return menu_items
@frappe.whitelist(allow_guest=True)
def get_customer_orders(customer):

    orders = frappe.get_all(
        "Food Order",
        filters={
            "customer": customer
        },
        fields=[
            "name",
            "restaurant",
            "grand_total",
            "order_status",
            "creation"
        ],
        order_by="creation desc"
    )

    return orders
@frappe.whitelist(allow_guest=True)
def accept_delivery(order_id):

    frappe.db.set_value(
        "Food Order",
        order_id,
        "order_status",
        "Picked Up"
    )

    return {
        "status": "success",
        "message": "Delivery accepted"
    }
