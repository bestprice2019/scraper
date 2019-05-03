from urllib.request import urlopen as uReq
import urllib.request
import time
import re
import json
from bs4 import BeautifulSoup as soup

#getting list of categories
my_url = 'https://www.ishopnewworld.co.nz/'
hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
req = urllib.request.Request(my_url, headers=hdr)
uClient = urllib.request.urlopen(req)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")


#the directories under the browse drop down
#categories = page_soup.findAll("a",{"class":"fs-mega-menu__link fs-mega-menu__link--all"})

#category_list = []
#for category in categories:
#	if '/category' in category.find('a')['href']:
#		category_list.append(category.find('a')['href'])
category_list=[]
category_list.append('fresh-foods-and-bakery')
category_list.append('chilled-frozen-and-desserts')
category_list.append('pantry')
category_list.append('drinks')
category_list.append('beer-cider-and-wine')
category_list.append('personal-care')
category_list.append('baby-toddler-and-kids')
category_list.append('pets')
category_list.append('kitchen-dining-and-household')

print("All category URLS: ")
print(category_list)

filename = "productsNewWorld.csv"
f = open(filename,"w")

headers = "store, title, price\n"
f.write(headers)


for url in category_list:


	#grabbing page list after going into category
	my_url = 'https://www.ishopnewworld.co.nz/category/'+url
	#my_url = 'https://www.ishopnewworld.co.nz/category/fresh-foods-and-bakery'
	current_url = my_url
	
	hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
	req = urllib.request.Request(my_url, headers=hdr)
	uClient = urllib.request.urlopen(req)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")


	total_pages = page_soup.findAll("li",{"class":"fs-pagination__item"})
	if total_pages:
		#total_pages index -1 is the last one of the list, so the final page
		total_pages = total_pages[-2].text.strip()
		total_pages = int(total_pages)
	else:
		#if there is 1 page theres no page menu, so list should? be empty
		total_pages = 1	

	
	print('Category: ' +url)
	print('Total number of pages in this category: '+str(total_pages))




	count=1

	while count < total_pages+1:
		time.sleep(5)
		page = "?pg="+str(count)
		print('Page '+str(count)+' of '+str(total_pages))
		count += 1

		my_url = current_url
		my_url = my_url+page
		print(my_url)
		
		hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
		req = urllib.request.Request(my_url, headers=hdr)
		uClient = urllib.request.urlopen(req)
		page_html = uClient.read()
		uClient.close()
		page_soup = soup(page_html, "html.parser")

		#grabs each product from page and adds them to array 'products'
		products = page_soup.findAll("div",{"class":"fs-product-card"})



		#loops through all products and pulls title, price
		for product in products:
			#grabs the header3 which contains title,  strip() removes the formatting \r\n etc
			#title = product.text.replace('\nkg','').replace('\nea','').strip()
			tempnum = product.text.count("\n") -5 

			title = product.text.replace('\n','', tempnum)
			#reverse
			title = title[::-1]
			tempnum = title.count("\n") -1
			title = title.replace('\n','',tempnum)					#LEGIT DONT EVEN TRY FIGURE THIS BIT OUT
			title = title[::-1]
			title = title.replace('\n',' ')
			#title = title.replace(\n)

			#print(title)
			price = None

			#grabs the price
			price = str(product.find("div",{"class":"js-product-card-footer fs-product-card__footer-container"}))
			remove = """<div class="js-product-card-footer fs-product-card__footer-container" data-options='"""
			remove2 = """'></div>"""
			remove3 = '\n'
			remove4 = '\r'
			price = price.replace(remove,'').replace(remove2,'').replace(remove3,'').replace(remove4,'')
			d = json.loads(price)

			a = str(d['ProductDetails'])
			#print(a)
			#print('removing things')
			a = a.partition("'HasMultiBuyDeal'")[0]
			#print(a)
			a=''.join(i for i in a if i.isdigit())
			if len(a) > 3 :
				a = a[0]+a[1]+'.'+a[2]+a[3]
			else :
				a = a[0]+'.'+a[1]+a[2]
				

			price = a

			print("title: "+ title.replace(',','|'))
			print("price: "+price)

			#f.write(title +"," +price +"\n")
			f.write("NW" +"," +title.replace(',','|') +"," +price.replace('$','').replace(' ea','') +"\n")

f.close()


