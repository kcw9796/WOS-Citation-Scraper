import csv
from citation import citation
from helper_functions import write_obj_to_csv, init_excel_file, write_excel_page
import geocoder
import collections
import time
import requests

EXCEL_INPUT_FILENAME = '../output_files/PPL_citations_article2.csv'
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

def analyze(csvfilename,output): 	
	raw_addresses = []
	output_addresses = [['Location','Latitude','Longitude','Number of Articles']]
	raw_journals = []
	output_journals = [['Journal','Number of Articles']]
	with open(csvfilename) as csvfile:
		data = csv.DictReader(csvfile)
		for row in data:
			if(row['address']!= 'UNDEFINED'):
				raw_addresses.append(row['address'].split(',')[0])
			if(row['journal']!= 'UNDEFINED'):
				raw_journals.append(row['journal'])
	
	address_counter = collections.Counter(raw_addresses)
	with requests.Session() as session:
		for address in address_counter.most_common():
			address_name = address[0]
			address_count = address[1]
			try:
				g = geocoder.google(address_name, session=session)
				if(g.ok == False):
					time.sleep(1.00)
					g = geocoder.google(address_name, session=session)
				x = location(name=address_name,latitude=g.lat,longitude=g.lng,count=address_count)
				x.print_location()
				output_addresses.append(list(x))
			except:
				continue
	write_excel_page(output_addresses,output,'Map Coordinates')

	journal_counter = collections.Counter(raw_journals)
	for journal in journal_counter.most_common():
		output_journals.append([journal[0],journal[1]])
	write_excel_page(output_journals,output,'Journals')

	output.close()


def main():
	workbook = init_excel_file(EXCEL_OUTPUT_FILENAME)
	analyze(EXCEL_INPUT_FILENAME,workbook)


if __name__ == "__main__":
   main()