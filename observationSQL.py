#! /usr/bin/python3
import sqlite3
# connect to a database 
connection = sqlite3.connect('analyst.db')
# create a "cursor" for working with the database
cursorRead = connection.cursor()
cursorWrite = connection.cursor()

#cursorWrite.execute("""CREATE TABLE postsPerSectors(
#                                sector TEXT,
#                                avgPosts FLOAT
#                                );"""
#                                )

#cursorWrite.execute("""CREATE TABLE salaries(
#                               location TEXT,
#                               avgLow FLOAT,
#                               avgHigh FLOAT,
#                               avgRating FLOAT,
#                               numOfPosts INT);"""
#                                           )
print('20 sectors with highest number of posts:\n')
cursorRead.execute("SELECT sector,count() AS sector_count FROM jobs WHERE sector IS NOT NULL GROUP BY sector ORDER BY sector_count DESC LIMIT 20;")
for row in cursorRead:
    print(row[0],row[1])

print('\ncontribution of each country pre sector:\n')
cursorRead.execute(""" SELECT sector,COUNT() AS postPerComp 
                FROM jobs 
                WHERE sector is not null 
                AND company is not null 
                GROUP BY company,sector;""")

averageSectors = dict()
for row in cursorRead:
    sector, numOfPosts = row[0], row[1]
    if sector not in averageSectors:
        averageSectors[sector] = {'sum' : numOfPosts, 'count' : 1}
    else:
        averageSectors[sector]['sum'] += numOfPosts
        averageSectors[sector]['count'] += 1;
subresult = []
for key,value in averageSectors.items():
    subresult.append((key,round(value['sum']/value['count'],2)))
subresult.sort(key = lambda x : x[1],reverse = True)
for sector,avg in subresult:
    print(sector,avg)
    #cursorWrite.execute("""INSERT INTO postsPerSectors VALUES (?,?);""",(sector,avg))

cursorRead.execute("""SELECT location,COUNT() AS c, AVG(low) AS avgLow, AVG(high) ,AVG(rating) FROM jobs  GROUP BY location HAVING c >= 15 ORDER BY avgLow DESC; """)
print('\nlocations with mean low salary, mean high salary and mean rating: \n')
for row in cursorRead:
    loc,l,h,rt = row[0],round(row[2],2),round(row[3],2),round(row[4],2)
    print(loc,l,h,rt)
    #cursorWrite.execute("""INSERT INTO salaries VALUES (?,?,?,?,?);""",(loc,l,h,rt,row[1]))

connection.commit()
connection.close()

