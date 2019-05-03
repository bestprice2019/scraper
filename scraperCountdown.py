from urllib.request import urlopen as uReq
import time
from bs4 import BeautifulSoup as soup

#getting list of categories
my_url = 'https://shop.countdown.co.nz/'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")


#the directories under the browse drop down
categories = page_soup.findAll("li",{"class":"toolbar-slidebox-item"})

category_list = []
for category in categories:
	if '/browse' in category.find('a')['href']:
		category_list.append(category.find('a')['href'])

print("All category URLS: ")
print(category_list)

filename = "productsCountdown.csv"
f = open(filename,"w")

headers = "store, title, price\n"
f.write(headers)


for url in category_list:


	#grabbing page list after going into category
	my_url = 'https://shop.countdown.co.nz'+url
	#my_url = 'https://shop.countdown.co.nz/shop/browse/christmas'
	current_url = my_url
	
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")


	total_pages = page_soup.findAll("li",{"class":"page-number"})
	if total_pages:
		#total_pages index -1 is the last one of the list, so the final page
		total_pages = total_pages[-1].text.strip()
		total_pages = int(total_pages)
	else:
		#if there is 1 page theres no page menu, so list should? be empty
		total_pages = 1	

	
	print('Category: ' +url)
	print('Total number of pages in this category: '+str(total_pages))




	count=1

	while count < total_pages+1:
		time.sleep(5)
		page = "?page="+str(count)
		print('Page '+str(count)+' of '+str(total_pages))
		count += 1
		
		#grabbing products from category
		#my_url = 'https://shop.countdown.co.nz/shop/browse/bakery'
		my_url = current_url
		my_url = my_url+page
		print(my_url)

		#opening up connection, grabbing the page
		uClient = uReq(my_url)
		page_html = uClient.read()
		uClient.close()

		#html parsing
		page_soup = soup(page_html, "html.parser")

		#grabs each product from page and adds them to array 'products'
		products = page_soup.findAll("div",{"class":"gridProductStamp gridStamp"})



		#loops through all products and pulls title, price
		for product in products:
			#grabs the header3 which contains title,  strip() removes the formatting \r\n etc
			title = product.div.div.a.h3.text.strip()
			price = None

			#grabs the price
			price = product.findAll("div",{"class":"gridProductStamp-price din-medium"})
			#if is on special, it's contained with in a span instead of div for some reason, 'if not' is checking if price was created (above returned nothing must be special)
			if not price:
				price = product.findAll("span",{"class":"gridProductStamp-price savings-text din-medium"})
			if not price:
				price = product.findAll("span",{"class":"gridProductStamp-price club-text-colour din-medium"})
			
				

			#strip() removes the formatting. .replace() is replacing \xa0 which is a nbps with a standard space
			price = price[0].text.strip().replace(u'\xa0', u' ')

			print("title: "+ title.replace(',','|'))
			print("price: "+price)

			#f.write(title +"," +price +"\n")
			f.write("CD" +"," +title.replace(',','|') +"," +price.replace('$','').replace(' ea','') +"\n")

f.close()


