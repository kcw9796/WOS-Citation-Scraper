import csv
from citation import citation
from helper_functions import write_obj_to_csv
import geocoder
import collections
import time
import requests

EXCEL_INPUT_FILENAME = '../output_files/PPL_citations_article2.csv'
EXCEL_OUTPUT_FILENAME = '../output_files/Map_Coordinates.csv'

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

def analyze(csvfilename): 	
	journals = []
	addresses = []
	with open(csvfilename) as csvfile:
		data = csv.DictReader(csvfile)
		for row in data:
			if(row['address']!= 'UNDEFINED'):
				addresses.append(row['address'].split(',')[0])
			# journals.append(row['journal'])
	# counter = collections.Counter(journals)
	address_counter = collections.Counter(addresses)
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
				write_obj_to_csv(x,EXCEL_OUTPUT_FILENAME)
			except:
				continue


def main():
	analyze(EXCEL_INPUT_FILENAME)



if __name__ == "__main__":
   main()