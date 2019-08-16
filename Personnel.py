from datetime import datetime
import loadfromsheets
from datetime import timedelta

personnel = None
id_to_person_index = None


class Person(object):
    def __init__(self, paygrade: str, link: str, firstname: str, lastname: str, aor: str, status: str, status2,
                 specstatus: str, bct_date: str, pfcdate: str, spcdate: str, cpldate: str, ncoabool: bool, sacbool: bool,
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
        self.NCOA = ncoabool
        self.SAC = sacbool
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


def paygrade2rank(inperson):
    paygrades = ["E-3 PFC", "E-4A SPC", "E-4B CPL", "E-5 SGT", "E-6 SSG", "E-7 SFC", "E-8 1SG", "E-9A SGM", "E-9B CSM",
                 "O-01 2LT", "O-02 1LT", "O-03 CPT", "O-04 MAJ", "O-05 LTC", "O-06 COL", "O-07 BG", "O-08 MG", "O-09 ",
                 "O-10A GEN", "O-10B GOA", "W-1 WO1", "W-2 CW2", "W-3 CW3", "W-4 CW4", "W-5 CW5"]
    ranks = ["Private First Class", "Specialist", "Corporal", "Sergeant", "Staff Sergeant", "Sergeant First Class",
             "First Sergeant", "Sergeant Major", "Command Sergeant Major", "Second Lieutenant", "First Lieutenant",
             "Captain", "Major", "Lieutenant Colonel", "Colonel", "Brigadier General", "Major General", " General2",
             "General", "General of the Army", "Warrant Officer 1","Chief Warrant Officer 2", "Chief Warrant Officer 3",
             "Chief Warrant Officer 4", "Chief Warrant Officer 5"]
    if inperson.paygrade in paygrades:
        inperson.rank = ranks[paygrades.index(inperson.paygrade)]
    else:
        inperson.rank = "Not Found"


def promo_finder():
    pfc_list = []
    spc_list = []
    cpl_list = []
    global personnel

    week_start, week_end = get_week_range(datetime.today() + timedelta(days=-3))
    print("weekstart:"+str(week_start)+" week-end:"+str(week_end))
    for person in personnel:
        if week_start <= person.PFC_Promo_date <= week_end and \
                (person.status == "Active" or person.status == "Military ELOA") and person.paygrade != "E-3 PFC":
            print("PFC Promotion due: " + str(person.paygrade) + " " + str(person.firstname) + " "
                  + str(person.lastname) + " dated: " + str(person.PFC_Promo_date.strftime("%d %b %Y")).upper())
            pfc_list.append(person)
        elif week_start <= person.SPC_Promo_date <= week_end and \
                (person.status == "Active" or person.status == "Military ELOA") and person.paygrade != "E-4A SPC":
            print("SPC Promotion due: " + str(person.paygrade) + " " + str(person.firstname) + " "
                  + str(person.lastname) + " dated: " + str(person.SPC_Promo_date.strftime("%d %b %Y")).upper())
            spc_list.append(person)
        elif person.CPL_Promo_date <= week_end and \
                (person.status == "Active" or person.status == "Military ELOA") \
                and person.paygrade == "E-4A SPC" and person.NCOA is True and person.SAC is True:
            print("CPL Promotion due? " + str(person.paygrade) + " " + str(person.firstname) + " "
                  + str(person.lastname) + " dated: " + str(person.CPL_Promo_date.strftime("%d %b %Y")).upper()
                  + "NCOA/SAC:" + str(person.NCOA) + "/" + str(person.SAC))
            cpl_list.append(person)


def gc_finder():
    global personnel
    gc_list = []
    bk1_list = []
    bk2_list = []
    bk3_list = []

    sk1_list = []
    sk2_list = []
    sk3_list = []

    gk1_list = []
    gk2_list = []
    gk3_list = []

    day_start, day_end = get_month_range(datetime.today())
    for person in personnel:
        paygrade2rank(person)
        if day_start <= person.gc <= day_end and (person.status == "Active" or person.status == "Military ELOA"):
            gc_list.append(person)
        elif day_start <= person.gc_bk1 <= day_end and (person.status == "Active" or person.status == "Military ELOA"):
            bk1_list.append(person)
        elif day_start <= person.gc_bk2 <= day_end and (person.status == "Active" or person.status == "Military ELOA"):
            bk2_list.append(person)
        elif day_start <= person.gc_bk3 <= day_end and (person.status == "Active" or person.status == "Military ELOA"):
            bk3_list.append(person)
        elif day_start <= person.gc_sk1 <= day_end and (person.status == "Active" or person.status == "Military ELOA"):
            sk1_list.append(person)
        elif day_start <= person.gc_sk2 <= day_end and (person.status == "Active" or person.status == "Military ELOA"):
            sk2_list.append(person)
        elif day_start <= person.gc_sk3 <= day_end and (person.status == "Active" or person.status == "Military ELOA"):
            sk3_list.append(person)
        elif day_start <= person.gc_gk1 <= day_end and (person.status == "Active" or person.status == "Military ELOA"):
            gk1_list.append(person)
        elif day_start <= person.gc_gk2 <= day_end and (person.status == "Active" or person.status == "Military ELOA"):
            gk2_list.append(person)
        elif day_start <= person.gc_gk3 <= day_end and (person.status == "Active" or person.status == "Military ELOA"):
            gk3_list.append(person)

    gc_list.sort(key=lambda x: (x.AOR, x.gc), reverse=False)

    bk1_list.sort(key=lambda x: (x.AOR, x.gc_bk1), reverse=False)
    bk2_list.sort(key=lambda x: (x.AOR, x.gc_bk2), reverse=False)
    bk3_list.sort(key=lambda x: (x.AOR, x.gc_bk3), reverse=False)

    sk1_list.sort(key=lambda x: (x.AOR, x.gc_sk1), reverse=False)
    sk2_list.sort(key=lambda x: (x.AOR, x.gc_sk2), reverse=False)
    sk3_list.sort(key=lambda x: (x.AOR, x.gc_sk3), reverse=False)

    gk1_list.sort(key=lambda x: (x.AOR, x.gc_gk1), reverse=False)
    gk2_list.sort(key=lambda x: (x.AOR, x.gc_gk2), reverse=False)
    gk3_list.sort(key=lambda x: (x.AOR, x.gc_gk3), reverse=False)

    print("[CENTER][B] The following are awarded the Good Conduct Medal[/B]\n\n")

    if gc_list:
        print("[IMG]https://7cav.us/data/pixelexit/rosters/awards/0/24.jpg[/IMG]")
        print("[B]First Award for 1 Year of Service[/B]\n")
        for person in gc_list:
            index = gc_list.index(person)
            if gc_list.__len__() == 1:
                print(person.AOR)
            elif gc_list[index].AOR != gc_list[index-1].AOR:
                print(person.AOR)
            print("[URL='{0}']{1} {2} {3}[/URL] {4}".format(person.milpaclink, person.rank, person.firstname,
                                                            person.lastname, person.gc_bk1.strftime("%d %b %Y").upper()))
# ---------------------------------------------------------------------------------------------------------------------
    if bk1_list:
        print("\n\n[IMG]https://wiki.7cav.us/images/8/87/GCM1BZ.png[/IMG]\n")
        print("[B]1st Bronze Knot for 2 Years of Service[/B]\n")
        for person in bk1_list:
            index = bk1_list.index(person)
            if bk1_list.__len__() == 1:
                print(person.AOR)
            elif bk1_list[index].AOR != bk1_list[index-1].AOR:
                print(person.AOR)
            print("[URL='{0}']{1} {2} {3}[/URL] {4}".format(person.milpaclink, person.rank, person.firstname,
                                                            person.lastname, person.gc_bk1.strftime("%d %b %Y").upper()))
# ---------------------------------------------------------------------------------------------------------------------
    if bk2_list:
        print("\n\n[IMG]https://wiki.7cav.us/images/6/60/GCM2BZ.png[/IMG]\n")
        print("[B]2nd Bronze Knot for 3 Years of Service[/B]\n")
        for person in bk2_list:
            index = bk2_list.index(person)
            if bk2_list.__len__() == 1:
                print(person.AOR)
            elif bk2_list[index].AOR != bk2_list[index-1].AOR:
                print(person.AOR)
            print("[URL='{0}']{1} {2} {3}[/URL] {4}".format(person.milpaclink, person.rank, person.firstname,
                                                            person.lastname, person.gc_bk2.strftime("%d %b %Y").upper()))
# ---------------------------------------------------------------------------------------------------------------------
    if bk3_list:
        print("\n\n[IMG]https://wiki.7cav.us/images/a/ae/GCM3BZ.png[/IMG]\n")
        print("[B]3rd Bronze Knot for 4 Years of Service[/B]\n")
        for person in bk3_list:
            index = bk3_list.index(person)
            if bk3_list.__len__() == 1:
                print(person.AOR)
            elif bk3_list[index].AOR != bk3_list[index - 1].AOR:
                print(person.AOR)
            print("[URL='{0}']{1} {2} {3}[/URL] {4}".format(person.milpaclink, person.rank, person.firstname,
                                                                person.lastname, person.gc_bk3.strftime("%d %b %Y").upper()))
# ---------------------------------------------------------------------------------------------------------------------
    if sk1_list:
        print("\n\n[IMG]https://wiki.7cav.us/index.php/File:GCM1S.png[/IMG]\n")
        print("[B]1st Silver Knot for 5 Years of Service[/B]\n")
        for person in sk1_list:
            index = sk1_list.index(person)
            if sk1_list.__len__() == 1:
                print(person.AOR)
            elif sk1_list[index].AOR != sk1_list[index - 1].AOR:
                print(person.AOR)
            print("[URL='{0}']{1} {2} {3}[/URL] {4}".format(person.milpaclink, person.rank, person.firstname,
                                                            person.lastname, person.gc_sk1.strftime("%d %b %Y").upper()))
# ---------------------------------------------------------------------------------------------------------------------
    if sk2_list:
        print("\n\n[IMG]https://wiki.7cav.us/images/5/57/GCM2S.png[/IMG]\n")
        print("[B]2nd Silver Knot for 6 Years of Service[/B]\n")
        for person in sk2_list:
            index = sk2_list.index(person)
            if sk2_list.__len__() == 1:
                print(person.AOR)
            elif sk2_list[index].AOR != sk2_list[index - 1].AOR:
                print(person.AOR)
            print("[URL='{0}']{1} {2} {3}[/URL] {4}".format(person.milpaclink, person.rank, person.firstname,
                                                            person.lastname, person.gc_sk2.strftime("%d %b %Y").upper()))
# ---------------------------------------------------------------------------------------------------------------------
    if sk3_list:
        print("\n\n[IMG]https://wiki.7cav.us/images/9/97/GCM3S.png[/IMG]\n")
        print("[B]3rd Silver Knot for 7 Years of Service[/B]\n")
        for person in sk3_list:
            index = sk3_list.index(person)
            if sk3_list.__len__() == 1:
                print(person.AOR)
            elif sk3_list[index].AOR != sk3_list[index - 1].AOR:
                    print(person.AOR)
            print("[URL='{0}']{1} {2} {3}[/URL] {4}".format(person.milpaclink, person.rank, person.firstname,
                                                            person.lastname, person.gc_sk3.strftime("%d %b %Y").upper()))
# ---------------------------------------------------------------------------------------------------------------------
    if gk1_list:
        print("\n\n[IMG]https://wiki.7cav.us/images/f/fa/GCM1G.png[/IMG]\n")
        print("[B]1st Gold Knot for 8 Years of Service[/B]\n")
        for person in gk1_list:
            index = gk1_list.index(person)
            if gk1_list.__len__() == 1:
                print(person.AOR)
            elif gk1_list[index].AOR != gk1_list[index - 1].AOR:
                    print(person.AOR)
            print("[URL='{0}']{1} {2} {3}[/URL] {4}".format(person.milpaclink, person.rank, person.firstname,
                                                            person.lastname, person.gc_gk1.strftime("%d %b %Y").upper()))
# ---------------------------------------------------------------------------------------------------------------------
    if gk2_list:
        print("\n\n[IMG]https://wiki.7cav.us/images/1/1b/GCM2G.png[/IMG]\n")
        print("[B]2nd Gold Knot for 9 Years of Service[/B]\n")
        for person in gk2_list:
            index = gk2_list.index(person)
            if gk2_list.__len__() == 1:
                print(person.AOR)
            elif gk2_list[index].AOR != gk2_list[index - 1].AOR:
                print(person.AOR)
            print("[URL='{0}']{1} {2} {3}[/URL] {4}".format(person.milpaclink, person.rank, person.firstname,
                                                            person.lastname, person.gc_gk2.strftime("%d %b %Y").upper()))
# ---------------------------------------------------------------------------------------------------------------------
    if gk3_list:
        print("\n\n[IMG]https://wiki.7cav.us/images/7/75/GCM3G.png[/IMG]\n")
        print("[B]3rd Gold Knot for 10 Years of Service[/B]\n")
        for person in gk3_list:
            index = gk3_list.index(person)
            if gk3_list.__len__() == 1:
                print(person.AOR)
            elif gk3_list[index].AOR != gk3_list[index - 1].AOR:
                print(person.AOR)
            print("[URL='{0}']{1} {2} {3}[/URL] {4}".format(person.milpaclink, person.rank, person.firstname,
                                                            person.lastname, person.gc_gk3.strftime("%d %b %Y").upper()))


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
    # Find the first day of the week:
    if dow == 6:  # Since we want to start with Saturday, if the input is saturday we are good
        start_date = date
    else:
        # Otherwise, subtract `dow` number days to get the sunday (=7) and add 1 to get the saturday
        start_date = date - timedelta(dow+1)
    # Now, add 6 for the last day of the week (i.e., count up to Friday)
    end_date = start_date + timedelta(6)
    return start_date.replace(hour=0, minute=0, second=0), end_date.replace(hour=23, minute=59, second=59)


def get_month_range(date):
    first_day = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    print("first day = " + str(first_day))
    if date.month == 12 and date.year == datetime.today().year:
        last_day = date.replace(day=31, hour=23, minute=59, second=59, microsecond=999999)
        print("last day = " + str(last_day))
        return first_day, last_day
    elif date.year == datetime.today().year:
        last_day1 = date.replace(month=date.month+1, day=1) - timedelta(days=1)
        last_day = last_day1.replace(hour=23, minute=59, second=59, microsecond=999999)
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
    promo_finder()
    #print("-----\n Good Conduct Medals:\n----\n")
    #gc_finder()

