import pymysql
import warnings
import datetime
warnings.filterwarnings("ignore")

cur = ''
conn = ''
menu = []

def strtodate(string): #convert a string so we could send it
    #string format day - month - year
    string = string.split('-')
    year = int(string[2])
    month = int(string[1])
    day = int(string[0])
    return datetime.date(year,month,day)

def strtodate_time(string):
    #string format day - month - year  hour:minute
    string = string.split('-')
    month = int(string[1])
    day = int(string[0])
    string = string[2].split(' ')
    year = int(string[0])
    string  = string[1].split(':')
    minute = int(string[1])
    hour = int(string[0])
    return datetime.datetime(year,month,day,hour,minute)

def insert_iliko(): #prosthiki ylikou
    global cur,conn
    while (True):
        try:
            iliko= input('Τι υλικό θέλετε να προσθέσουμε;\n')
            mon_met = input('Δώσε μονάδα μέτρησης: ')
            buf = "INSERT INTO iliko(name,monada_metrisis) VALUES('"+iliko+"','"+mon_met+"');"
            cur.execute(buf)
            conn.commit()
            ans = input('Θες να προσθέσουμε κάποιο άλλο υλικό; Αν ναι πατήστε 1, αλλιώς πατήστε κενό για επιστροφή στο αρχικό μενού!\n')
            if (ans!='1'):
                print('Ο νέος πίνακας είναι:')
                print_table('iliko')
                return
        except:
            print("Αδυναμία προσθήκης υλικού!")
            return
        
def insert_dish(): #prosthiki piatou
    global cur,conn
    while True:
        print("Αυτά είναι τα υλικά που έχεις προσθέσει.") #elegxos an thelei o xrhsths na dwsei ki alla ylika
        print_table("iliko")
        if (input('Θες να προσθέσεις κάποιο υλικό; Αν ναι, πάτησε 1 αλλιώς πάτησε κενό.') == '1') :
            insert_iliko()
        
        name = input('Δώσε το όνομα του πιάτου:')
        price = input('Δώσε την τιμή πώλησης του πιάτου:')
        cook_price = input("Δώσε τιμή κατασκευής του πιάτου: ")
        mon_met = input('Δώσε την μονάδα μέτρησης του πιάτου:')
        while True:
            try:
                print("Ωραία! Αυτή είναι η λίστα των μαγείρων! Δώσε το επώνυμο του υπεύθυνου του πιάτου.\n") #elegxos an o mageiras yparxei
                buf = "SELECT afm,last_name FROM ergazomenos WHERE job = 'Μάγειρας'"
                cur.execute(buf)
                result =cur.fetchall()
                for row in result:
                      print(row)
                afm = input()
                cur.execute("SELECT afm from ergazomenos where last_name='"+afm+"';")
                result = cur.fetchone()
                afm = int(result[0])
                break
            except:
                print("Ο υπεύθυνος αυτός δεν υπάρχει")
        dish_sup = afm
        buf = "INSERT INTO piato(onoma,polisis_cost,afm_ipefthinou,cost,monada_metrisis) VALUES('"+name+"','"+price+"',"+str(afm)   +",'"+cook_price+"','"+mon_met+"');"
        cur.execute(buf)
        buf= "SELECT LAST_INSERT_ID()"
        cur.execute(buf)
        dish_code = cur.fetchone()
        dish_code = str(dish_code[0])
        print("Ωραία! Ήρθε η ώρα να προσθέσουμε την συνταγή!")
        ans = '1'
        print("Αυτά είναι τα υλικά που έχεις προσθέσει.")
        print_table("iliko")
        while (ans=='1'):
            try:
                code_il = input("Δώσε όνομα υλικού: ") #elegxos an to yliko yparxei
                cur.execute("SELECT code_ilikou from iliko where name='"+str(code_il)+"';")
                result = cur.fetchone()
                code_il = result[0]
                ammount = input("Δώσε ποσότητα: ")
                buf = "INSERT INTO piato_apoteleitai VALUES('"+dish_code+"','"+str(code_il)+"','"+ammount+"');"
                cur.execute(buf)
                ans = input('Αν θες να προσθέσεις και άλλο συστατικό στην συνταγή πάτησε 1!')
            except:
                print("Δεν υπάρχει αυτό το υλικό!")
        print(name+"\n")
        buf = "SELECT name,posotita,monada_metrisis FROM `piato_apoteleitai` JOIN iliko on code_il=code_ilikou WHERE code_piatou="+(dish_code)+";"
        cur.execute(buf)
        conn.commit()
        res = cur.fetchall()
        for row in res:
            print(row[0] +"\t"+str(float(row[1]))+"\t"+row[2])
        if (input('Θέλεις να προσθέσεις άλλο πιάτο; Εάν ναι πάτησε 1')!='1'):
            break

def insert_order():
    global cur,conn,menu
    while True:
        price =0.0 #prosthiki paraggelias
        print("Αυτά είναι τα πιάτα στο μενού!")
        check_menu()
        datet = strtodate_time(input("Δώσε ημερομηνία και ώρα παραγγελίας με την μορφή Ημέρα-Μήνας-Χρόνος Ώρα:Λεπτά πχ 17-01-2019 17:32 :    "))
        buf = "INSERT INTO paraggelia(date) values('"+str(datet)+"');"
        cur.execute(buf)
        buf= "SELECT LAST_INSERT_ID()"
        cur.execute(buf)
        order_code = cur.fetchone()
        order_code = str(order_code[0])
        print("Προσθήκη προϊόντων στην παραγγελία")
        while True:
            try:
                name = input("Παρακαλώ εισάγετε το όνομα του πιάτου:")
                if name not in dict(menu):
                    print(d)
                buf = "SELECT code_piatou,polisis_cost FROM piato WHERE onoma='"+name+"';"
                cur.execute(buf)
                product = cur.fetchone()
                price += float(product[1])
                product = product[0]
                ammount = int(input("Δώσε ποσότητα:"))
                if ammount>(dict(menu))[name]:
                    print(d)
                buf ="INSERT INTO paraggelia_apoteleitai VALUES("+str(order_code)+","+str(product)+","+str(ammount)+");" #prosthiki sthn vash kai afairesh apo apothiki
                cur.execute(buf)
                buf = "UPDATE apothiki JOIN piato_apoteleitai on apothiki.code_ilkou = piato_apoteleitai.code_il SET apothiki.trexon_apothema = apothiki.trexon_apothema - "
                buf += str(ammount)+"*piato_apoteleitai.posotita WHERE piato_apoteleitai.code_piatou = "+str(product)+" ;"
                cur.execute(buf)
                conn.commit()
            except:
                print("Αυτό το υλικό δεν είναι στο μενού")
                
            ans = input("Θες να προσθέσεις αλλο υλικό; Εάν ναι πάτησε 1!")
            check_menu()
            if (ans!='1'):
                break
        ans = input("Θες να προσθέσεις κι άλλη παραγγελία; Εάν ναι πάτησε 1!")
        if (ans!='1'):
            break


def insert_promithia(): #eisagwgh promhtheias
    global cur,conn
    while True:
        num = input("Δώσε αριθμό τιμολογίου: ")
        date = strtodate(input("Δώσε ημερομηνία έκδοσης τιμολογίου με την μορφή Ημέρα-Μήνας-Χρόνος πχ 17-01-2019: "))
        buf = "INSERT INTO promithia VALUES("+num+",'"+str(date)+"');"
        cur.execute(buf)
        while True:
            print("Αυτή είναι η λίστα με τους προμηθευτές:")
            print_table("promitheftis")
            afm = input("Δώσε το ΑΦΜ του προμηθευτή:")
            try:
                cur.execute("SELECT last_name from promitheftis where afm='"+str(afm)+"';")
                result = cur.fetchone()
                print("Ο προμηθευτής είναι είναι ο: "+result[0])
                break
            except:
                print("Ο προμηθευτής αυτός δεν υπάρχει")
        print("Εισαγωγή προΐόντων στην παραγγελία. Αυτά είναι τα διαθέσιμα υλικά: ")
        print_table("iliko")
        while True:
            name = input("Δώσε όνομα προϊόντος: ")
            try:
                buf = "SELECT code_ilikou FROM iliko WHERE name='"+name+"';"
                cur.execute(buf)
                result = cur.fetchone()
                code = result[0]
                ammount = input("Δώσε ποσότητα: ")
                price = input("Δώσε συνολικό κόστος για το προϊόν: ")
                buf = "INSERT INTO paraggelia_promitheia VALUES("+str(code)+","+afm+","+num+","+ammount+","+price+");"
                cur.execute(buf)
                if (input("Το προϊόν αυτό έχει ημερομηνία λήξης; Εάν ναι πάτησε 1. ") == '1'):
                    deadline = strtodate(input("Δώσε ημερομηνία λήξης του προϊόντος στην μορφή Ημέρα-Μήνας-Έτος. :"))
                else:
                    deadline = strtodate("31-12-2100")
                buf = "INSERT INTO apothiki VALUES ("+str(code)+",'"+str(deadline)+"',"+ammount+");"
                cur.execute(buf)
                
            except:
                ans = input("Δεν υπάρχει αυτό το υλικό! Θες μήπως να το προσθέσεις; Εάν ναι, πάτησε 1")
                if ans == '1':
                    insert_iliko()
            if (input("Θες να προσθέσεις κι άλλο προϊόν στην παραγγελία; Εάν ναι πάτησε 1: ") != '1'):
                    break
                    
            
        conn.commit()
        if (input("Θες να προσθέσεις κι άλλη παραγγελία; Εάν ναι πάτησε 1: ") != '1'):
            return
        
        
        
def insert_promith():
    global cur,conn
    while True: 
        afm = input("Δώσε ΑΦΜ:")
        name = (input("Δώσε Όνομα:"))
        l_name = (input("Δώσε Επώνυμο:"))
        address = (input("Δώσε Διεύθυνση:"))
        city = (input("Δώσε Πόλη:"))
        mail = (input("Δώσε Mail:"))
        home_ph = (input("Δώσε Σταθερό:"))
        mobile_ph =(input("Δώσε Κινητό:"))
        start_date = strtodate(input("Δώσε Ημερομηνία Έναρξης Σύμβασης με την μορφή Ημέρα-Μήνας-Χρόνος πχ 17-01-2019: "))
        end_date = strtodate(input("Δώσε Ημερομηνία Λήξης Σύμβασης με την μορφή Ημέρα-Μήνας-Χρόνος πχ 17-01-2019: "))
        sign_date = strtodate(input("Δώσε Ημερομηνία Σύναψης Σύμβασης με την μορφή Ημέρα-Μήνας-Χρόνος πχ 17-01-2019:    "))

        
        buf= "INSERT INTO simvasi(start_date,end_date) VALUES('"+str(start_date)+"','"+str(end_date)+"');"
        cur.execute(buf)
        buf= "SELECT LAST_INSERT_ID()"
        cur.execute(buf)
        simv_code = cur.fetchone()
        buf = "INSERT INTO promitheftis VALUES('"+afm+"','"+name+"','"+l_name+"','"+address+"','"+\
                          city+"','"+mail+"','"+home_ph+"','"+mobile_ph+"','"+str(simv_code[0])+"','"+str(sign_date)+"');"
        cur.execute(buf)
        conn.commit() 
        ans = input('Θες να προσθέσουμε κάποιον άλλον προμηθευτή; Αν ναι πατήστε 1, αλλιώς πατήστε κενό για επιστροφή στο αρχικό μενού!\n')
        if (ans!='1'):
            print('Ο νέος πίνακας είναι:')
            print_table('promitheftis')
            return

def insert_worker(): #eisagwgh promhthefth
    global cur,conn
    while True:
        afm = input("Δώσε ΑΦΜ:")
        name = (input("Δώσε Όνομα:"))
        l_name = (input("Δώσε Επώνυμο:"))
        address = (input("Δώσε Διεύθυνση:"))
        city = (input("Δώσε Πόλη:"))
        mail = (input("Δώσε Mail:"))
        position = (input("Δώσε Θέση:"))
        home_ph = (input("Δώσε Σταθερό:"))
        mobile_ph =(input("Δώσε Κινητό:"))
        salary = (input("Δώσε Μισθό:"))
        sal_exh = (input("Δώσε Μισθό υπερωρίας:"))
        start_date = strtodate(input("Δώσε Ημερομηνία Έναρξης Σύμβασης με την μορφή Ημέρα-Μήνας-Χρόνος πχ 17-01-2019: "))
        end_date = strtodate(input("Δώσε Ημερομηνία Λήξης Σύμβασης με την μορφή Ημέρα-Μήνας-Χρόνος πχ 17-01-2019: "))
        
        buf= "INSERT INTO simvasi(start_date,end_date) VALUES('"+str(start_date)+"','"+str(end_date)+"');"
        cur.execute(buf)
        buf= "SELECT LAST_INSERT_ID()"
        cur.execute(buf)
        simv_code = cur.fetchone()
        buf = "INSERT INTO ergazomenos VALUES('"+afm+"','"+name+"','"+l_name+"','"+address+"','"+\
                          city+"','"+mail+"','"+position+"','"+home_ph+"','"+mobile_ph+"','"+str(simv_code[0])+"','"+salary+"','"+sal_exh+"');"
        cur.execute(buf)
        conn.commit()
        ans = input('Θες να προσθέσουμε κάποιον άλλον εργαζόμενο; Αν ναι πατήστε 1, αλλιώς πατήστε κενό για επιστροφή στο αρχικό μενού!\n')
        if (ans!='1'):
            print('Ο νέος πίνακας είναι:')
            print_table('ergazomenos')
            return
        
def insert_process(): #eisagwgh epeksergasias ylikoy
    global cur,conn
    while True:
        name = input("Δώσε το όνομα της διαδικασίας: ")
        print_table("iliko")
        if (input('Αυτά ειναι τα υλικά που έχεις προσθέσει. Θες να πρσοθέσεις υλικό; Εάν ναι πάτησε 1!') == '1'):
            insert_iliko()
        try:
            frst = input("Δώσε όνομα πρώτης ύλης: ")
            buf = "SELECT code_ilikou FROM iliko WHERE name='"+frst+"';"
            cur.execute(buf)
            frst = cur.fetchone()
            frst = frst[0]
            qu1 = input("Δώσε ποσότητα που απαιτείται για την πρώτη ύλη: ") 
        except:
            print("Αδύνατη η προσθήκη επεξεργασίας")
            return
        while True:
            print("Προσθήκη δεύτερης ύλης!")
            try:
                scnd = input("Δώσε όνομα δεύτερης ύλης: ")
                buf = "SELECT code_ilikou FROM iliko WHERE name='"+scnd+"';"
                cur.execute(buf)
                scnd = cur.fetchone()
                scnd = scnd[0]
                qu2 = input("Δώσε ποσότητα που απαιτείται για την δεύτερη ύλη: ")
                buf = "INSERT INTO epeksergasia_ilikou VALUES ('"+name+"',"+str(frst)+","+str(scnd)+","+(qu1)+","+(qu2)+");"
                cur.execute(buf)
            except:
                print("Αδύνατη η προσθήκη επεξεργασίας")
            if (input('Η προσθήκη της δεύτερης ύλης ολοκληρώθηκε. Θέλεις να προσθέσεις και άλλη δεύτερη ύλη; Εάν ναι, πάτησε 1:') != '1'):
                break
        conn.commit()
        if (input('Η προσθήκη της διαδικασίας ολοκληρώθηκε. Θέλεις να προσθέσεις και άλλη διαδικασία; Εάν ναι, πάτησε 1:') != '1'):
                break
            

def print_table(table): #ektypwsh pinaka -pretty
    global cur,conn
    buf = "SELECT * FROM "+table+";"
    try:
        cur.execute(buf)
        result = cur.fetchall()
        col = len(result)
        row = len(result[0])
        stri = ''
        for i in range(col):
            for j in range(row):
                stri += str(result[i][j]) + "\t"
            print(stri)
            stri=''
    except:
        print("Άδειος Πίνακας")
    print("\n")
        
def print_store(): #ektypwsh apothikis
    buf = "SELECT iliko.name, apothiki.end_date,apothiki.trexon_apothema,iliko.monada_metrisis FROM apothiki JOIN iliko on apothiki.code_ilkou = iliko.code_ilikou ORDER BY apothiki.end_date, iliko.name"
    try:
        cur.execute(buf)
        result = cur.fetchall()
        col = len(result)
        row = len(result[0])
        stri = ''
        for i in range(col):
            for j in range(row):
                stri += str(result[i][j]) + "\t"
            print(stri)
            stri=''
    except:
        print("Άδειος Πίνακας")
    print("\n")
    
def connect_to_db(): #syndesh sth vash
    global cur,conn
    try:
        conn = pymysql.connect(host='150.140.186.217',user='db19_up1053641',password='up1053641',charset='utf8',database='project_up1053641')
        cur = conn.cursor()
        print("Επιτυχής σύνδεση στην βάση δεδομένων!\n")
    except:
        print("Αποτυχία")
        exit()

def call_init_menu(): #menu
    print('Καλησπέρα!\n')
    while True:
        ans =input('Για προσθήκη πατήστε....1\nΓια εκτύπωση κατάστασης πατήστε 2\nΓια έξοδο πατήστε κενό\n')
        if ans=='1':
            call_prosthiki()
        if ans=='2':
            call_print()
        if ans==' ':
            return

def call_prosthiki(): #menu
    while True:
        ans = input('Για προσθήκη υλικού πατήστε 1\nΓια προσθήκη εργαζόμενου πατήστε 2\nΓια προσθήκη προμηθευτή πατήστε 3\n\
Για προσθήκη πιάτου πατήστε 4\nΓια προσθήκη παραγγελίας πατήστε 5\nΓια εισαγωγή προμήθειας πατήστε 6\nΓια προσθήκη επεξεργασίας υλικού πατήστε 7\nΓια επιστροφή στο μενού πατήστε κενό\n')
        if (ans == '1'):
            insert_iliko()
        if (ans == '2'):
            insert_worker()
        if (ans == '3'):
            insert_promith()
        if (ans == '4'):
            insert_dish()
            check_menu()
        if (ans == '5'):
            insert_order()
            check_menu()
        if (ans == '6'):
            insert_promithia()
            check_menu()
        if (ans =='7'):
            insert_process()
        if (ans == ' '):
            return
        
def call_print(): #menu
    while True:
        ans = input('Για εκτύπωση κατάστασης υλικών πατήστε 1\nΓια εκτύπωση κατάστασης εργαζόμενων πατήστε 2\n\
Για εκτύπωση κατάστασης προμηθευτών πατήστε 3\n\
Για εκτύπωση κατάστασης αποθήκης πατήστε 4\nΓια εκτύπωση μενού πατήστε 5\nΓια επιστροφή στο μενού πατήστε κενό\n')
        if (ans == '1'):
            print("Κατάσταση Υλικών\n")
            print_table("iliko")
        if (ans == '2'):
            print("Κατάσταση Εργαζομένων\n")
            print_table("ergazomenos")
        if (ans == '3'):
            print("Κατάσταση Προμηθευτών\n")
            print_table("promitheftis")
        if (ans == '4'):
            print_store()
        if (ans == '5'):
            check_menu()
        if (ans == ' '):
            return

def check_store():
    global cur,conn
    buf = "DELETE FROM apothiki WHERE end_date< CURRENT_DATE or trexon_apothema<=0"
    cur.execute(buf)
    conn.commit()

def check_menu():
    global cur,conn,menu
    check_store()
    buf = "CREATE VIEW synolo AS SELECT apothiki.code_ilkou as id,sum(apothiki.trexon_apothema) as olo FROM apothiki GROUP BY apothiki.code_ilkou "
    cur.execute(buf)
    buf = "SELECT onoma, floor(min((synolo.olo)/(posotita))) as posothta "
    buf += "FROM piato_apoteleitai JOIN synolo ON piato_apoteleitai.code_il = synolo.id JOIN piato on piato.code_piatou = piato_apoteleitai.code_piatou "
    buf += "WHERE piato_apoteleitai.code_piatou not IN (SELECT piato_apoteleitai.code_piatou FROM piato_apoteleitai left JOIN apothiki on piato_apoteleitai.code_il = apothiki.code_ilkou  "
    buf += "WHERE trexon_apothema is null or synolo.olo<posotita) GROUP BY piato_apoteleitai.code_piatou"
    cur.execute(buf)
    menu = cur.fetchall()
    print("Το μενού σήμερα έχει:")
    for row in menu:    
        print(row[0]+"   Διαθέσιμες Μερίδες:\t"+str(row[1]))
    buf = "DROP VIEW synolo"
    cur.execute(buf)
    print("\n")
    return 

def main():
    connect_to_db()
    check_menu()
    call_init_menu()
    print('Ευχαριστώ πολύ!\n')
        

if __name__=="__main__":
    main()
