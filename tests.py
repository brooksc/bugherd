import random
import unittest
from bugherd import BugHerd
import random
from pprint import pprint

ORGANIZATION_ID = 31542

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        api_key = 'nvbawbf8hwyzacvrimio1a'
        # debug = True
        debug = False
        self.bh = BugHerd(api_key, debug)


    def test_a_testOrganization(self):
    # def test_organization(self):
    #     print "test_a_testOrganization"
        # organization
        results = self.bh.organization()
        assert(results['organization']['id'] == ORGANIZATION_ID)
        # pprint(results)

    # record the number of projects before create project is run
    # def test_a_recordProjectList(self):
    #     # print "test_a_recordProjectList"
    #     self.__class__.project_list = self.bh.project().list()
    #     # print len(self.__class__.project_list)
    #     self.__class__.project_list_active = self.bh.project().list_active()
    #     # print len(self.__class__.project_list_active)

    # create a project we'll use for tests
    def test_b_createProject(self):
    # def test_createProject(self):
        # Create a Project
        # print "test_b_createProject"
        number = random.randint(1,99999999)
        name = "Project %s" % number
        self.__class__.name = name
        devurl = "%s.brooksc.com" % number
        self.__class__.devurl = devurl
        # print "Creating '%s'" % name
        results = self.bh.project().create(name, devurl)
        self.__class__.project_id = results['project']['id']

    # Check that one more projects exists now than before
    # def test_c_checkProjectList(self):
    #     # print "test_c_checkProjectList"
    #     self.__class__.project_list2 = self.bh.project().list()
    #     # print len(self.__class__.project_list2)
    #     self.__class__.project_list_active2 = self.bh.project().list_active()
    #     # print len(self.__class__.project_list_active2)
    #     project_list = self.__class__.project_list['projects']
    #     project_list_active = self.__class__.project_list_active['projects']
    #     project_list2 = self.__class__.project_list2['projects']
    #     project_list_active2 = self.__class__.project_list_active2['projects']
    #     assert(len(project_list)+1 == len(project_list2))
    #     assert(len(project_list_active)+1 == len(project_list_active2))

    # Check if project details are the same as created
    # def test_d_projectDetails(self):
    #     results = self.bh.project(self.__class__.project_id).details()
    #     assert(results['project']['name'] == self.__class__.name)
    #     assert(results['project']['devurl'] == self.__class__.devurl)


    # Project:
    # add_member
    # add_guest
    # update

    # TODO: not working
    # def test_e_add_guest(self):
    #     results = self.bh.project(self.__class__.project_id).add_guest('bugherd@brooksc.com')
    #     pprint(results)

    # Task:
    # task = bh.project(123).Task()
    # task.create(description, requester_id, assigned_to_id, status, priority, tags)

    def test_f_listTasks(self):
        self.__class__.task_list = self.bh.project(self.__class__.project_id).task().list()

    def test_g_createTask(self):
        task_description = "This is a test task"
        self.__class__.task_description = task_description
        results = self.bh.project(self.__class__.project_id).task().create(task_description)
        # pprint(results)
        self.__class__.task_id = results['task']['id']
        assert(self.task_id == self.bh.project(self.__class__.project_id).task(self.__class__.task_id).id)

    def test_h_taskDescription(self):
        results = self.bh.project(self.__class__.project_id).task(self.__class__.task_id).detail()
        assert(results['task']['description'] == self.__class__.task_description)
        # pprint(results)


    def test_h_listTasks2(self):
        self.__class__.task_list2 = self.bh.project(self.__class__.project_id).task().list()
        len_task_list = len(self.__class__.task_list['tasks'])
        len_task_list2 = len(self.__class__.task_list2['tasks'])
        assert(len_task_list+1 == len_task_list2)

    # TODO: task.update()

    def test_z_deleteProject(self):
    # def tearDown(self):
        self.bh.project(self.__class__.project_id).delete()


    # def test_shuffle(self):
    #     # make sure the shuffled sequence does not lose any elements
    #     random.shuffle(self.seq)
    #     self.seq.sort()
    #     self.assertEqual(self.seq, range(10))
    #
    #     # should raise an exception for an immutable sequence
    #     self.assertRaises(TypeError, random.shuffle, (1,2,3))
    #
    # def test_choice(self):
    #     element = random.choice(self.seq)
    #     self.assertTrue(element in self.seq)
    #
    # def test_sample(self):
    #     with self.assertRaises(ValueError):
    #         random.sample(self.seq, 20)
    #     for element in random.sample(self.seq, 5):
    #         self.assertTrue(element in self.seq)

if __name__ == '__main__':
    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)