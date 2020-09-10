
"""
    Avem aplicatia care tine stocul unui depozit (Cap 5-6). Efectuati urmatoarele imbunatatiri:
	
	Este necesar rezolvati minim 5 din punctele de mai jos:

1. Implementati o solutie care sa returneze o proiectie grafica a intrarilor si iesirilor intr-o
anumita perioada, pentru un anumit produs;	--pygal--

2. Implementati o solutie care sa va avertizeze automat cand stocul unui produs este mai mic decat o 
limita minima, predefinita per produs. Limita sa poata fi variabila (per produs). Preferabil sa 
transmita automat un email de avertizare;

3. Creati o metoda cu ajutorul careia sa puteti transmite prin email diferite informatii(
de exemplu fisa produsului) ; 	--SMTP--

4. Utilizati Regex pentru a cauta :
    - un produs introdus de utilizator;
    - o tranzactie cu o anumita valoare introdusa de utilizator;	--re--

5. Creati o baza de date care sa cuprinda urmatoarele tabele:	--pymysql--  sau --sqlite3--
    Categoria
        - idc INT NOT NULL AUTO_INCREMENT PRIMARY KEY (integer in loc de int in sqlite3)
        - denc VARCHAR(255) (text in loc de varchar in sqlite3)
    Produs
        - idp INT NOT NULL AUTO_INCREMENT PRIMARY KEY
        - idc INT NOT NULL
        - denp VARCHAR(255)
        - pret DECIMAL(8,2) DEFAULT 0 (real in loc de decimal)
        # FOREIGN KEY (idc) REFERENCES Categoria.idc ON UPDATE CASCADE ON DELETE RESTRICT
    Operatiuni
        - ido INT NOT NULL AUTO_INCREMENT PRIMARY KEY
        - idp INT NOT NULL
        - cant DECIMAL(10,3) DEFAULT 0
        - data DATE

6. Imlementati o solutie cu ajutorul careia sa populati baza de date cu informatiile adecvate.

7. Creati cateva view-uri cuprinzand rapoarte standard pe baza informatiilor din baza de date. --pentru avansati--

8. Completati aplicatia astfel incat sa permita introducerea pretului la fiecare intrare si iesire.
Pretul de iesire va fi pretul mediu ponderat (la fiecare tranzactie de intrare se va face o medie intre
pretul produselor din stoc si al celor intrate ceea ce va deveni noul pret al produselor stocate).
Pretul de iesire va fi pretul din acel moment;  

9. Creati doua metode noi, diferite de cele facute la clasa, testatile si asigurativa ca functioneaza cu succes;


""" #



-------------------------------------------
# 571 Clase
# Clase
# PF - 10/08/2016

'''
Importati functia datetime din modulul datetime. Instructiune scrisa deja (vezi mai jos)

Creati o clasa 'Stoc' care va avea:
  - o metoda constructor cu
        denumire produs
        categoria
        unitatea de masura default 'Buc'
        sold default 0
        initializati trei dictionare, cu cheie comuna (numerica), pentru data op.,
    intrari si iesiri din stoc, care vor fi atribuite fiecarei instante

  - o metoda intrari cu
        cantitatea,
        data = str ( datetime.now ( ).strftime ( '%Y%m%d' ) )
        testati daca exista chei in dictionarul cu data op. Daca exista stabileste cheia curenta
    ca fiind maximul cheilor existente plus 1, altfel va fi egala cu 1
        introduce in dict intrari cheie si cant
        introduce in dict data cheie si data op
        actualizeaza soldul

  - o metoda iesiri, similara cu precedenta. Diferente: populam dict iesiri

  - o metoda fisa produsului cu urmatoarele specificatii:
        Sa printeze 'Fisa produsului "denumire_produs"' (sa stim si noi a cui e fisa)
        Sa printeze ' Nrc ', '  Data  ', ' Intrare', ' Iesire' pentru toate tranzactiile produsului
        Sa printeze stocul actual al produsului
        pentru avansati - aliniati coloanele

Creati trei instante (produse). Pentru 2 din ele efectuati cate 4-5 operatiuni (intrari, iesiri)

Apelati metoda fisa produsului pentru cele 2 produse
''' #

from datetime import datetime

class Stoc:
    """Tine stocul unui depozit"""

    def __init__(self, prod, categ, um='Buc', sold=0, limita=0):
        self.prod = prod
        self.categ = categ
        self.sold = sold
        self.pret = 0             #CERINTA 8
        self.um = um
        self.i = {}
        self.e = {}
        self.d = {}
        self.sol = {}               # CERINTA 1: AM ADAUGAT UN DICTIONAR PENTRU A TINE EVIDENTA STOCULUI SI A DATEI
        self.limita = limita        #CERINTA 2: DACA STOCUL SCADE SUB ACAESTA LIMITA=> a se vedea metoda iesiri

    def intr(self, cant,pret, data=str(datetime.now().strftime('%Y%m%d'))):
        self.data = data
        self.cant = cant
        self.sold += cant          # recalculam soldul dupa fiecare tranzactie
        #######CERINTA 8
        if (self.pret == 0):
            self.pret = pret
        else:
            self.pret = (self.pret + pret)/2
        ###########SFARSIT CERINTA 8
        self.sol[self.data] = self.sold
        if self.d.keys():               # dictionarul data are toate cheile (fiecare tranzactie are data)
            cheie = max(self.d.keys()) + 1
        else:
            cheie = 1
        self.i[cheie] = cant       # introducem valorile in dictionarele de intrari si data
        self.d[cheie] = self.data

    def iesi(self, cant, data=str(datetime.now().strftime('%Y%m%d'))):
        #   datetime.strftime(datetime.now(), '%Y%m%d') in Python 3.5
        self.data = data
        self.cant = cant
        self.sold -= self.cant
        self.sol[self.data] = self.sold
        self.pret = self.pret              #CERINTA 8, nu am inteles exact partea cu iesirea
        if self.d.keys():
            cheie = max(self.d.keys()) + 1
        else:
            cheie = 1
        self.e[cheie] = self.cant       # similar, introducem datele in dictionarele iesiri si data
        self.d[cheie] = self.data

        #CERINTA 2: DACA STOCUL SCADE SUB LIMITA DATA SE TRIMITE UN MAIL
        if (self.sold < self.limita):
            try:
                import smtplib
                smtp_ob = smtplib.SMTP_SSL("smtp.gmail.com", 465)  #
                mesaj = "Stocul pentru produsul {0} a scazut sub {1}".format(self.prod,self.limita)
                smtp_ob.login('andreineacsu227@gmail.com', '')
                smtp_ob.sendmail("andreineacsu227@gmail.com", "andreineacsu227@gmail.com", mesaj)
                print('Mesaj expediat cu succes!')
            except:
                print('Mesajul nu a putut fi expediat!')
            finally:
                smtp_ob.close()
            #FINAL CERINTA 2


    def fisap(self):

        print('Fisa produsului ' + self.prod + ': ' + self.um)
        print(40 * '-')
        print(' Nrc ', '  Data ', 'Intrari', 'Iesiri')
        print(40 * '-')
        for v in self.d.keys():
            if v in self.i.keys():
                print(str(v).rjust(5), self.d[v], str(self.i[v]).rjust(6), str(0).rjust(6))
            else:
                print(str(v).rjust(5), self.d[v], str(0).rjust(6), str(self.e[v]).rjust(6))
        print(40 * '-')
        print('Stoc actual:      ' + str(self.sold).rjust(10))
        print(40 * '-' + '\n')


    ##############CERINTA 3 + 9:
    def informatiiProduse(self):
        try:
            import smtplib
            smtp_ob = smtplib.SMTP_SSL("smtp.gmail.com", 465)  #
            mesaj = """Informatii despre produsul {0}:
                           -> sold: {1}
                           -> um  : {2}
                           -> pret: {3}""".format(self.prod,self.sold,self.um,self.pret)
            smtp_ob.login('andreineacsu227@gmail.com', '')
            smtp_ob.sendmail("andreineacsu227@gmail.com", "andreineacsu227@gmail.com", mesaj)
            print('Mesaj expediat cu succes!')
        except:
            print('Mesajul nu a putut fi expediat!')
        finally:
            smtp_ob.close()

    def detaliiSuplimentare(self,brand,taraOrig,taraDest,calitatea):
        self.brand = brand
        self.taraOrig = taraOrig
        self.taraDest = taraDest
        self.calitatea = calitatea

    def afisDetaliiSuplimentare(self):
        from prettytable import PrettyTable
        x = PrettyTable()
        x.field_names = ["Brand", "taraOrig", "taraDest", "calitatea"]
        x.add_row([self.brand, self.taraOrig, self.taraDest, self.calitatea])
        print(x)
        ##########FINAL CERINTA 3 + 9



fragute = Stoc('fragute', 'fructe', 'kg')       # cream instantele clasei
lapte = Stoc('lapte', 'lactate', 'litru')
ceasuri = Stoc('ceasuri', 'ceasuri')
iaurt= Stoc('iaurt','lactate','litru')
capsuni = Stoc('capsuni','fructe', 'kg')
banane = Stoc('banane', 'fructe', 'kg')



# 1. Implementati o solutie care sa returneze o proiectie grafica a intrarilor si iesirilor intr-o
# anumita perioada, pentru un anumit produs;	--pygal--

#REZOLVARE: Pentru instantele deja create cu ajutorul functiilor de mai jos, se pot introduce date de
#intrare si de iesire, din care va reiesi graficul odata cu introducerea datelor in mod dinamic;

import pygal;

def adaugaStoc(produs,cantitate,data):
    if isinstance(produs,Stoc):
        bar_chart = pygal.Line()
        bar_chart.no_data_text = "Fara Date"
        bar_chart.title = 'Grafic Stoc'
        bar_chart.human_readable = True
        bar_chart.y_title = 'Stoc Produse'
        bar_chart.x_title = 'Data'
        produs.intr(cantitate,data)
        dictlist = []
        dictlist0 = []
        for value in produs.sol.values():
            dictlist.append(value)
        for value in produs.sol.keys():
            dictlist0.append(value)
        bar_chart.x_labels = dictlist0
        bar_chart.add('Stoc', dictlist)
        bar_chart.render_to_file('{0}.svg'.format(produs.prod))
    else:
        print("NU EXISTA PRODUSUL INTRODUS")

def scadeStoc(produs,cantitate,data):
    if isinstance(produs,Stoc):
        bar_chart = pygal.Line()
        bar_chart.no_data_text = "Fara Date"
        bar_chart.title = 'Grafic Stoc'
        bar_chart.human_readable = True
        bar_chart.y_title = 'Stoc Produse'
        bar_chart.x_title = 'Data'
        produs.iesi(cantitate,data)
        dictlist = []
        dictlist0 = []
        for value in produs.sol.values():
            dictlist.append(value)
        for value in produs.sol.keys():
            dictlist0.append(value)
        bar_chart.x_labels = dictlist0
        bar_chart.add('Stoc', dictlist)
        bar_chart.render_to_file('{0}.svg'.format(produs.prod))
    else:
        print("NU EXISTA PRODUSUL INTRODUS")








#######################################################################################################

# 2. Implementati o solutie care sa va avertizeze automat cand stocul unui produs este mai mic decat o
# limita minima, predefinita per produs. Limita sa poata fi variabila (per produs). Preferabil sa
# transmita automat un email de avertizare;

#REZOLVARE:
   #-> am adaugat un atribut limita care este 0 default sau poate fi dat la instantiere
   #-> atunci cand se apeleaza metoda iesiri, daca stocul scade sub aceasta limita se trimite email(TESTAT)




# 3. Creati o metoda cu ajutorul careia sa puteti transmite prin email diferite informatii
# de exemplu fisa produsului) ; 	--SMTP--

#REZOLVARE: Am creat o metoda in clasa





# 4. Utilizati Regex pentru a cauta :
#     - un produs introdus de utilizator;
#     - o tranzactie cu o anumita valoare introdusa de utilizator;	--re--+

#####!!!!!!!!!DUPA CE SE INSTANTIAZA IAURT de exemplu , se poate apela functia de mai jos si cauta dupa
#####!!!!!!!!! 'iau' si va gasi iaurt

#Nu am intles ce inseamna  - o tranzactie cu o anumita valoare introdusa de utilizator;	--re--+

def cautaProdus():
    import re
    inp = input("Introduceti produsul pe care doriti sa-l cautati")
    sirProduse = ""
    import gc
    for obj in gc.get_objects():
        if isinstance(obj,Stoc):
            if sirProduse == "":
                sirProduse = obj.prod
            else:
                sirProduse = " ".join((sirProduse, obj.prod))
    numeProdList = re.findall('({0}[a-z]+)'.format(inp), sirProduse)
    numpProdSir = numeProdList[0]
    print("Exista produsul introdus si anume: " + numpProdSir)

cautaProdus() #si apoi se poate cauta produsul tantand de exemplu : ban (de la banane) sau iau(de la iaurt)







# 5. Creati o baza de date care sa cuprinda urmatoarele tabele:	--pymysql--  sau --sqlite3--
#     Categoria
#         - idc INT NOT NULL AUTO_INCREMENT PRIMARY KEY (integer in loc de int in sqlite3)
#         - denc VARCHAR(255) (text in loc de varchar in sqlite3)
#     Produs
#         - idp INT NOT NULL AUTO_INCREMENT PRIMARY KEY
#         - idc INT NOT NULL
#         - denp VARCHAR(255)
#         - pret DECIMAL(8,2) DEFAULT 0 (real in loc de decimal)
#         # FOREIGN KEY (idc) REFERENCES Categoria.idc ON UPDATE CASCADE ON DELETE RESTRICT
#     Operatiuni
#         - ido INT NOT NULL AUTO_INCREMENT PRIMARY KEY
#         - idp INT NOT NULL
#         - cant DECIMAL(10,3) DEFAULT 0
#         - data DATE

import sqlite3

dataBase = sqlite3.connect('produse.db')
dataBase.execute('''CREATE TABLE Categoria
                (idc INTEGER PRIMARY KEY NOT NULL,
                denc TEXT);''')
dataBase.execute('''CREATE TABLE Produs
                (idp INTEGER PRIMARY KEY NOT NULL,
                idc int not null,
                denp text,
                pret NUMERIC DEFAULT 0,
                FOREIGN KEY(idc) REFERENCES  Categoria(idc) ON UPDATE CASCADE ON DELETE RESTRICT);''')
dataBase.execute('''CREATE TABLE Operatiuni
                (ido INTEGER PRIMARY KEY NOT NULL,
                idp INTEGER NOT NULL,
                cant NUMERIC DEFAULT 0,
                data TEXT,                                   
                FOREIGN KEY (idp) REFERENCES Produs(idp) ON UPDATE CASCADE ON DELETE RESTRICT);''')
dataBase.commit()
dataBase.close()









#####################################################################################################

# 6. Imlementati o solutie cu ajutorul careia sa populati baza de date cu informatiile adecvate.

#REZOLVARE: La CERINTA 1, am adaugat si functionalitatea ca la fiecare intrare sau iesire sa
#adaugam detaliile corespunzatoare in baza de date


def adaugaStoc(produs,cantitate,data,pret):
    if isinstance(produs,Stoc):
        import pygal
        bar_chart = pygal.Line()
        bar_chart.no_data_text = "Fara Date"
        bar_chart.title = 'Grafic Stoc'
        bar_chart.human_readable = True
        bar_chart.y_title = 'Stoc Produse'
        bar_chart.x_title = 'Data'
        produs.intr(cantitate,pret,data)
        dictlist = []
        dictlist0 = []
        for value in produs.sol.values():
            dictlist.append(value)
        for value in produs.sol.keys():
            dictlist0.append(value)
        bar_chart.x_labels = dictlist0
        bar_chart.add('Stoc', dictlist)
        bar_chart.render_to_file('{0}.svg'.format(produs.prod))
        ###########################PARTEA DE BAZE DE DATE
        import sqlite3
        baza = sqlite3.connect('produse.db',timeout=10)
        #################TABELA Categoria
        print(produs.categ)
        cursor = baza.cursor()
        cursor.execute("SELECT * FROM Categoria where denc = '{0}'".format(produs.categ))
        result = cursor.fetchall()
        if not result:
            baza.execute("INSERT INTO Categoria values(null,'{0}')".format(produs.categ))
        ###################Tabela Produs
        cursor.execute("SELECT * FROM Produs where denp = '{0}'".format(produs.prod))
        result = cursor.fetchall()
        if not result:
            cursor.execute("SELECT * FROM Categoria where denc = '{0}'".format(produs.categ))
            result2 = cursor.fetchall()
            baza.execute("INSERT INTO Produs values(null,'{0}','{1}','{2}')".format(result2[0][0],produs.prod,int(produs.pret)))
        cursor.execute("SELECT * FROM Produs where denp = '{0}'".format(produs.prod))
        result2 = cursor.fetchall()
        ###################Tabela Operatiuni
        baza.execute("INSERT INTO Operatiuni values(null,'{0}','{1}','{2}')".format(result2[0][0],produs.sold,data))
        baza.commit()
        cursor.close()
        baza.close()
    else:
        print("NU EXISTA PRODUSUL INTRODUS")

adaugaStoc(fragute,20,'20191231',10)
adaugaStoc(banane,10,'20200202',5)
adaugaStoc(fragute,5,'20191231',50)
adaugaStoc(iaurt,20,'20200303',100)

dataBase = sqlite3.connect('produse.db')

cursor = dataBase.execute("select * from Categoria;")
for row in cursor:
    print("IDCategorie = ", row[0])
    print("Categorie = ", row[1])
    print("-----------------------------------------")

cursor = dataBase.execute("select * from Produs;")
for row in cursor:
    print("IDProdus = ", row[0])
    print("IDCategorie = ", row[1])
    print("DenumireProdus = ", row[2])
    print("Pret = ", row[3])
    print("-----------------------------------------")


cursor = dataBase.execute("select * from Operatiuni;")
for row in cursor:
    print("IDOperatiune = ", row[0])
    print("IDProdus = ", row[1])
    print("CantitateRamasa = ", row[2])
    print("DataOperatiune = ", row[3])
    print("-----------------------------------------")

#PE FUNCTIA DE SCADE PRODUS AM adaugat sa se faca modificari doar in tabela Operatiuni
#intrucat doar aceste date se modifica atunci cand scoatem produse din stoc

def scadeStoc(produs,cantitate,data):
    if isinstance(produs,Stoc):
        import pygal
        bar_chart = pygal.Line()
        bar_chart.no_data_text = "Fara Date"
        bar_chart.title = 'Grafic Stoc'
        bar_chart.human_readable = True
        bar_chart.y_title = 'Stoc Produse'
        bar_chart.x_title = 'Data'
        produs.iesi(cantitate,data)
        dictlist = []
        dictlist0 = []
        for value in produs.sol.values():
            dictlist.append(value)
        for value in produs.sol.keys():
            dictlist0.append(value)
        bar_chart.x_labels = dictlist0
        bar_chart.add('Stoc', dictlist)
        bar_chart.render_to_file('{0}.svg'.format(produs.prod))
        import sqlite3
        baza = sqlite3.connect('produse.db',timeout=10)
        cursor.execute("SELECT * FROM Produs where denp = '{0}'".format(produs.prod))
        result2 = cursor.fetchall()
        baza.execute("INSERT INTO Operatiuni values(null,'{0}','{1}','{2}')".format(result2[0][0],produs.sold,data))
        baza.commit()
        cursor.close()
        baza.close()
        ###########################PARTEA DE BAZE DE DATE##################
    else:
        print("NU EXISTA PRODUSUL INTRODUS")

scadeStoc(fragute,10,'20190505')

cursor = dataBase.execute("select * from Operatiuni;")
for row in cursor:
    print("IDOperatiune = ", row[0])
    print("IDProdus = ", row[1])
    print("CantitateRamasa = ", row[2])
    print("DataOperatiune = ", row[3])
    print("-----------------------------------------")








# 7. Creati cateva view-uri cuprinzand rapoarte standard pe baza informatiilor din baza de date. --pentru avansati--

import sqlite3

dataBase = sqlite3.connect('produse.db')

dataBase.execute('''CREATE VIEW detaliiProduse
                        AS 
                        SELECT
                            c.idc as IDCategorie,
                            p.idp AS IDProdus,
                            p.denp AS DenumireProdus,
                            p.pret AS PretProdus
                        FROM
                            Categoria c
                        INNER JOIN Produs p ON p.idc = c.idc;''')

dataBase.execute('''CREATE VIEW detaliiComplete
                        AS 
                        SELECT
                            c.idc as IDCategorie,
                            p.idp as IDProdus,
                            p.ido AS IDOperatiune,
                            p.denp AS DenumireProdus,
                            p.pret AS PretProdus,
                            o.cant as Stoc,
                            o.data as Data
                        FROM
                            Categoria c
                        INNER JOIN Produs p ON p.idc = c.idc
                        INNER JOIN Operatiuni o ON o.idp = p.idp;''')

dataBase.commit()

cursor = dataBase.execute("select * from detaliiProduse;")
for row in cursor:
    print("IDCategorie = ", row[0])
    print("IDProdus = ", row[1])
    print("DenumireProdus = ", row[2])
    print("PretProdus = " , row[3])
    print("-----------------------------------------")


cursor = dataBase.execute("select * from detaliiComplete;")
for row in cursor:
    print("IDCategorie = ", row[0])
    print("IDProdus = ", row[1])
    print("IDOperatiune = ", row[2])
    print("DenumireProdus = " , row[3])
    print("PretProdus = " , row[4])
    print("Stoc = " , row[5])
    print("Data Modificare Stoc = " , row[6])
    print("-----------------------------------------")


cursor.close()
dataBase.close()








# 8. Completati aplicatia astfel incat sa permita introducerea pretului la fiecare intrare si iesire.
# Pretul de iesire va fi pretul mediu ponderat (la fiecare tranzactie de intrare se va face o medie intre
# pretul produselor din stoc si al celor intrate ceea ce va deveni noul pret al produselor stocate).
# Pretul de iesire va fi pretul din acel moment;


#REZOLVARE: ->AM ADAUGAT IN MEDOTA DE INTRARE variabila pret ce se modifica conform cerintei
        #   -> se poate vedea implementarea la cerinta 6 unde am adaugat si optiunea de insert a pretului
        #   -> si update-ul acestuia in baza de date





# 9. Creati doua metode noi, diferite de cele facute la clasa, testatile si asigurativa ca functioneaza cu succes;

#REZOLVARE: AM CREAT DOUA METODE NOI. Apelarea lor este jos


fragute.detaliiSuplimentare("TaraMea","Austria","Olanda",1)

fragute.afisDetaliiSuplimentare()



###############################################################################














