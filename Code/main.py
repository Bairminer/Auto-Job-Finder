import csv

from search import Search

def write_file(filename, data, fields):
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(data)

def main():
    file = open("keywords.txt", "r").read()
    keywords = file.split('\n')
    file = open("badwords.txt", "r").read()
    badwords = file.split('\n')
    # print(keywords)
    s = Search(keywords, badwords)
    data = s.scrape("https://www.indeed.com/jobs?q=hardware+intern&l=US&start=", "https://www.indeed.com/rc")
    data.reverse()
    write_file("out.csv", data, ["url", "score"])

if __name__ == '__main__':
    main()
