#!/usr/bin/env python3

import csv

FILE_NAME = 'some.csv'
csv.register_dialect('has_double_quote', delimiter='|', doublequote=True)

def read_from_csv():
    with open(FILE_NAME, 'r', newline='') as f:
        reader = csv.reader(f, 'has_double_quote')
        for i in reader:
            print("{line}: {msg}".format(line=reader.line_num, msg=i))

def write_to_csv():
    with open(FILE_NAME, 'w', newline='') as f:
        writer = csv.writer(f, 'has_double_quote')
        writer.writerow(['name', 'number'])
        writer.writerow(['ak', '9527'])
        writer.writerow(['google', '95"""28'])
        
def read_dic_from_csv():
    with open(FILE_NAME, 'r', newline='') as f:
        reader = csv.DictReader(f, fieldnames=None, dialect='has_double_quote')
        for i in reader:
            print(i)
            print(i.get('number'), i.get('name'),'----')

def write_dic_to_csv():
    dic1 = {'name': 'ak1', 'number': '01'}
    dic2 = {'name': 'ak2', 'number': '02'}
    with open(FILE_NAME, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'number'], dialect="has_double_quote")
        writer.writeheader()
        writer.writerow(dic1)
        writer.writerow(dic2)

def main():
    print('writer_to_csv')
    write_to_csv()
    print('read from csv')
    read_from_csv()
    print('writer dic to csv')
    write_dic_to_csv()
    print('read_dic_from_csv')
    read_dic_from_csv()

if __name__ == '__main__':
    main()
