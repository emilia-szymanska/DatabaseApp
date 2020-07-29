import mysql.connector
from hashlib import blake2b

def Login(login, password):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    hashed = blake2b(key=b'secret', digest_size=10)
    password = password + "bfbfjqbr"
    hashed.update(password.encode())
    password = hashed.hexdigest()
    args = [login, password, '']
    result_args = cur.callproc('logowanie', args)
    cur.close()
    cnx.close()
    return result_args[2]

def GetUserData(login):
    query = """SELECT * FROM wszyscy_uzytkownicy_dane 
            WHERE login = %s """
    
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    cur.execute(query, (login,))
    user_data = cur.fetchone()
    
    cur.close()
    cnx.close()
    return user_data

def ChangeLogin(old, new):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    args = [old, new]
    cur.callproc('zmien_login', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def ChangePwd(login, old, new):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    hashedold = blake2b(key=b'secret', digest_size=10)
    old = old + "bfbfjqbr"
    hashedold.update(old.encode())
    old = hashedold.hexdigest()

    hashednew = blake2b(key=b'secret', digest_size=10)
    new = new + "bfbfjqbr"
    hashednew.update(new.encode())
    new = hashednew.hexdigest()
    args = [login, old, new]
    cur.callproc('zmien_haslo', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def ChangeName(who, whom, new):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, whom, new]
    cur.callproc('zmien_imie', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def ChangeSname(who, whom, new):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, whom, new]
    cur.callproc('zmien_nazwisko', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def ChangeDep(who, whom, new):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, whom, new]
    cur.callproc('zmien_dzial', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def GetDepartments():
    query = """SELECT nazwa_dzialu FROM dzial """
    
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    cur.execute(query)
    dep_data = cur.fetchall()
    departments = []
    for dep in dep_data:
        departments.append(dep[0])
    
    cur.close()
    cnx.close()
    return departments

def GetRights():
    query = """SELECT nazwa_uprawnienia FROM uprawnienia """
    
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    cur.execute(query)
    rig_data = cur.fetchall()
    rights = []
    for rig in rig_data:
        rights.append(rig[0])
    
    cur.close()
    cnx.close()
    return rights

def ChangeRig(who, whom, new):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, whom, new]
    cur.callproc('zmien_uprawnienia', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def GetUsers():
    query = """SELECT login FROM uzytkownik"""
    
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    cur.execute(query)
    usr_data = cur.fetchall()
    users = []
    for usr in usr_data:
        users.append(usr[0])
    
    cur.close()
    cnx.close()
    return users

def GetUsersNamesLogins():
    query = """SELECT * FROM wszyscy_uzytkownicy_dane ORDER BY nazwisko """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    

    cur.execute(query)
    usr_data = cur.fetchall()
    users = []
    for usr in usr_data:
        users.append([f"{usr[0]} {usr[1]} ({usr[3]})", usr[2]])

    cur.close()
    cnx.close()
    return users

def AddNewUser(who, newname, newsname, newlogin, newpwd, department, rights):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    hashed = blake2b(key=b'secret', digest_size=10)
    newpwd = newpwd + "bfbfjqbr"
    hashed.update(newpwd.encode())
    newpwd = hashed.hexdigest()
   
    args = [who, newname, newsname, newlogin, newpwd, department, rights]
    cur.callproc('dodaj_uzytkownika', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def DeleteUser(who, user):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, user]
    cur.callproc('usun_uzytkownika_login', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def UserBasicData(login):
    query = """SELECT * FROM wszyscy_uzytkownicy_dane WHERE login = %s """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    cur.execute(query, (login,))
    usr = cur.fetchone()
    user = f"{usr[0]} {usr[1]} ({usr[3]})"

    cur.close()
    cnx.close()
    return user

def Equipment():
    query = """SELECT * FROM sprzet """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query)
    eqp = cur.fetchall()

    cur.close()
    cnx.close()
    return eqp

def UsEquipment():
    query = """SELECT nazwa FROM sprzet_zuzywalny """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query)
    eqp = cur.fetchall()

    cur.close()
    cnx.close()
    return eqp

def UnUsEquipment():
    query = """SELECT nazwa FROM sprzet_niezuzywalny """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query)
    eqp = cur.fetchall()

    cur.close()
    cnx.close()
    return eqp

def UsableEquipmentKind():
    query = """SELECT rodzaj FROM rodzaj_sprzetu_z """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query)
    eqp = cur.fetchall()
    equip = []
    for x in eqp:
        equip.append(x[0])

    cur.close()
    cnx.close()
    return equip

def AddEqpUs(who, eqpname, amount, kind):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    args = [who, eqpname, amount, kind]
    cur.callproc('dodaj_sprzet_z', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def UnUsableEquipmentKind():
    query = """SELECT rodzaj FROM rodzaj_sprzetu_nz """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query)
    eqp = cur.fetchall()
    equip = []
    for x in eqp:
        equip.append(x[0])

    cur.close()
    cnx.close()
    return equip

def AddEqpUnUs(who, eqpname, kind):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, eqpname, kind]
    cur.callproc('dodaj_sprzet_nz', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def AddEqpUsKind(who, kindname):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, kindname]
    cur.callproc('dodaj_rodzaj_sprzetu_z', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def AddEqpUnUsKind(who, kindname, maxdays):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, kindname, maxdays]
    cur.callproc('dodaj_rodzaj_sprzetu_nz', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def GetDebtUsers():
    query = """SELECT * FROM uzytkownicy_zadluzeni """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    cur.execute(query)
    usr_data = cur.fetchall()
    users = []
    for usr in usr_data:
        users.append(f"{usr[0]} {usr[1]} ({usr[2]}) : {usr[3]} : {usr[4]}")

    cur.close()
    cnx.close()
    return users

def DeleteUsKind(who, kindname):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, kindname]
    cur.callproc('usun_rodzaj_sprzetu_z', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def DeleteUnUsKind(who, kindname):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, kindname]
    cur.callproc('usun_rodzaj_sprzetu_nz', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def GetUnavailUsEqp():
    query = """SELECT * FROM niedostepny_sprzet_z """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    

    cur.execute(query)
    eqp_data = cur.fetchall()
    eqp = []
    for x in eqp_data:
        eqp.append([f"{x[1]} ({x[0]})", x[1]])

    cur.close()
    cnx.close()
    return eqp

def GetUnavailUnUsEqp():
    query = """SELECT * FROM zamowienia_nz_niezwrocone ORDER BY 'nazwa sprzętu'"""
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    

    cur.execute(query)
    eqp_data = cur.fetchall()
    eqp = []
    for x in eqp_data:
        eqp.append([f"{x[4]} ({x[3]})", x[4]])

    cur.close()
    cnx.close()
    return eqp

def UnUsableEquipmentDaysKind():
    query = """SELECT * FROM rodzaj_sprzetu_nz """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query)
    eqp = cur.fetchall()
    equip = []
    for x in eqp:
        equip.append([f"{x[1]} ({x[2]} dni)", x[1]])

    cur.close()
    cnx.close()
    return equip

def ChangeMaxBorrow(who, kind, days):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, kind, days]
    cur.callproc('zmien_rodzaj_nz_max_wyp', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def CurrentMaxBorrow(kindname):
    query = """SELECT max_wypozyczenie FROM rodzaj_sprzetu_nz WHERE rodzaj_sprzetu_nz.rodzaj = %s """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (kindname,))
    days = cur.fetchone()
    result = str(days[0])

    cur.close()
    cnx.close()
    return result

def IfUsable(eqpname):
    query = """ SELECT EXISTS (SELECT * from sprzet_zuzywalny WHERE sprzet_zuzywalny.nazwa = %s) """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (eqpname,))
    result = cur.fetchone()
    cur.close()
    cnx.close()

    response = result[0]

    if response == 1:
        return True
    else:
        return False

def IfUsableKind(eqpname):
    query = """ SELECT EXISTS (SELECT * from rodzaj_sprzetu_z WHERE rodzaj_sprzetu_z.rodzaj = %s) """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (eqpname,))
    result = cur.fetchone()
    cur.close()
    cnx.close()

    response = result[0]

    if response == 1:
        return True
    else:
        return False

def IfBorrowed(eqpname):
    query = """ SELECT EXISTS (SELECT * from uzytkownicy_wypozyczajacy WHERE uzytkownicy_wypozyczajacy.sprzet_wypozyczony = %s) """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (eqpname,))
    result = cur.fetchone()
    cur.close()
    cnx.close()

    response = result[0]

    if response == 1:
        return True
    else:
        return False

def BorrowData(eqpname):
    query = """ SELECT * from uzytkownicy_wypozyczajacy WHERE uzytkownicy_wypozyczajacy.sprzet_wypozyczony = %s """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (eqpname,))
    result = cur.fetchone()

    response = [result[0], result[1], result[4]]

    cur.close()
    cnx.close()
    return response

def DeleteEqp(who, eqpname):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, eqpname]
    usable = IfUsable(eqpname)


    if usable == True:
        cur.callproc('usun_sprzet_z', args)
    else:
        cur.callproc('usun_sprzet_nz', args)

    cnx.commit()
    cur.close()
    cnx.close()

def UsEqpData(eqpname):
    query = """ SELECT * from sprzet_z WHERE sprzet_z.nazwa = %s """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (eqpname,))
    eqp_data = cur.fetchone()
   
    eqp = [eqp_data[1], eqp_data[0], str(eqp_data[2])]

    cur.close()
    cnx.close()
    return eqp

def UnUsEqpData(eqpname):
    query = """ SELECT * from sprzet_nz WHERE sprzet_nz.nazwa = %s """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (eqpname,))
    eqp_data = cur.fetchone()

    borrowed = IfBorrowed(eqpname)

    if borrowed == True:
        bordata = BorrowData(eqpname)
        eqp = [eqp_data[1], eqp_data[0], f"Wypozyczony przez {bordata[0]} {bordata[1]} do {bordata[2]}"]
    else: 
        eqp = [eqp_data[1], eqp_data[0], "Niewypozyczony"]

    cur.close()
    cnx.close()
    return eqp

def ModUsEqpKind(who, eqpname, kindname):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, eqpname, kindname]
    cur.callproc('zmien_sprzet_z_rodzaj', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def ModUnUsEqpKind(who, eqpname, kindname):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, eqpname, kindname]
    cur.callproc('zmien_sprzet_nz_rodzaj', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def ChangeEqpUsName(who, eqpname, neweqpname):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, eqpname, neweqpname]
    cur.callproc('zmien_sprzet_z_nazwa', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def ChangeEqpUnUsName(who, eqpname, neweqpname):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, eqpname, neweqpname]
    cur.callproc('zmien_sprzet_nz_nazwa', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def ChangeEqpUsNr(who, eqpname, neweqpnr):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [who, neweqpnr, eqpname]
    cur.callproc('zmien_sprzet_z_liczba', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def IsUsNameUnique(eqpname):
    query = """ SELECT EXISTS (SELECT * from sprzet_zuzywalny WHERE sprzet_zuzywalny.nazwa = %s) """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (eqpname,))
    result = cur.fetchone()
    cur.close()
    cnx.close()

    response = result[0]

    if response == 1:
        return False
    else:
        return True

def IsUnUsNameUnique(eqpname):
    query = """ SELECT EXISTS (SELECT * from sprzet_niezuzywalny WHERE sprzet_niezuzywalny.nazwa = %s) """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (eqpname,))
    result = cur.fetchone()
    cur.close()
    cnx.close()

    response = result[0]

    if response == 1:
        return False
    else:
        return True

def IsUsKindUnique(eqpname):
    query = """ SELECT EXISTS (SELECT * from rodzaj_sprzetu_z WHERE rodzaj_sprzetu_z.rodzaj = %s) """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (eqpname,))
    result = cur.fetchone()
    cur.close()
    cnx.close()

    response = result[0]

    if response == 1:
        return False
    else:
        return True

def IsUnUsKindUnique(eqpname):
    query = """ SELECT EXISTS (SELECT * from rodzaj_sprzetu_nz WHERE rodzaj_sprzetu_nz.rodzaj = %s) """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (eqpname,))
    result = cur.fetchone()
    cur.close()
    cnx.close()

    response = result[0]

    if response == 1:
        return False
    else:
        return True

def IsLoginUnique(login):
    query = """ SELECT EXISTS (SELECT * from uzytkownik WHERE uzytkownik.login = %s) """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (login,))
    result = cur.fetchone()
    cur.close()
    cnx.close()

    response = result[0]

    if response == 1:
        return False
    else:
        return True

def UsEquipByKind(eqpkind):
    query = """ SELECT * from sprzet_z WHERE sprzet_z.rodzaj = %s """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (eqpkind,))
    eqp_data = cur.fetchall()
    eqp = []
    for x in eqp_data:
        eqp.append(x[1])

    cur.close()
    cnx.close()
    return eqp

def UnUsEquipByKind(eqpkind):
    query = """ SELECT * from sprzet_nz WHERE sprzet_nz.rodzaj = %s """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (eqpkind,))
    eqp_data = cur.fetchall()
    eqp = []
    for x in eqp_data:
        eqp.append(x[1])

    cur.close()
    cnx.close()
    return eqp

def Search(type, kind, searching):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    if type == "Wybierz typ":
        query = """ SELECT * from sprzet WHERE sprzet.nazwa LIKE %s """
        cur.execute(query, ('%'+searching+'%',))
        eqp_data = cur.fetchall()
        eqp = []
        for x in eqp_data:
            eqp.append(x[0])
        cnx.commit()
        cur.close()
        cnx.close()
        return eqp
    else:
        if type == "Sprzety zuzywalne":
            if kind != "Wybierz rodzaj":
                query = """ SELECT * from sprzet_z WHERE sprzet_z.rodzaj = %s AND sprzet_z.nazwa LIKE %s """
                cur.execute(query, (kind,'%'+searching+'%'))
                eqp_data = cur.fetchall()
                eqp = []
                for x in eqp_data:
                    eqp.append(x[1])
                cnx.commit()
                cur.close()
                cnx.close()
                return eqp
            else:
                query = """ SELECT * from sprzet_z WHERE sprzet_z.nazwa LIKE %s """
                cur.execute(query, ('%'+searching+'%',))
                eqp_data = cur.fetchall()
                eqp = []
                for x in eqp_data:
                    eqp.append(x[1])
                cnx.commit()
                cur.close()
                cnx.close()
                return eqp
        else:
            if kind != "Wybierz rodzaj":
                query = """ SELECT * from sprzet_nz WHERE sprzet_nz.rodzaj = %s AND sprzet_nz.nazwa LIKE %s """
                cur.execute(query, (kind,'%'+searching+'%'))
                eqp_data = cur.fetchall()
                eqp = []
                for x in eqp_data:
                    eqp.append(x[1])
                cnx.commit()
                cur.close()
                cnx.close()
                return eqp
            else:
                query = """ SELECT * from sprzet_nz WHERE sprzet_nz.nazwa LIKE %s """
                cur.execute(query, ('%'+searching+'%',))
                eqp_data = cur.fetchall()
                eqp = []
                for x in eqp_data:
                    eqp.append(x[1])
                cnx.commit()
                cur.close()
                cnx.close()
                return eqp

def AvailEquipment():
    query = """SELECT * FROM dostepny_sprzet_z """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query)
    eqp_data = cur.fetchall()
    eqp = []
    for x in eqp_data:
        eqp.append([f"{x[1]} (na stanie: {x[2]})", x[1]])

    query = """SELECT * FROM dostepny_sprzet_nz """
    cur = cnx.cursor(buffered=True)
    cur.execute(query)
    eqp_data2 = cur.fetchall()
    for x in eqp_data2:
        eqp.append([f"{x[1]} (maks. wyp. : {x[2]})", x[1]])

    cur.close()
    cnx.close()
    return eqp

def SearchAvail(type, kind, searching):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    if type == "Wybierz typ":
        query = """ SELECT * from dostepny_sprzet_z WHERE dostepny_sprzet_z.nazwa LIKE %s """
        cur.execute(query, ('%'+searching+'%',))
        eqp_data = cur.fetchall()
        eqp = []
        for x in eqp_data:
            eqp.append([f"{x[1]} (na stanie: {x[2]})", x[1], x[2]])
        query = """ SELECT * from dostepny_sprzet_nz WHERE dostepny_sprzet_nz.nazwa LIKE %s """
        cur.execute(query, ('%'+searching+'%',))
        eqp_data2 = cur.fetchall()
        for x in eqp_data2:
            eqp.append([f"{x[1]} (maks. wyp. : {x[2]})", x[1], x[2]])
        cnx.commit()
        cur.close()
        cnx.close()
        return eqp
    else:
        if type == "Sprzety zuzywalne":
            if kind != "Wybierz rodzaj":
                query = """ SELECT * from dostepny_sprzet_z WHERE dostepny_sprzet_z.rodzaj = %s AND dostepny_sprzet_z.nazwa LIKE %s """
                cur.execute(query, (kind,'%'+searching+'%'))
                eqp_data = cur.fetchall()
                eqp = []
                for x in eqp_data:
                    eqp.append([f"{x[1]} (na stanie: {x[2]})", x[1], x[2]])
                cnx.commit()
                cur.close()
                cnx.close()
                return eqp
            else:
                query = """ SELECT * from dostepny_sprzet_z WHERE dostepny_sprzet_z.nazwa LIKE %s """
                cur.execute(query, ('%'+searching+'%',))
                eqp_data = cur.fetchall()
                eqp = []
                for x in eqp_data:
                    eqp.append([f"{x[1]} (na stanie: {x[2]})", x[1], x[2]])
                cnx.commit()
                cur.close()
                cnx.close()
                return eqp
        else:
            if kind != "Wybierz rodzaj":
                query = """ SELECT * from dostepny_sprzet_nz WHERE dostepny_sprzet_nz.rodzaj = %s AND dostepny_sprzet_nz.nazwa LIKE %s """
                cur.execute(query, (kind,'%'+searching+'%'))
                eqp_data = cur.fetchall()
                eqp = []
                for x in eqp_data:
                    eqp.append([f"{x[1]} (maks. wyp. : {x[2]})", x[1], x[2]])
                cnx.commit()
                cur.close()
                cnx.close()
                return eqp
            else:
                query = """ SELECT * from dostepny_sprzet_nz WHERE dostepny_sprzet_nz.nazwa LIKE %s """
                cur.execute(query, ('%'+searching+'%',))
                eqp_data = cur.fetchall()
                eqp = []
                for x in eqp_data:
                    eqp.append([f"{x[1]} (maks. wyp. : {x[2]})", x[1], x[2]])
                cnx.commit()
                cur.close()
                cnx.close()
                return eqp

def AvailUsEquipment():
    query = """SELECT * FROM dostepny_sprzet_z """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query)
    eqp_data = cur.fetchall()

    eqp = []
    for x in eqp_data:
        eqp.append([f"{x[1]} (na stanie: {x[2]})", x[1], x[2]])

    cur.close()
    cnx.close()
    return eqp

def AvailUnUsEquipment():
    query = """SELECT * FROM dostepny_sprzet_nz """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query)
    eqp_data = cur.fetchall()

    eqp = []
    for x in eqp_data:
        eqp.append([f"{x[1]} (maks. wyp. : {x[2]})", x[1], x[2]])

    cur.close()
    cnx.close()
    return eqp

def AvailUsEquipByKind(eqpkind):
    query = """ SELECT * from dostepny_sprzet_z WHERE dostepny_sprzet_z.rodzaj = %s """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (eqpkind,))
    eqp_data = cur.fetchall()
    eqp = []
    for x in eqp_data:
        eqp.append([f"{x[1]} (na stanie: {x[2]})", x[1], x[2]])

    cur.close()
    cnx.close()
    return eqp

def AvailUnUsEquipByKind(eqpkind):
    query = """ SELECT * from dostepny_sprzet_nz WHERE dostepny_sprzet_nz.rodzaj = %s """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (eqpkind,))
    eqp_data = cur.fetchall()
    eqp = []
    for x in eqp_data:
        eqp.append([f"{x[1]} (maks. wyp. : {x[2]})", x[1], x[2]])

    cur.close()
    cnx.close()
    return eqp

def UsOrders():
    query = """SELECT * FROM zamowienia_z """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query)
    ord_data = cur.fetchall()
    ord = []
    dict = {}
    for x in ord_data:
        if dict.get(str(x[2])) == None:
            ord.append([f"{x[0]} {x[1]} - zam. nr {x[2]} z dnia {x[6]}", x[2]])
            dict[str(x[2])] = 1

    cur.close()
    cnx.close()
    return ord

def UnUsOrders():
    query = """SELECT * FROM zamowienia_nz_wszystkie """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query)
    ord_data = cur.fetchall()
    ord = []
    dict = {}
    for x in ord_data:
        if dict.get(str(x[2])) == None:
            ord.append([f"{x[0]} {x[1]} - zam. nr {x[2]} z dnia {x[5]}", x[2]])
            dict[str(x[2])] = 1

    cur.close()
    cnx.close()
    return ord

def UsOrderContent(nr):
    query = """ SELECT * from zamowienia_z WHERE zamowienia_z.numer_zamowienia = %s """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (nr,))
    ord_data = cur.fetchall()
    ord = []
    equip = []
    for x in ord_data:
        equip.append(f"{x[4]} ({x[3]}) - {x[5]} szt. ")

    ord.append(f"{ord_data[0][0]} {ord_data[0][1]}")
    ord.append(str(ord_data[0][6]))
    ord.append(equip)
    cur.close()
    cnx.close()
    return ord

def UnUsOrderContent(nr):
    query = """ SELECT * from zamowienia_nz_wszystkie WHERE zamowienia_nz_wszystkie.numer_zamowienia = %s """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (nr,))
    ord_data = cur.fetchall()
    ord = []
    equip = []
    for x in ord_data:
        if x[7] == None:
            equip.append(f"{x[4]} ({x[3]}) do {x[6]}")
        else:
            equip.append(f"{x[4]} ({x[3]}) - zwrocono {x[7]}")

    ord.append(f"{ord_data[0][0]} {ord_data[0][1]}")
    ord.append(str(ord_data[0][6]))
    ord.append(equip)
    cur.close()
    cnx.close()
    return ord

def UnUsOrderEqp(who):
    query = """SELECT * FROM zamowienia_nz_niezwrocone_loginy WHERE zamowienia_nz_niezwrocone_loginy.login = %s """
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    cur.execute(query, (who,))
    ord_data = cur.fetchall()
    ord = []

    for x in ord_data:
        ord.append([f"{x[3]} ({x[2]}) do {x[5]}", x[3]])

    cur.close()
    cnx.close()
    return ord

def ReturnEqp(eqpname):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)
    
    args = [eqpname]
    cur.callproc('zwrot_sprzetu_nz', args)
    
    cnx.commit()
    cur.close()
    cnx.close()

def MakeUsOrder(who, cart):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    args = [who, '']

    args = cur.callproc('zlozenie_zamowienia_z', args)

    order_number = args[1]

    for i in cart:
        args = [ order_number, i['nazwa'], i['ilosc'] ]
        cur.callproc('dodanie_elementu_zamowienia_z', args)

    cnx.commit()
    cur.close()
    cnx.close()

def MakeUnUsOrder(who, cart):
    cnx = mysql.connector.connect(user='sudo', password='xbxbpun', database='bd_projekt')
    cur = cnx.cursor(buffered=True)

    args = [who, '']

    args = cur.callproc('zlozenie_zamowienia_nz', args)

    order_number = args[1]

    for i in cart:
        args = [ order_number, i['nazwa'], i['ilosc'] ]
        cur.callproc('dodanie_elementu_zamowienia_nz', args)

    cnx.commit()
    cur.close()
    cnx.close()