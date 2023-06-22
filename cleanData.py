#! /usr/bin/python3
import sqlite3
import re
# connect to a database 
connection = sqlite3.connect('analyst.db')
# create a "cursor" for working with the database
cursorRead = connection.cursor()
cursorWrite = connection.cursor()

cursorRead.execute("SELECT * FROM jobs")
#cursorWrite.execute("ALTER TABLE jobs ADD low INT;")
#cursorWrite.execute("ALTER TABLE jobs ADD high INT;")

for row in cursorRead:
    newRow = []
    isNan = False
    low,high = None,None
    for i in range(1,len(row)-2):
        if row[i] in ['-1',-1,None,'Unknown']:
            newRow.append(None)
            isNan = True
        else:
            if i == 2:
                salary = re.findall(r'\d+', row[i])
                low,high = int(salary[0]),int(salary[1])
            if i == 5:
                cutRank = row[i].split('\n')
                if len(cutRank) == 2:
                    newRow.append(cutRank[0])
                    continue
            if i == 8:
                nums = re.findall(r'\d+', row[i])
                newRow.append(nums[-1])
                continue
            newRow.append(row[i])
    newRow.append(row[0])
    cursorWrite.execute("""UPDATE jobs
                        SET
                        title = ?,
                        salary = ?,
                        description = ?,
                        rating = ?,
                        company = ?,
                        location = ?,
                        headquarters = ?,
                        size = ?,
                        founded = ?,
                        ownership = ?,                                                   
                        industry = ?,
                        sector =?,                
                        revenue = ?,
                        competitors = ?,
                        easyApply =?
                        WHERE id =?;""", tuple(newRow))
    cursorWrite.execute(""" UPDATE jobs
                            SET 
                            low = ?,
                            high = ?
                            WHERE id = ?;""",(low, high, row[0]) )
        
print("missing values after removimng -1 and '-1'from table")
for col in 'title','salary','description','rating','company','location','headquarters','size','founded','ownership','industry','sector','competitors','revenue', 'easyApply':
    cursorRead.execute("SELECT count(id) FROM jobs WHERE " + col + " IS NULL;")
    for row in cursorRead:
        print(col,row[0], str(round(row[0]/2253*100,2)) + "%")

# important: save the changes
connection.commit()
                        
# close db connection
connection.close()
