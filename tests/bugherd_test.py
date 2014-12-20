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
        # print "test_a_testOrganization"
        results = self.bh.organization()
        assert(results.body['organization']['id'] == ORGANIZATION_ID)

    # record the number of projects before create project is run
    def test_a_recordProjectList(self):
        # print "test_a_recordProjectList"
        self.__class__.project_list = self.bh.project().list()
        self.__class__.project_list_active = self.bh.project().list_active()

    # create a project we'll use for tests
    def test_b_createProject(self):
        # print "test_b_createProject"
        number = random.randint(1,99999999)
        name = "Project %s" % number
        self.__class__.name = name
        devurl = "%s.brooksc.com" % number
        self.__class__.devurl = devurl
        # print "Creating '%s'" % name
        results = self.bh.project().create(name, devurl)
        self.__class__.project_id = results.body['project']['id']

    # Check that one more projects exists now than before
    def test_c_checkProjectList(self):
        # print "test_c_checkProjectList"
        self.__class__.project_list2 = self.bh.project().list()
        self.__class__.project_list_active2 = self.bh.project().list_active()
        project_list = self.__class__.project_list.body['projects']
        project_list_active = self.__class__.project_list_active.body['projects']
        project_list2 = self.__class__.project_list2.body['projects']
        project_list_active2 = self.__class__.project_list_active2.body['projects']
        assert(len(project_list)+1 == len(project_list2))
        assert(len(project_list_active)+1 == len(project_list_active2))

    # Check if project details are the same as created
    def test_d_projectDetails(self):
        # print "test_d_projectDetails"
        results = self.bh.project(self.__class__.project_id).details()
        assert(results.body['project']['name'] == self.__class__.name)
        assert(results.body['project']['devurl'] == self.__class__.devurl)


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
        # print "test_f_listTasks"
        self.__class__.task_list = self.bh.project(self.__class__.project_id).task().list()

    def test_g_createTask(self):
        # print "test_g_createTask"
        task_description = "This is a test task"
        self.__class__.task_description = task_description
        results = self.bh.project(self.__class__.project_id).task().create(task_description)
        # pprint(results)
        self.__class__.task_id = results.body['task']['id']
        assert(self.task_id == self.bh.project(self.__class__.project_id).task(self.__class__.task_id).id)

    def test_h_taskDescription(self):
        # print "test_h_taskDescription"
        results = self.bh.project(self.__class__.project_id).task(self.__class__.task_id).detail()
        assert(results.body['task']['description'] == self.__class__.task_description)
        # pprint(results)


    def test_h_listTasks2(self):
        # print "test_h_listTasks2"
        self.__class__.task_list2 = self.bh.project(self.__class__.project_id).task().list()
        len_task_list = len(self.__class__.task_list.body['tasks'])
        len_task_list2 = len(self.__class__.task_list2.body['tasks'])
        assert(len_task_list+1 == len_task_list2)

    # TODO: task.update()

    def test_z_deleteProject(self):
        # print "test_z_deleteProject"
    # def tearDown(self):
        self.bh.project(self.__class__.project_id).delete()


if __name__ == '__main__':
    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=9).run(suite)