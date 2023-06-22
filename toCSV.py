#! /usr/bin/python3
import sqlite3
connection = sqlite3.connect('analyst.db') 
cursorRead = connection.cursor() 
def fetch_table_data(table_name):
        cursorRead.execute('select * from ' + table_name)
        header = [row[0] for row in cursorRead.description]
        rows = cursorRead.fetchall()
        return header,rows

def export(table_name):
        header, rows = fetch_table_data(table_name)        
        f = open(table_name + '.csv', 'w')
        f.write(','.join(header) + '\n')

        for row in rows:
            writeRow = []
            for r in row:
                if isinstance(r,str): 
                    writeRow.append("\"" + str(r.replace("\"","")) + "\"")
                else :
                    writeRow.append(str(r)) 
            
            print(writeRow[-2])

            f.write(','.join(writeRow) + '\n')

        f.close()
        print(str(len(rows)) + ' rows written successfully to ' + f.name)

export('salaries')
export('postsPerSectors')
export('jobs')
