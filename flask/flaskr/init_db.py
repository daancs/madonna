# import os
# import psycopg2

# conn = psycopg2.connect(
        # host="localhost",
        # database="madonna",
        # user=os.environ['DB_USERNAME'],
        # password=os.environ['DB_PASSWORD'])

# cur = conn.cursor()

# sqlfile = open('schema.sql', 'r')
# cur.execute(sqlfile.read())
# conn.commit()
