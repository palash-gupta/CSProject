from flask import Flask, render_template, request, render_template_string, redirect
import mysql.connector as sql
from datetime import date
from random import randint

db = sql.connect(host = "localhost", user = "root", password = "", database = "Project")

cursor = db.cursor()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/order/")
def order():
    global cursor
    lst = []
    outOfStock = []

    cursor.execute("SELECT * FROM recipes;")
    out = cursor.fetchall()

    cursor.execute("SELECT ID, Stock FROM inventory;")
    currentInventory = cursor.fetchall();

    for i in out:
        if i[0] in outOfStock:
            continue
        elif currentInventory[i[1] - 1][1] < i[2]:
            outOfStock.append(i[0])
            if i[0] in lst:
                lst.remove(i[0])
            continue
        elif not i[0] in lst:
            lst.append(i[0])


    query = "SELECT * FROM sale_items WHERE ID = -1 OR "
    for i in lst:
        query += f"ID = {i} OR "
    query = query[:-4] + ";"

    cursor.execute(query)
    lst = cursor.fetchall()

    query = "SELECT * FROM sale_items WHERE ID = -1 OR "
    for i in outOfStock:
        query += f"ID = {i} OR "
    query = query[:-4] + ";"

    cursor.execute(query)
    outOfStock = cursor.fetchall()

    return render_template("order.html", availableItems=lst, outOfStock=outOfStock)

@app.route("/order/submit/", methods=["POST"])
def orderSubmit():
    global cursor
    
    requestForm = request.form.to_dict()
    cursor.execute("SELECT ID, Stock FROM inventory;")
    currentInventory = cursor.fetchall();

    reqdInventory = {}
    for i in list(requestForm.keys())[1:]:
        cursor.execute(f"SELECT Ingredient, Quantity FROM recipes WHERE ID = {i};")
        tmp = cursor.fetchall()
        for j in tmp:
            try:
                reqdInventory[j[0]] += j[1] * int(requestForm[i])
            except:
                reqdInventory[j[0]] = j[1] * int(requestForm[i])

    for i in currentInventory:
        if int(i[1]) < int(reqdInventory[i[0]]):
            return render_template_string("<script>alert('Items out of stock!'); window.history.back();</script>")
    
    id = randint(1000000, 10000000)
    currentDate = date.today().strftime("%Y-%m-%d")
    recpName = requestForm["recipientName"]

    for i in currentInventory:
        cursor.execute(f"UPDATE inventory SET Stock = {i[1] - reqdInventory[i[0]]} WHERE ID = {i[0]};")

    cursor.execute(f"INSERT INTO orders VALUES ({id}, '{recpName}', '{currentDate}')")
    for i in list(requestForm.keys())[1:]:
        if int(requestForm[i]) > 0:
            cursor.execute(f"INSERT INTO ordered_items VALUES ({id}, {i}, {requestForm[i]})")
    cursor.fetchall()
    db.commit()

    return redirect(f"/receipt/{id}/")


@app.route("/receipt/<id>/")
def receipt(id):
    global cursor

    cursor.execute(f"SELECT Recipient, TransactionDate FROM orders WHERE ID = {id};")
    recpName, currentDate = cursor.fetchall()[0]

    cursor.execute(f"SELECT SUM(sale_items.Price * Quantity) FROM ordered_items, sale_items  WHERE sale_items.ID = ordered_items.Item AND ordered_items.ID = {id};")
    price = cursor.fetchall()[0][0]

    cursor.execute(f"SELECT ItemName, Quantity, Quantity * Price FROM sale_items, ordered_items WHERE ordered_items.Item = sale_items.ID and ordered_items.ID = {id};")
    items = cursor.fetchall()

    return render_template("receipt.html", id=id, currentDate=str(currentDate), recpName=recpName, price=price, items=items)


@app.route("/recipes/")
def recipes():
    global cursor
    cursor.execute("SELECT ID, ItemName FROM sale_items;")
    lst = []
    for i in cursor.fetchall():
        cursor.execute(f"SELECT inventory.ItemName, recipes.Quantity FROM recipes, inventory WHERE recipes.Ingredient = inventory.ID AND recipes.ID = {i[0]};")
        lst.append([i[1], cursor.fetchall()])

    print(lst)

    return render_template("recipes.html", lst=lst)

@app.route("/stock/")
def stock():
    global cursor
    cursor.execute("SELECT ItemName, Stock, LastRenewed FROM inventory;")
    return render_template("stock.html", lst=cursor.fetchall())

@app.route("/menu/")
def menu():
    global cursor
    cursor.execute("SELECT ItemName, Price FROM sale_items;")
    return render_template("menu.html", lst=cursor.fetchall())

@app.route("/orders/")
def orders():
    global cursor
    cursor.execute("SELECT ID, Recipient, TransactionDate FROM orders;")
    lst = []
    for i in cursor.fetchall():
        cursor.execute(f"SELECT ItemName FROM ordered_items, sale_items WHERE sale_items.ID = ordered_items.Item AND ordered_items.ID = {i[0]};")
        lst.append([i[0], i[1], i[2], cursor.fetchall()])

    print(lst)

    return render_template("orders.html", lst=lst)

if __name__ == "__main__":
    app.run(debug=True)
    db.close()