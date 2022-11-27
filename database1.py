import mysql.connector
mydb = mysql.connector.connect(host='localhost',
                               password='hitchcardio12',
                               user='root',
                               database='hitchcardio')
    
mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE hitchcardio")

#mycursor.execute("SHOW DATABASES")

#mycursor.execute("CREATE TABLE users (name VARCHAR(255), address VARCHAR(225))")

#mycursor.execute("SHOW TABLES")

#mycursor.execute("ALTER TABLE users ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
#mycursor.execute("ALTER TABLE users DROP address")
#mycursor.execute("ALTER TABLE users ADD COLUMN resting_HR VARCHAR(225)")
#mycursor.execute("ALTER TABLE users ADD COLUMN max_HR VARCHAR(225)")
#mycursor.execute("ALTER TABLE users ADD COLUMN VO2_max VARCHAR(225)")


#sql = "INSERT INTO users (name, resting_HR, max_HR, VO2_max) VALUES (%s, %s, %s, %s)"
#val = ("Trevor", "48", "180", "58")
#mycursor.execute(sql, val)

#mycursor.execute("ALTER TABLE users DROP resting_HR")
#mycursor.execute("ALTER TABLE users DROP max_HR")
#mycursor.execute("ALTER TABLE users DROP VO2_max")

#mycursor.execute("ALTER TABLE users ADD COLUMN resting_HR smallint UNSIGNED")
#mycursor.execute("ALTER TABLE users ADD COLUMN max_HR smallint UNSIGNED")
#mycursor.execute("ALTER TABLE users ADD COLUMN VO2_max double")
#mycursor.execute("DESCRIBE users")

    
#mycursor.execute("INSERT INTO users (name, resting_HR, max_HR, VO2_max) VALUES (%s, %s, %s, %s)",("Yujin",39,155,69.0))
#mycursor.execute("DELETE FROM users WHERE id = 4")
#mycursor.execute("UPDATE users SET id = 3 WHERE id = 9")
#mydb.commit()

# example 1
"""
name = "Dr. Helsing"
rHR = 52
mHR = 179
vo2m = 87
mycursor.execute("INSERT INTO users (name, resting_HR, max_HR, VO2_max) VALUES (%s, %s, %s, %s)",(name,rHR,mHR,vo2m))
mydb.commit()
"""

# example 2
"""
mycursor.execute("UPDATE users SET name = 'Dr. Silvera' WHERE name = 'Dr. Helsing'")
mydb.commit()
"""
"""
# example 3
mycursor.execute("UPDATE users SET resting_HR = 55 WHERE resting_HR = 52")
mydb.commit()
"""

# example 4
mycursor.execute("DELETE FROM users WHERE name = 'Dr. Silvera'")
mydb.commit()


mycursor.execute("SELECT * FROM users")
for x in mycursor:
    print(x)


#print(mycursor.rowcount,"record inserted.")

#sql = "INSERT INTO CUSTOMERS (name, address) VALUES ("
