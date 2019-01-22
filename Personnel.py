from datetime import datetime
import loadfromsheets

personnel = None
id_to_person_index = None


class Person(object):
    def __init__(self, paygrade: str, link: str, firstname: str, lastname: str, aor: str, status: str, status2,
                 specstatus: str,
                 bct_date: str, pfcdate: str, spcdate: str, cpldate: str,
                 gc: str, bk1: str, bk2: str, bk3: str, sk1: str, sk2: str, sk3: str, gk1: str, gk2: str, gk3: str):
        self.paygrade = paygrade
        self.milpaclink = link
        self.firstname = firstname
        self.lastname=lastname
        self.AOR = aor
        self.status = status
        self.checkstatus = status2
        self.specialstatus = specstatus
        self.bootcampdate = bct_date
        self.PFC_Promo_date = datetime.strptime(pfcdate, '%d-%b-%y')
        self.SPC_Promo_date = datetime.strptime(spcdate, '%d-%b-%y')
        self.CPL_Promo_date = datetime.strptime(cpldate, '%d-%b-%y')
        self.gc = datetime.strptime(gc, '%d-%b-%y')
        self.gc_bk1 = datetime.strptime(bk1, '%d-%b-%y')
        self.gc_bk2 = datetime.strptime(bk2, '%d-%b-%y')
        self.gc_bk3 = datetime.strptime(bk3, '%d-%b-%y')
        self.gc_sk1 = datetime.strptime(sk1, '%d-%b-%y')
        self.gc_sk2 = datetime.strptime(sk2, '%d-%b-%y')
        self.gc_sk3 = datetime.strptime(sk3, '%d-%b-%y')
        self.gc_gk1 = datetime.strptime(gk1, '%d-%b-%y')
        self.gc_gk2 = datetime.strptime(gk2, '%d-%b-%y')
        self.gc_gk3 = datetime.strptime(gk3, '%d-%b-%y')


def loadfromtracker():
    global personnel
    global id_to_person_index

    personnel = []
    # id_to_person_index = []

    # TODO: load data from sheets here
    print("Loading Data from Sheets...")
    data = loadfromsheets.loaddata()
    print("Loaded {0} Records".format(len(data)))
    for i in range(0, len(data)):
        print(data[i])
        print(data[i][0],data[i][1])

        personnel.append(Person(*data[i]))
        print(personnel[i])
