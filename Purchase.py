#!/usr/bin/python
import cgi
import csv

#--------------------------------------------------------------------------
#We will need to first open member files and compare with user to see if they can continue
form = cgi.FieldStorage()
username = form.getvalue('username') 

f = open('LoggedIn.csv', 'rt')
reader = csv.reader(f)
members = []

for row in reader:
	members.append(row[0])

f.close()
x = 'false'

for member in members:
	if username == member:
		x = 'true'
		break
#If x = false then we print the error page
if x == 'false':
	err = open('NotLoggedIn.html', 'rt')
	lines = err.readlines()
	print "Content-type:text/html\r\n\r\n"
	for line in lines:
		print line
else:

#--------------------------------------------------------------------------
#Will create our lists from csv file here
	f = open("Inventory.csv", "rt")
	reader = csv.reader(f)
	file_prices = []
	file_quantity = []
	file_names = []

	for row in reader:
		file_prices.append(row[2])

	f.seek(0,0)
	for row in reader:
		file_quantity.append(row[1])
	file_quantity = map(int, file_quantity)

	f.seek(0,0)
	for row in reader:
		file_names.append(row[0])
	f.close()
#--------------------------------------------------------------------------
#Now we will get our values from our form

	quantity1 = int(form.getvalue('Quantity1'))
	quantity2 = int(form.getvalue('Quantity2'))
	quantity3 = int(form.getvalue('Quantity3'))
	quantity4 = int(form.getvalue('Quantity4'))


	purchase1 = form.getvalue('purchase1')
	purchase2 = form.getvalue('purchase2')
	purchase3 = form.getvalue('purchase3')
	purchase4 = form.getvalue('purchase4')

	if (quantity1 > file_quantity[0]) or (quantity2 > file_quantity[1]) or (quantity3 > file_quantity[2]) or (quantity4 > file_quantity[3]):
		err2 = open('TooManyItems.html', 'rt')
		lines = err2.readlines()
		print "Content-type:text/html\r\n\r\n"
		for line in lines:
			print line
	else: 		
#--------------------------------------------------------------------------
		string_total = "|"

		if quantity1 > 0 and purchase1 == "on" : 
			#calculate total
			total_p1 = 3.99*quantity1
			#construct string for bill viewing
			string_total += (" Apple Cider Fritters: $" + str(total_p1) + '|')
			#subtract quantity purchased from inventory
			file_quantity[0] = file_quantity[0] - quantity1
		else: 
			#if nothing purchased we leave it alone
			total_p1 = 0
	
		if quantity2 > 0 and purchase2 == "on" :
			total_p2 = 2.99*quantity2
			string_total += (" Red Velvet: $" + str(total_p2) + '|')
			file_quantity[1] = file_quantity[1] - quantity2
		else:
			total_p2 = 0
	
		if quantity3 > 0 and purchase3 == "on" :
			total_p3 = 3.49*quantity3
			string_total += (" Banana Caramel Pecan: $" + str(total_p3) + '|')
			file_quantity[2] = file_quantity[2] - quantity3
		else:
			total_p3 = 0
	
		if quantity4 > 0 and purchase4 == "on" :
			total_p4 = 19.99*quantity4
			string_total += (" Maple Bacon: $" + str(total_p4) + '|')
			file_quantity[3] = file_quantity[3] - quantity4
		else:
			total_p4 = 0

		overall_total = total_p1 + total_p2 + total_p3 + total_p4
	
#--------------------------------------------------------------------------
#Now we have new values for file_quantities which we want to replace our original file values with
		f = open('Inventory.csv', 'wt')
		writer = csv.writer(f)

		file_quantity = map(str, file_quantity)
		line1 = [file_names[0], file_quantity[0], file_prices[0]]
		line2 = [file_names[1], file_quantity[1], file_prices[1]]
		line3 = [file_names[2], file_quantity[2], file_prices[2]]
		line4 = [file_names[3], file_quantity[3], file_prices[3]]

		writer.writerow(line1)
		writer.writerow(line2)
		writer.writerow(line3)
		writer.writerow(line4)

		f.close()
#--------------------------------------------------------------------------
#Our html page

		print "Content-type:text/html\r\n\r\n"
		print "<html>"

#CSS styles --------
		print "<style>"
		print "p {font-family: helvetica;}"

		print "#totals {color: grey;}"

		print "body {background-color: Khaki;}"

		print "h1 {font-family:helvetica;}"

		print "a {font-family:helvetica;"
		print "text-decoration:none;"
		print "background-color: GoldenRod;"
		print "width: 80px;"
		print "color:white;"
		print "padding: 0.2em 0.6em;}"

		print "a:hover {background-color: Gold;}"

		print "</style>"
#-------------------

		print "<head>"
		print "<title> Thank You! </title>"
		print "</head>"
		print "<center><h1> Order Confirmation </h1><br><br>"
		print "<body>"
		print "<p id=totals> %s </p>" %string_total
		print "<p> ------------------------------------</p>"
		print "<p><b> Total = $%.2f </b></p>" %overall_total
		print "<p> ------------------------------------</p>"
		print "<img src=http://3.bp.blogspot.com/-ZVGjMlaHu0A/TVWIl3pwYWI/AAAAAAAAFkQ/Khtw_rTbsz4/s400/homer.bmp style=width:500px;height:500px alt='Homer bein sad with a donut'>"
		print "<br><br><br>"
		print "<p> Thank you very much for your order, click the link to confirm and go back to the home page! </p>"
		print "<br><br><a href='index.html' > Home </a>"
		print "<br><br><a href='catalogue.html' > Catalogue </a>"
		print "</center>"
		print "</body>"
		print "</html>"

#-------------------

