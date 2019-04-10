from datetime import datetime
import loadfromsheets
from datetime import timedelta

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
        self.lastname = lastname
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


def promo_finder():
    pfc_list = []
    spc_list = []
    cpl_list = []
    global personnel

    week_start, week_end = get_week_range(datetime.today())
    print(week_start, week_end)
    for person in personnel:
        if week_start <= person.PFC_Promo_date <= week_end and (person.status == "Active" or
                                                                person.status == "Military ELOA"):
            print("PFC Promotion due: " + str(person.paygrade) + " " + str(person.firstname) + ", "
                  + str(person.lastname) + " dated: " + str(person.PFC_Promo_date.strftime("%d %b %Y")).upper())
            pfc_list.append(person)
        elif week_start <= person.SPC_Promo_date <= week_end and (person.status == "Active" or
                                                                  person.status == "Military ELOA"):
            print("SPC Promotion due: " + str(person.paygrade) + " " + str(person.firstname) + ", "
                  + str(person.lastname) + " dated: " + str(person.SPC_Promo_date.strftime("%d %b %Y")).upper())
            spc_list.append(person)
        elif week_start <= person.CPL_Promo_date <= week_end and (person.status == "Active" or
                                                                  person.status == "Military ELOA"):
            print("CPL Promotion due? " + str(person.paygrade) + " " + str(person.firstname) + ", "
                  + str(person.lastname) + " dated: " + str(person.CPL_Promo_date.strftime("%d %b %Y")).upper())
            cpl_list.append(person)


def gc_finder():
    global personnel
    bk1_list = []
    bk2_list = []
    bk3_list = []

    day_start, day_end = get_month_range(datetime.today())
    print(day_start, day_end)
    for person in personnel:
        if day_start <= person.gc_bk1 <= day_end and (person.status == "Active" or
                                                              person.status == "Military ELOA"):

            print("First Bronze Knot due: " + str(person.paygrade) + " " + str(person.firstname) + ", "
                  + str(person.lastname) + " dated: " + str(person.gc_bk1.strftime("%d %b %Y")).upper())
            bk1_list.append(person)


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
        personnel.append(Person(*data[i]))
    # print(personnel[i])


def get_week_range(date):
    """ Find the first/last day of the Cav-week for the given day.
    Assuming weeks start on Saturday and end on Friday.
    Returns a tuple of ``(start_date, end_date)``.
    """
    # isocalendar calculates the year, week of the year, and day of the week.
    # dow is Mon = 1, Sat = 6, Sun = 7
    year, week, dow = date.isocalendar()
    # Find the first day of the week.
    if dow == 6:  # Since we want to start with Saturday
        start_date = date
    else:
        # Otherwise, subtract `dow` number days to get the first day
        start_date = date - timedelta(dow)
    # Now, add 6 for the last day of the week (i.e., count up to Friday)
    end_date = start_date + timedelta(6)
    return start_date, end_date


def get_month_range(date):
    first_day = datetime.today().replace(day=1)
    print("first day = " + str(first_day))
    if date.month == 12 and date.year == datetime.today().year:
        last_day = date.replace(day=31)
        print("last day = " + str(last_day))
        return first_day, last_day
    elif date.year == datetime.today().year:
        last_day = date.replace(month=date.month+1, day=1) - timedelta(days=1)
        return first_day, last_day


def get_quarter_range(date):
    """ Find the first/last day of the Cav-week for the given day.
    Assuming weeks start on Saturday and end on Friday.
    Returns a tuple of ``(start_date, end_date)``.
    """
    quarter = int((date.month - 1) / 3 + 1)
    month = 3 * quarter
    remaining = int(month / 12)
    first_day = datetime(date.year, 3 * quarter - 2, 1)
    last_day = datetime(date.year + remaining, month % 12 + 1, 1) + timedelta(days=-1)
    return first_day, last_day


if __name__ == '__main__':
    loadfromtracker()
    # promo_finder()
    print("-----\n Good Conduct Medals:\n----\n")
    gc_finder()
