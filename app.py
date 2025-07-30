from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# ✅ Database connection function
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "poultry_business"),
        user=os.getenv("DB_USER", "superset"),
        password=os.getenv("DB_PASS", "superset"),
        port=os.getenv("DB_PORT", "5432")
    )

# ================== HOME PAGE ==================
@app.route("/")
def home():
    return render_template("index.html")

# ================== SALES ENTRY ==================
@app.route("/sales", methods=["GET", "POST"])
def sales():
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        product_id = request.form["product_id"]
        customer_id = request.form["customer_id"]
        quantity = int(request.form["quantity"])
        sale_date = request.form["sale_date"]
        total_amount = float(request.form["total_amount"])

        cur.execute("""
            INSERT INTO sales (sale_date, product_id, customer_id, quantity, total_amount)
            VALUES (%s, %s, %s, %s, %s)
        """, (sale_date, product_id, customer_id, quantity, total_amount))

        conn.commit()
        cur.close()
        conn.close()
        return redirect("/sales")

    # Fetch dropdown data
    cur.execute("SELECT product_id, product_name FROM products ORDER BY product_name")
    products = cur.fetchall()

    cur.execute("SELECT customer_id, name FROM customers ORDER BY name")
    customers = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("sales.html", products=products, customers=customers)

# ================== PRODUCTION ENTRY ==================
@app.route("/production", methods=["GET", "POST"])
def production():
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        date = request.form["date"]
        product_id = request.form["product_id"]
        quantity_produced = request.form["quantity_produced"]

        cur.execute("""
            INSERT INTO production (date, product_id, quantity_produced)
            VALUES (%s, %s, %s)
        """, (date, product_id, quantity_produced))

        conn.commit()
        cur.close()
        conn.close()
        return redirect("/production")

    cur.execute("SELECT product_id, product_name FROM products ORDER BY product_name")
    products = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("production.html", products=products)

# ================== EXPENSES ENTRY ==================
@app.route("/expenses", methods=["GET", "POST"])
def expenses():
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        date = request.form["date"]
        expense_type = request.form["expense_type"]
        amount = request.form["amount"]
        notes = request.form["notes"]

        cur.execute("""
            INSERT INTO expenses (date, expense_type, amount, notes)
            VALUES (%s, %s, %s, %s)
        """, (date, expense_type, amount, notes))

        conn.commit()
        cur.close()
        conn.close()
        return redirect("/expenses")

    cur.close()
    conn.close()
    return render_template("expenses.html")

# ✅ Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

