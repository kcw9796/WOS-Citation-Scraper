import csv
import json
from citation import citation

def write_obj_to_csv(citation_obj,filename):
	myFile = open(filename, 'a')
	with myFile:
		writer = csv.writer(myFile, delimiter=',')
		writer.writerow(list(citation_obj))

def write_str_to_csv(str_content,filename):
	myFile = open(filename, 'a')
	with myFile:
		writer = csv.writer(myFile, delimiter=',')
		writer.writerow(str_content.split(','))

def make_csv_header_citations(filename):
	x = 'title,authors,journal,volume,issue,date,email,address,research areas,authors keywords,keywords plus,Funding Agency/Grant Number'
	write_str_to_csv(x,filename)

def csv_to_json(csvfilename,jsonfilename):
	csv_rows = []
	with open(csvfilename) as csvfile:
		reader = csv.DictReader(csvfile)
		title = reader.fieldnames
		for row in reader:
			csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
		write_json(csv_rows, jsonfilename)

def write_json(data, jsonfilename):
    with open(jsonfilename, "w") as f:
        if format == "pretty":
            f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '),encoding="utf-8",ensure_ascii=False))
        else:
            f.write(json.dumps(data))