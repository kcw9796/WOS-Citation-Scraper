from bs4 import BeautifulSoup
import grequests
import time
import csv
import math


class citation:

	def __init__(self, title, authors, journal, volume, issue, date, email, address, research_areas, authors_keywords, keywords_plus, funding):
		self.title = title
		self.authors = authors
		self.journal = journal
		self.volume = volume
		self.issue = issue
		self.date = date
		self.email = email
		self.address = address
		self.research_areas = research_areas
		self.authors_keywords = authors_keywords
		self.keywords_plus = keywords_plus
		self.funding = funding

	def __iter__(self):
		return iter([self.title, self.authors, self.journal, self.volume, self.issue, self.date, self.email, self.address, self.research_areas, 
					self.authors_keywords, self.keywords_plus, self.funding])

	def print_citation(self):
		print("\n")
		print("Title: {}".format(self.title))
		print("Authors: {}".format('; '.join(self.authors)))
		print("Journal: {}".format(self.journal))
		print("Volume: {}".format(self.volume))
		print("Issue: {}".format(self.issue))
		print("Email: {}".format(self.email))
		print("Address: {}".format(self.address))
		print("Research Areas: {}".format('; '.join(self.research_areas)))
		print("Authors Keywords: {}".format('; '.join(self.authors_keywords)))
		print("Keywords Plus: {}".format('; '.join(self.keywords_plus)))
		print("Funding: ", end='')
		for x in self.funding:
			print(', '.join(x), end='; ')
		print("\n")


def get_links(article):
	# Request the page and use beautifulsoup to parse
	links = []
	urls = [article]
	unsent_request = (grequests.get(url) for url in urls)
	page = grequests.map(unsent_request)[0]
	soup = BeautifulSoup(page.content, 'html.parser')
	citations_link = soup.find('a',title='View all of the articles that cite this one').attrs['href']
	citation_num = int(soup.find('a',title='View all of the articles that cite this one').next_element.contents[0])
	total_pages = math.ceil(citation_num/50)
	urls = []
	for page_num in range(1,total_pages+1):
		urls.append("https://apps.webofknowledge.com"+citations_link+'&page='+str(page_num))
	try:	
		unsent_request = (grequests.get(url) for url in urls)
		pages = grequests.map(unsent_request)
	except:
		"Failed to get links"
	else:
		for page in pages:
			soup = BeautifulSoup(page.content, 'html.parser')

			# The class 'search-results-content' contains a wrapper that holds the link plus other info
			link_elems = soup.find_all("div", class_="search-results-content")
			# Loop through each wrapper element, the first child is an outer div that contains the desired link
			# Search for a link in the first child and grab the href and append it to links with the proper url heading
			for link_elem in link_elems:
				link = link_elem.contents[0].find('a').attrs['href']
				links.append("https://apps.webofknowledge.com"+link)

	return links


def scrape_pages(links):
	# This function receives a list of links to an article page on Web of Science that contains extensive information on the article. 
	# This information includes title, authors, journal name, volume, issue, date, email, address, research areas, keywords, and funding
	# By looking at the source code from one of the articles we can see what tags and class names are used to locate this info
	# This function uses knowledge of those locations to parse out the data and store it in an object called citation

	# Request the pages and use beautifulsoup to parse
	unsent_requests = (grequests.get(link) for link in links)
	results = grequests.map(unsent_requests, size=5)
	for result in results:
		soup = BeautifulSoup(result.content, 'html.parser')
		error_value = 'UNDEFINED'

		# Parse page searching for each element based on source code

		# Find title by looking for class 'title'
		try:
			title = soup.find("div", class_="title").get_text().strip()
		except:
			title = error_value

		# Find journal by looking for class 'sourceTitle'
		try:
			journal = soup.find("p", class_="sourceTitle").get_text().strip()
		except:
			journal = error_value

		# Find volume by looking for the text 'Volume:'
		try:
			volume = soup.find(text="Volume:").parent.parent.get_text().replace("Volume:","").strip()
		except:
			volume = error_value

		# Find issue by looking for the text 'Issue:'
		try:
			issue = soup.find(text="Issue:").parent.parent.get_text().replace("Issue:","").strip()
		except:
			issue = error_value

		# Find date by looking for the text 'Published:'
		try:
			date = soup.find(text="Published:").parent.parent.get_text().replace("Published:","").strip()
		except:
			date = error_value

		# Find email by looking for the text 'E-mail Addresses:'
		try:
			email = soup.find(text="E-mail Addresses:").parent.parent.get_text().replace("E-mail Addresses:","").strip()
		except:
			email = error_value

		# Find address by looking for class 'fr_address_row2'
		try:
			address = soup.find(class_="fr_address_row2").contents[0].strip()
		except:
			address = error_value

		# Find research areas by looking for the text 'Research Areas' to give you a string of all research areas
		try:
			research_areas_string = soup.find(text="Research Areas:").parent.parent.get_text().replace("Research Areas:","").strip()
			research_areas_list = []
			# Loop through each research area by splitting the string by ;
			for research_area in research_areas_string.split(';'):
				research_areas_list.append(research_area.strip())
		except:
			research_areas_list = [error_value]
			
		# Find where the authors are in source code by looking for the title 'Find more records by this author'
		try:
			authors_location = soup.find_all('a',{"title" : "Find more records by this author"})
			author_list = []
			# Loop through each of the authors location and find where the authors name is located
			for author_location in authors_location:
				author_list.append(author_location.next_sibling.replace("(","").replace(")","").strip())
		except:
			authors_list = [error_value]		

		# Find where the authors keywords are in source code by looking for the title 'Find more records by this author keywords'
		try:
			akeywords_location = soup.find_all('a',{"title" : "Find more records by this author keywords"})
			akeywords_list = []
			# Loop through each of the authors keywords location and get the text of each keyword
			for akeywords_location in akeywords_location:
				akeywords_list.append(akeywords_location.get_text().strip())
		except:
			akeywords_list = [error_value]

		# Find where the keywords plus are in source code by looking for the title 'Find more records by this keywords plus'
		try:
			pkeywords_location = soup.find_all('a',{"title" : "Find more records by this keywords plus"})
			pkeywords_list = []
			# Loop through each of the keywords plus location and get the text of each keyword
			for pkeywords_location in pkeywords_location:
				pkeywords_list.append(pkeywords_location.get_text().strip())
		except:
			pkeywords_list = [error_value]

		# Find the table with funding info by looking for class 'fr_data_row'
		try:
			funding_rows = soup.find_all(class_="fr_data_row")
			funding_list = []
			# Loop through each row, the first column represents Funding Agency and the second column represents 
			for funding_row in funding_rows:
				cols = funding_row.find_all('td')
				funding_list.append([cols[0].get_text().strip(),cols[1].get_text().strip()])
		except:
			funding_list = [[error_value]]
			
		# Make citation object using all of parsed data
		x = citation(title=title,authors=author_list,journal=journal,volume=volume,issue=issue,date=date,email=email,address=address,
						research_areas=research_areas_list,authors_keywords=akeywords_list,keywords_plus=pkeywords_list,funding=funding_list)
		x.print_citation()
		write_to_csv(x)


def write_to_csv(citation_obj):
	myFile = open('citations.csv', 'a')
	with myFile:
		writer = csv.writer(myFile, delimiter=',')
		writer.writerow(list(citation_obj))


def main():
	article = input("Enter the article link: ")
	print("Searching Web of Science...\n")
	t0 = time.time()
	links = get_links(article)
	print(links)
	t1 = time.time()
	print("Time Spent To Get Links: {} seconds".format(t1-t0))
	# scrape_pages(link)
	t2 = time.time()
	print("Total Time Spent: {} seconds".format(t2-t0))

if __name__ == '__main__': main()





