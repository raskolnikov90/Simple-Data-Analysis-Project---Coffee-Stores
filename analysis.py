import csv
import sqlite3
import os
from reportlab.pdfgen import canvas
from reportlab.lib import colors


if os.path.exists("stores.db"):
    os.remove("stores.db")
if os.path.exists("report.pdf"):
    os.remove("report.pdf")

conn = sqlite3.connect("stores.db")

pdf = canvas.Canvas('report.pdf')
pdf.setTitle("Stores Report")

#Create report and initialize database
with open('Coffee Shop Sales data.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)  # Create DictReader
    store_repeat = []
    productlist = []
    productandstore = []
    storeandearnings = []
    c = conn.cursor()
    for row in csv_reader:
        store_repeat.append(row["store_location"])
        productlist.append(row["product_detail"])
        productandstore.append(row["store_location"]+" "+row["product_detail"])
        storeandearnings.append(row["store_location"]+"-"+row["unit_price"])
        
    cleaned_store = list(dict.fromkeys(store_repeat))
    cleaned_products = list(dict.fromkeys(productlist))
    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawCentredString(300, 770, "Store Sales Report")
    text = pdf.beginText(20, 700)
    for store in cleaned_store:
    	query = "CREATE TABLE \""+store.replace("'", "").replace(" ", "_")+"\"(transaction_id, transaction_date, transaction_time, unit_price, product_category, product_type, product_detail)"
    	c.execute(query)
    	text.setFont("Courier", 16)
    	text.textLine(store)
    	text.setFont("Courier", 14)
    	text.textLine("Number of transactions: "+ str(store_repeat.count(store)))
    	total = 0
    	for earnings in storeandearnings:
    		if store == earnings.split("-")[0]:
    			earning = earnings.split("-")
    			total = total + float(earning[1])
    	text.setFont("Courier", 14)
    	text.textLine("Total earnings: $"+ str(round(total,2)))
    	text.textLine("Popular Products: ")
    	for product in cleaned_products:
    	    	if productandstore.count(store+" "+product) > 1000:
    	    		text.setFont("Courier", 11)
    	    		text.textLine("-Sales of " + product + ": " + str(productandstore.count(store+" "+product)))
    	text.textLine("")
    	pdf.drawText(text)
pdf.save()

#Insert values into Sqlite Database			
with open('Coffee Shop Sales data.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    counter = 0
    for row in csv_reader:
    	counter = counter + 1
    	query = "INSERT INTO "+row["store_location"].replace("'", "").replace(" ", "_")+"(transaction_id, transaction_date, transaction_time, unit_price, product_category, product_type, product_detail) VALUES(?,?,?,?,?,?,?)"
    	c.execute(query, (row["\ufefftransaction_id"], row["transaction_date"], row["transaction_time"], row["unit_price"], row["product_category"], row["product_category"], row["product_detail"]))
    	conn.commit()
    	#the sqlite file would be too big so I limited the number
    	if counter == 100:
    	    	break
        
    	
