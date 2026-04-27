def initialize():
    import pymysql as db
    from data_org import student,students_subject,read_file,writing_to_binary_file
    import json
    import os

    con = db.connect(host = 'localhost',password='G@v!nd',user='root')
    cur = con.cursor()
    querry = 'CREATE DATABASE RESULT'

    cur.execute(querry)
    con.commit()
    querry = 'USE RESULT'
    cur.execute(querry)
    con.commit()

    querry = 'CREATE TABLE STUDENTS(ROLL INT,NAME TEXT, GENDER TEXT,PERCENTAGE FLOAT,STREAM CHAR(3))'
    cur.execute(querry)
    con.commit()



    path = input(r"Enter the path to txt file provided by cbse center.>")
    writing_to_binary_file(path)
    st_rec = read_file(path)
    with open('prsnt_sb_cds.json','r') as f:
        temp_data = json.load(f)
        subcodes = temp_data['present_subcodes']
    subjects_with_cds = {}
    with open('subcodes.json','r') as f:
        temp_data = json.load(f)
        for i in subcodes:
            if i not in subjects_with_cds:
                subjects_with_cds[i] = temp_data[i]
        del subcodes
        del temp_data
    for i in subjects_with_cds:
        querry = "CREATE TABLE {}(ROLL INT,MARKS INT,GRADES CHAR(3))".format(subjects_with_cds[i])
        cur.execute(querry)
        con.commit()

    for stdnt in st_rec:
        querry = "INSERT INTO STUDENTS(ROLL,NAME,GENDER,PERCENTAGE,STREAM) VALUES({},'{}','{}',{},'{}')".format(stdnt.roll,stdnt.name,stdnt.gender,stdnt.percentage,stdnt.stream)
        cur.execute(querry)
        con.commit()
# ['21689866', 'RANI YADAV', 'Female', ({'301': ('098', 'A1')}, {'028': ('100', 'A1')}, {'048': ('100', 'A1')}, {'037': ('100', 'A1')}, {'027': ('096', 'A1')}, {'049': ('100', 'A1')})]
# ['21689844', '    ROHIT SINGH', 'Male', ({'301': ('067', 'C2')}, {'054': ('048', 'D1')}, {'055': ('026', 'E')}, {'030': ('046', 'D2')}, {'049': ('083', 'D1')}, {'041': ('021', 'E')})]
# [roll,name,gen,tuple(dictsub(str code:tuple(strmrk,strgrd))]
        for sbjct in stdnt.subjects:
            querry = "INSERT INTO {}(ROLL,MARKS,GRADES) VALUES({},{},'{}')".format(subjects_with_cds[sbjct.code],stdnt.roll,sbjct.marks,sbjct.grade)
            cur.execute(querry)
            con.commit()
    
    with open('Present_st_data.json','r') as f:
        temp_for_present_st_data = json.load(f)
        querry = "CREATE TABLE PRESENT_DATA(TOTAL_CANDIDATES INT,TOTAL_PASS INT,TOTAL_COMPTT INT,TOTAL_ESSENTIAL_REPEAT INT,TOTAL_ABSENT INT)"
        cur.execute(querry)
        con.commit()
        values = tuple([temp_for_present_st_data[i] for i in temp_for_present_st_data])
        querry = "INSERT INTO PRESENT_DATA VALUES{}".format(values)
        cur.execute(querry)
        con.commit()
        


    cur.close()
    con.close()
    os.remove("Present_st_data.json")
    os.remove(path[:-3]+'bin')
    os.remove("prsnt_sb_cds.json")
