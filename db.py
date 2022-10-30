import pymysql as ps

ID = []
passw = []
try:
    db = ps.connect(
        host = "localhost",
        user= "root",
        password = "Mcg0d516!",
        db = "enai_db"
    )

    print("connected")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user")
    databases = cursor.fetchall()

    for i in databases:
        for col in i:
            print(col,end=' ')
        print()
    
    db.close()

except Exception as e:
    print(e)