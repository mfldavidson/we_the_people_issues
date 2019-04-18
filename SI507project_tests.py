import sqlite3, unittest
from si507project import *

class FinalProjDBTests(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect("petitions.db")
        self.cur = self.conn.cursor()

    def testPetitionsTable(self):
        self.cur.execute("select * from petitions where id = 2722358")
        data = self.cur.fetchone()
        self.assertEqual(data,(2722358, "Remove Chuck Schumer and Nancy Pelosi from office", "Schumer and Pelosi's hatred and refusing to work with President Donald J. Trump is holding America hostage. We the people know securing our southern border is a priority which will not happen with these two in office. Lets build the wall NOW!", 149, 99851, "https://petitions.whitehouse.gov/petition/remove-chuck-schumer-and-nancy-pelosi-office", '2019-02-08 11:07:44.000000', 'closed', None, '2019-01-09 11:07:44.000000', False, False), "Testing data that results from selecting petition 2722358")

    def testIssuesTable(self):
        self.cur.execute("select id, name from issues where id = 326")
        data = self.cur.fetchone()
        self.assertEqual(data,(326, 'Homeland Security & Defense'), "Testing data that results from selecting issue 326")

    def testTypesTable(self):
        self.cur.execute("select id, name from types where id = 291")
        data = self.cur.fetchone()
        self.assertEqual(data,(291, "Call on Congress to act on an issue"), "Testing data that results from selecting type 291")

    def testIssuePetitionRelTable(self):
        self.cur.execute("select petition_id, issue_id from issuepetitionassociation where petition_id = 2722358 and issue_id = 326")
        data = self.cur.fetchone()
        self.assertEqual(data,(2722358, 326), "Testing data that results from selecting the relationship between petition 2722358 and issue 326")

    def testTypePetitionRelTable(self):
        self.cur.execute("select petition_id, type_id from typepetitionassociation where petition_id = 2722358 and type_id = 291")
        data = self.cur.fetchone()
        self.assertEqual(data,(2722358, 291), "Testing data that results from selecting the relationship between petition 2722358 and type 291")

    def testGetPetitionsByIssueFunction(self):
        petitions = getPetitionsByIssue(301)
        self.assertEqual(len(petitions),39, "Testing that getPetitionsByIssue function returns 39 results when querying by issue 301")

    def testSplitPetitionsBySignableFunctionOpen(self):
        petitions = getPetitionsByIssue(301)
        open_petitions, closed_petitions = splitPetitionsBySignable(petitions)
        self.assertEqual(len(open_petitions),0, "Testing that splitPetitionsBySignable function returns 0 results when splitting the 39 petitions with issue 301")

    def testSplitPetitionsBySignableFunctionClosed(self):
        petitions = getPetitionsByIssue(301)
        open_petitions, closed_petitions = splitPetitionsBySignable(petitions)
        self.assertEqual(len(closed_petitions),39, "Testing that splitPetitionsBySignable function returns 39 results when querying by issue 301")

    def tearDown(self):
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)
