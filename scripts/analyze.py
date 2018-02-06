import csv
from citation import citation
from helper_functions import init_excel_file, write_excel_page
import geocoder
import collections
import time
import requests

EXCEL_INPUT_FILENAME = '../output_files/PPL_citations_article.csv'
EXCEL_OUTPUT_FILENAME = '../output_files/PPL_citations_Analysis.xlsx'

class location:
	
	def __init__(self, name, latitude, longitude, count):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude
		self.count = count

	def print_location(self):
		print("\n")
		print("Location: {}".format(self.name))
		print("Coordinates: {}, {}".format(self.latitude,self.longitude))
		print("Count: {}".format(self.count))

	def __iter__(self):
		return iter([self.name, self.latitude, self.longitude, self.count])

def analyze(csvfilename,excel_output): 	
	
	copy_citations_to_excel(csvfilename,excel_output)

	raw_addresses = []
	output_addresses = [['Location','Latitude','Longitude','Number of Repeats']]
	raw_last_authors = []
	output_last_authors = [['Last Author','Number of Repeats']]
	raw_journals = []
	output_journals = [['Journal','Number of Repeats']]
	raw_research_areas = []
	output_research_areas = [['Reasearch Area','Number of Repeats']]
	raw_keywords = []
	output_keywords = [['Keyword','Number of Repeats']]

	with open(csvfilename) as csvfile:
		data = csv.DictReader(csvfile)
		for row in data:
			if(row['address']!= 'UNDEFINED'):
				raw_addresses.append(row['address'].split(',')[0])
			if(row['authors']!= 'UNDEFINED'):
				all_authors = row['authors'].split(';')
				raw_last_authors.append(all_authors[len(all_authors)-1].strip())
			if(row['journal']!= 'UNDEFINED'):
				raw_journals.append(row['journal'])
			if(row['research areas']!= 'UNDEFINED'):
				for research_area in row['research areas'].split(';'):
					if research_area != ' ':
						raw_research_areas.append(research_area.strip())
			if(row['authors keywords']!= 'UNDEFINED'):
				for keyword in row['authors keywords'].split(';'):
					if keyword != ' ':
						raw_keywords.append(keyword.strip())
			if(row['keywords plus']!= 'UNDEFINED'):
				for keyword in row['keywords plus'].split(';'):
					if keyword != ' ':
						raw_keywords.append(keyword.strip())
	
	counter = collections.Counter(raw_addresses)
	with requests.Session() as session:
		print("\nMap Coordinates:")
		for address in counter.most_common():
			address_name = address[0]
			address_count = address[1]
			try:
				time.sleep(0.01)
				g = geocoder.google(address_name, session=session)
				if(g.ok == False):
					time.sleep(1.00)
					g = geocoder.google(address_name, session=session)
				x = location(name=address_name,latitude=g.lat,longitude=g.lng,count=address_count)
				x.print_location()
				output_addresses.append(list(x))
			except:
				continue
	write_excel_page(output_addresses,excel_output,'Map Coordinates')

	analyze_collection(raw_last_authors,output_last_authors,'Last Authors',excel_output)
	analyze_collection(raw_journals,output_journals,'Journals',excel_output)
	analyze_collection(raw_research_areas,output_research_areas,'Research Areas',excel_output)
	analyze_collection(raw_keywords,output_keywords,'Keywords',excel_output)


def analyze_collection(data,output,name,excel_output):
	print("\n{}:".format(name))
	counter = collections.Counter(data)
	for x in counter.most_common():
		output.append([x[0],x[1]])
		print("\n{}: {}".format(name,x[0]))
		print("Number of Repeats: {}".format(x[1]))
	write_excel_page(output,excel_output,name)

def copy_citations_to_excel(csvfilename,output):
	with open(csvfilename) as csvfile:
		output_citations = csv.reader(csvfile)
		write_excel_page(output_citations,output,'Citations')

def main():
	workbook = init_excel_file(EXCEL_OUTPUT_FILENAME)
	analyze(EXCEL_INPUT_FILENAME,workbook)
	workbook.close()


if __name__ == "__main__":
   main()