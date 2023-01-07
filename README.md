Run these Queries in a new MySQL database

```sql
CREATE TABLE inventory (ID Int Primary Key, ItemName varchar(20), Stock Int, LastRenewed Date);
CREATE TABLE sale_items (ID Int Primary Key, ItemName varchar(20), Price Int);
CREATE TABLE recipes (ID Int, Ingredient Int, Quantity Int);
CREATE TABLE orders (ID Int Primary Key, Recipient varchar (20), TransactionDate Date);
CREATE TABLE ordered_items (ID Int, Item Int, Quantity Int);

INSERT INTO sale_items VALUES (1, "Caramel Macchiato", 300), (2, "Espresso Martini", 350), (3, "Classic Cappuccino", 250), (4, "Caffe Mocha", 300), (5, "Caffe Americano", 250), (6, "Cinnamon Coffee Cake", 300), (7, "Chocolate Chip Cookies", 150), (8, "Iced Coffee Lemonade", 200), (9, "Caffe Latte", 200), (10, "Iced Mocha", 300);

INSERT INTO inventory VALUES (1, "Brown Sugar", 500, "1970/01/01"), (2, "Butter", 300, "1970/01/01"), (3, "Salt", 500, "1970/01/01"), (4, "Roast Espresso", 60, "1970/01/01"), (5, "Milk", 10, "1970/01/01"), (6, "Vodka", 200, "1970/01/01"), (7, "Coffee Liqueur", 200, "1970/01/01"), (8, "Mocha Sauce", 500, "1970/01/01"), (9, "Whipped Cream", 100, "1970/01/01"), (10, "Flour", 50, "1970/01/01"), (11, "Eggs", 30, "1970/01/01"), (12, "Ground Cinnamon", 30, "1970/01/01"), (13, "Chocolate Chips", 50, "1970/01/01"), (14, "Lemons", 30, "1970/01/01");

INSERT INTO recipes VALUES (1, 1, 1),(1, 2, 4),(1, 3, 1),(1, 4, 2),(1, 5, 1),(2, 4, 2),(2, 6, 4),(2, 7, 2),(3, 4, 2),(3, 5, 4),(4, 4, 1),(4, 5, 4),(4, 8, 1),(4, 9, 2),(5, 4, 2),(6, 2, 12),(6, 1, 3),(6, 11, 3),(6, 10, 3),(6, 3, 4),(6, 12, 3),(7, 2, 3),(7, 11, 3),(7, 1, 2),(7, 3, 2),(7, 13, 3),(8, 1, 2),(8, 14, 2),(8, 4, 1),(9, 4, 1),(9, 5, 4),(10, 4, 2),(10, 5, 4),(10, 9, 3);
```