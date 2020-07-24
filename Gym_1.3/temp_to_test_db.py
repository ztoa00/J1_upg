from sqlalchemy import create_engine, text

eng = create_engine('sqlite:///database.db')
with eng.connect() as con:
    """
    query = text("INSERT INTO gym(name,contact,foundation,phone,description,instagram,facebook) values('Gym 4','Ztoa','2010','+919092749520','Gym 4 is gym where you can practice boxing and whole bunch of fighting sports,\nThere is also a swimming pool, a workout section......','','')")
    print(query)
    con.execute(query)

    query = text("INSERT INTO gym(name,contact,foundation,phone,description,instagram,facebook) values('Studio A','Marce','2013','+543515222209','Studio A is gym where you can practice all king of exercise and whole bunch of fighting sports,\nThere is also a swimming pool, a workout section......','https://www.instagram.com/instagram/','https://www.facebook.com/faccebook')")
    print(query)
    con.execute(query)
    """

    """
    search_keyword = 'gy'
    query = text("SELECT * From gym WHERE LOWER(REPLACE(name, ' ', '')) LIKE '%{0}%' ;".format(
        search_keyword.replace(" ", "%").lower()))
    reviews = con.execute(query)


    if reviews.fetchall():
        print("xxx")
        print(reviews)

    """
