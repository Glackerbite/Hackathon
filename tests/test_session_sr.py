import os
import shutil
import unittest

from session import Session


class TestSessionSR(unittest.TestCase):
    def setUp(self):
        # create a clean test area
        self.date = '010125'
        self.time = '0900'
        self.type = 'physics'
        self.sdir = os.path.join('sessions', self.date)
        self.rdir = 'sessionRequests'
        shutil.rmtree(self.sdir, ignore_errors=True)
        os.makedirs(self.sdir, exist_ok=True)
        # ensure requests dir exists
        os.makedirs(self.rdir, exist_ok=True)

        # create a session file with expected keys
        self.session_file = os.path.join('sessions', self.date, 'M0900')
        with open(self.session_file, 'w') as f:
            f.write('time end:1000\n')
            f.write('session type:physics\n')
            f.write('teacher Supervisor:Alice\n')
            f.write('equipment:Microscope\n')
            f.write('places:2\n')
            f.write('students:john,doe\n')
            f.write('waitlist:mary\n')

        # create a request file
        self.request_file = os.path.join('sessionRequests', '010125M0900')
        with open(self.request_file, 'w') as f:
            f.write('requestees:bob\n')
            f.write('time end:1000\n')
            f.write('session type:physics\n')
            f.write('teacher Supervisor:Carol\n')

        self.session = Session(self.date, self.time, self.type)

    def tearDown(self):
        shutil.rmtree(os.path.join('sessions'), ignore_errors=True)
        shutil.rmtree(os.path.join('sessionRequests'), ignore_errors=True)

    def test_SRGet_session_students(self):
        students = self.session.SRGet('session', 'students')
        self.assertEqual(students, ['john', 'doe'])

    def test_SRChange_replace_add_remove_students(self):
        # replace students with 'alice'
        self.session.SRChange('session', 'students', 'alice')
        self.assertEqual(self.session.SRGet('session', 'students'), ['alice'])

        # add bob
        self.session.SRChange('session', 'students', 'bob', add=True)
        self.assertEqual(self.session.SRGet('session', 'students'), ['alice', 'bob'])

        # remove alice
        self.session.SRChange('session', 'students', 'alice', remove=True)
        self.assertEqual(self.session.SRGet('session', 'students'), ['bob'])

    def test_request_SRGet_and_SRChange(self):
        # SRGet for request
        reqs = self.session.SRGet('request', 'requestees')
        self.assertEqual(reqs, ['bob'])

        # change teacher Supervisor
        self.session.SRChange('request', 'teacher Supervisor', 'David')
        self.assertEqual(self.session.SRGet('request', 'teacher Supervisor'), ['David'])

    def test_addToWaitlist_server_flow(self):
        # simulate a server flow where addToWaitlist decides between students and waitlist
        # create a fresh session file with 2 places and no students
        s2_date = '020125'
        s2_time = '1000'
        s2_id = 'M1000'
        os.makedirs(os.path.join('sessions', s2_date), exist_ok=True)
        s2_file = os.path.join('sessions', s2_date, s2_id)
        with open(s2_file, 'w') as f:
            f.write('time end:1100\n')
            f.write('session type:physics\n')
            f.write('teacher Supervisor:Alice\n')
            f.write('equipment:None\n')
            f.write('places:2\n')
            f.write('students:\n')
            f.write('waitlist:\n')

        s2 = Session(s2_date, s2_time, 'physics')
        # add first student -> should go to students
        import updates
        updates.addToWaitlist(s2, 'charlie')
        self.assertIn('charlie', s2.SRGet('session', 'students'))

        # fill the session (add another student)
        updates.addToWaitlist(s2, 'dan')
        self.assertIn('dan', s2.SRGet('session', 'students'))

        # now session is full; next join goes to waitlist
        updates.addToWaitlist(s2, 'erin')
        self.assertIn('erin', s2.SRGet('session', 'waitlist'))

    def test_denysession_teacher_removal_and_request_deletion(self):
        # Create a session and corresponding request file, then simulate denysession flow
        d_date = '030125'
        d_time = '1100'
        d_id = 'M1100'
        os.makedirs(os.path.join('sessions', d_date), exist_ok=True)
        sfile = os.path.join('sessions', d_date, d_id)
        rfile = os.path.join('sessionRequests', f'{d_date}{d_id}')
        with open(sfile, 'w') as f:
            f.write('time end:1200\n')
            f.write('session type:physics\n')
            f.write('teacher Supervisor:Zoe\n')
            f.write('equipment:None\n')
            f.write('places:2\n')
            f.write('students:\n')
            f.write('waitlist:\n')
        # create a request file that should be deleted when no teachers left
        with open(rfile, 'w') as f:
            f.write('requestees:someone\n')

        s3 = Session(d_date, d_time, 'physics')
        # remove the only teacher
        s3.SRChange('session', 'teacher Supervisor', 'Zoe', remove=True)
        # teacher list should be empty
        self.assertEqual(s3.SRGet('session', 'teacher Supervisor'), [])
        # deleting request file as server does
        # emulate server's denysession which deletes the request file when no teachers
        if s3.SRGet('session', 'teacher Supervisor') == []:
            s3.delete(type='request')
        self.assertFalse(os.path.exists(rfile))


if __name__ == '__main__':
    unittest.main()
