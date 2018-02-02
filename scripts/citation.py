
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
		fund_list = []
		for x in self.funding:
			fund_list.append(': '.join(x))
		return iter([self.title, '; '.join(self.authors), self.journal, self.volume, self.issue, self.date, self.email, self.address, '; '.join(self.research_areas), 
					'; '.join(self.authors_keywords), '; '.join(self.keywords_plus), '; '.join(fund_list)])

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





