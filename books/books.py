# Claire Williams and Luisa Escosteguy
# Revised by Claire Williams and Luisa Escosteguy

import argparse
import csv
import sys

def get_parsed_arguments():
	"""
	Returns arguments from argparser. 
	"""
	parser = argparse.ArgumentParser(description='Process books.csv using a keyword from the title, an author, or a range of publication')
	parser.add_argument('--book', '-b', nargs=1, metavar='S', help='print a list of books whose titles contain the string S')
	parser.add_argument('--author', '-a', nargs=1, metavar='S', help='print a list of authors whose names contain the string S')
	parser.add_argument('--publication','-p', nargs=2, type=int, metavar='year', help='print a list of books published between the two years')
	parsed_arguments = parser.parse_args()
	return parsed_arguments

def filter_books_by_title(title, books):
	"""
	Returns books with titles containing title string.
	"""
	new_books = []
	S = title[0].lower()

	for book in books: 
		if S in book[0].lower():
			new_books.append(book)
	
	return new_books

def filter_books_by_author(author, books):
	"""
	Returns books with authors containing author string.
	"""
	new_books = []
	S = author[0].lower()

	for book in books:
		if S in book[2].lower():
			new_books.append(book)

	return new_books

def filter_books_by_publication(years, books):
	"""
	Returns books with publication year between year range.
	"""
	new_books = []
	
	year_start = min(years)
	year_end = max(years)

	for book in books:
		year_of_publication = int(book[1])
		if year_of_publication >= year_start and year_of_publication <= year_end:
			new_books.append(book)

	return new_books

def print_books(books):
	"""
	Prints books formatted.
	"""
	if not books:
		print("We are sorry. We cannot find any results that match your search criteria.", file=sys.stderr)
		exit()

	dash = '-' * 80
	print(dash)
	print('{:<44s}{:>6s}{:>30s}'.format('Book', 'Year', 'Author'))
	print(dash)
	for i in range(len(books)):
		book_name, year, author = books[i]
		print('{:<44s}{:^6s}{:>30s}'.format(book_name, year, author))

def main():
	arguments = get_parsed_arguments()
	books = csv.reader(open("books.csv", "r"), delimiter=",")

	if not (arguments.book or arguments.author or arguments.publication):
		print("Please add a flag to search for books", file=sys.stderr)
		print("For additional information, enter python3 books.py --help", file=sys.stderr)
		exit()

	if arguments:
		if arguments.book:
			books = filter_books_by_title(arguments.book, books)
		if arguments.author:
			books = filter_books_by_author(arguments.author, books)
		if arguments.publication:
			books = filter_books_by_publication(arguments.publication, books)
	
	print_books(books)

if __name__ == '__main__':
	main()
