__author__ = 'brooksc'

from pprint import pprint
import requests
import json, time
from requests.auth import HTTPBasicAuth
# import sys
import collections

API_BASE_URL = 'http://www.bugherd.com/api_v2/{api}'


class Error(Exception):
    pass


class Response(object):
    def __init__(self, body):
        self.raw = body
        self.body = json.loads(body)
        # self.successful = self.body['ok']
        # self.error = self.body.get('error')


class BaseAPI(object):
    def __init__(self, token=None):
        self.token = token

    def _request(self, method, api, **kwargs):
        # if self.token:
        # kwargs.setdefault('params', {})['token'] = self.token

        response = method(API_BASE_URL.format(api=api), auth=HTTPBasicAuth(self.api_key, 'x'),
                          **kwargs)

        assert response.status_code == 200

        response = Response(response.text)
        # if not response.successful:
        #     raise Error(response.error)
        # return response
        return response.body

    def get(self, api, **kwargs):
        return self._request(requests.get, api, **kwargs)

    def post(self, api, **kwargs):
        return self._request(requests.post, api, **kwargs)


# Usage Examples
# bh = BugHerd(api_key)
# bh = BugHerd(api_key, True) # enable debugging
# bh.organization()
# bh.projects()
# bh.projects_active()
# bh.users()
# bh.members()
# bh.guests()
class BugHerd(BaseAPI):
    def __init__(self, api_key, debug=False):
        # self.api_key = 'sqpauk9fi9fk1qcvv0svdg'
        self.api_key = api_key
        self.url = API_BASE_URL
        # self.url = 'https://www.bugherd.com/api_v2'
        self.proxies = {
            # "http": "http://localhost:8080",
            # "https": "http://localhost:8080",
        }
        self.debug = debug


    def project(self, project_id):
        return Project(self.api_key, project_id, self.debug)

    # Get more detail of your account.
    #

    # GET /api_v2/organization.json
    def organization(self):
        return self.get('organization.json')

    # Get a list of all projects within your account.
    #

    # GET /api_v2/projects.json
    def projects(self):
        return self.get('projects.json')

    # GET /api_v2/projects/active.json
    def projects_active(self):
        return self.get('projects/active.json')

    # See all the people in your account.
    #

    # GET /api_v2/users.json
    def users(self):
        return self.get('users.json')

    # GET /api_v2/users/members.json
    def members(self):
        return self.get('users/members.json')

    # GET /api_v2/users/guests.json
    def guests(self):
        return self.get('users/guests.json')

# bh = BugHerd(api_key)
# project = bh.Project()
# project.list()
# project = bh.Project(123)
# project.id # 123
# project.show()
# project.update??
class Project(BaseAPI):
    def __init__(self, api_key, project_id, debug=False):
        self.api_key = api_key
        self.project_id = project_id
        self.id = project_id

    # Show details for a specific project. Note: if you'd like to see the tasks in the project, refer to section 'List tasks'.
    #
    # GET /api_v2/projects/#{project_id}.json
    def details(self):
        return self.get('projects/%s.json' % self.project_id)



    # List details of a task in a given project, includes all data including comments, attachments, etc.
    #
    # GET /api_v2/projects/#{project_id}/tasks/#{task_id}.json
    def task(self, task_id):
        return Task(self.api_key, self.project_id, self.task_id, self.debug)


    # Create a new project. The project will initially have no members.
    #
    # POST /api_v2/projects.json
    #
    # Example request data:
    #
    # {"project":{
    # "name":"My Website",
    #   "devurl":"http://www.example.com",
    #   "is_active":true,
    #   "is_public":false
    # }}
    def create(self, name, devurl, is_active=None, is_public=None):
        # TODO: implement
        pass

    # Add a member to a project.
    #
    # POST /api_v2/projects/#{project_id}/add_member.json
    #
    # Request data:
    #
    # {"user_id":123}
    def add_member(self, user_id):
        # TODO: implement
        pass

    # Add an existing guest to a project, or invite someone by email address.
    #
    # POST /api_v2/projects/#{project_id}/add_guest.json
    #
    # Request data:
    #
    # {"user_id":123}
    # {"email":"someone@example.com"}
    def add_guest(self, user_id, email):
        # TODO: implement
        pass

    # Update settings for an existing project under your control (ie: only the ones you own).
    #
    # PUT /api_v2/projects/#{project_id}.json
    #
    # Example request data:
    #
    # {"project":{
    #   "is_public":true
    # }}
    def update(self, is_public=None):
        # TODO: implement
        pass

    # Delete a project and all associated data. Use with care, deleted projects cannot be recovered.
    #
    # DELETE /api_v2/projects/#{project_id}.json
    def delete(self):
        # TODO: implement
        pass


# task = bh.project(123).Task()
# task.create(description, requester_id, assigned_to_id, status, priority, tags)
# task.list()
# task = bh.project(123).Task(123)
# task.id
# task.update??
# task.show()

class Task(BaseAPI):
    def __init__(self, api_key, project_id, task_id, debug=False):
        self.api_key = api_key
        self.project_id = project_id
        self.id = task_id
        self.task_id = task_id

    # Get a full list of tasks for a project, including archived tasks.
    #
    # GET /api_v2/projects/#{project_id}/tasks.json
    #
    #
    # You can filter tasks using the following GET parameters: updated_since, created_since, status, priority, tag, assigned_to_id and external_id. Examples on how to use filters are below:
    def list(self):
        # TODO: implement filter
        return self.get("projects/%s/tasks.json" % (self.url, self.project_id))

    def show(self):
        url = "%s/projects/%s/tasks/%s.json" % (self.url, self.project_id, self.task_id)
        return self._get(url)

    # POST /api_v2/projects/#{project_id}/tasks.json
    #
    # Example request data:
    #
    # {"task":{
    # "description":"Example task",
    #   "priority":"normal",
    #   "status":"backlog",
    #   "requester_id":123,
    #   "tag_names":["ui","feature"],
    #   "assigned_to_id":123,
    #   "external_id":"ABC123"
    # }}
    # or:
    #
    # {"task":{
    #   "description":"Example task",
    #   "requester_email":"user@example.com",
    #   "assigned_to_email":"someone@company.com",
    # }}
    # "requester_email" can be any email address while "assigned_to_email" needs to be of a current project member.
    #
    # Values for "priority" are not set, critical, important, normal, and minor.
    #
    # Values for "status" are backlog, todo, doing, done, and closed. Omit this field or set as "null" to send tasks to the Feedback panel.
    #
    # External ID is an API-only field. It cannot be set from the BugHerd application, only using the API. An external ID can be used to track originating IDs from other systems in BugHerd bugs.
    def create(self, description=None, requester_id=None, assigned_to_id=None, status=None, priority=None, tags=None):
        if not description or not requester_id:
            raise Exception
        url = "%s/projects/%s/tasks.json" % (self.url, self.project_id)
        tree = lambda: collections.defaultdict(tree)
        data = tree()
        data['task']['description'] = description
        data['task']['requester_id'] = requester_id
        if assigned_to_id:
            data['task']['assigned_to_id'] = assigned_to_id
        if tags:
            data['task']['tag_names'] = tags
        if status:
            data['task']['status'] = status
        if priority:
            data['task']['priority'] = priority
        # data['task']['external_id'] = "testing"

        return self._post(url, data)

    # Update one of the tasks in a project.
    #
    # PUT /api_v2/projects/#{project_id}/tasks/#{task_id}.json
    #
    # Request data:
    #
    # {"task":{
    #   "priority":"normal",
    #   "status":"backlog",
    #   "assigned_to_id":123,
    # }}
    #
    # If you'd like the update to happen on behalf of a specific user in the project (note that those user's permissions do not apply when making an update via the API, this is only for audit logging purposes)
    #
    # {"task":{
    #   "status":"todo",
    #   "updater_email":"someone@company.com",
    # }}
    # Below are examples for unsettings values (only allowed for status and assigned_to_id)
    #
    # Unassigning a task:
    #
    # {"task":{"assigned_to_id":null}}
    # Moving a task back to feedback:
    #
    # {"task":{"status_id":null}}
    def update(self):
        pass

# attachments = bh.Project(123).Task(456).attachments
# attachments.list()
# attachments(123).show()
# attachments().create()
# attachments(123).delete()
# TODO: implement
# class Attachments(BaseAPI):
# List attachments
#
# Get a paginated list of attachments for a task.
#
# GET /api_v2/projects/#{project_id}/tasks/#{task_id}/attachments.json
#
#
# Show attachment
#
# Get detail for specific attachment.
#
# GET /api_v2/projects/#{project_id}/tasks/#{task_id}/attachments/#{id}.json
#
#
# Create attachment
#
# Adds a new attachment to the specified task using an existing URL.
#
# POST /api_v2/projects/#{project_id}/tasks/#{task_id}/attachments.json
# Request data:
#
# {"comment":{
# "file_name":"resolution.gif",
#   "url":"http://i.imgur.com/U9h3jZI.gif"
# }}
#
# Upload attachment
#
# Upload a new attachment and add it to the specified task. The file contents need to be specified as the POST data on this request.
#
# Note that your upload needs to be reasonable in size as the maximum time the request may take is around 30 seconds. If you have larger uploads please create arrange your own file upload and create the attachment from a URL instead.
#
# POST /api_v2/projects/#{project_id}/tasks/#{task_id}/attachments/upload
# Note in the sample below please specify an existing file name.
#
#
# Delete attachment
#
# Delete an attachment from a task. Note that this action is permanent and cannot be undone.
#
# DELETE /api_v2/projects/#{project_id}/tasks/#{task_id}/attachments/#{id}.json
#

class Comments(BaseAPI):
    pass
    # Get a paginated list of comments for a task.
    #
    # GET /api_v2/projects/#{project_id}/tasks/#{task_id}/comments.json

    def list_comments(self):
        pass


    # Adds a new comment to the specified task.
    #
    # POST /api_v2/projects/#{project_id}/tasks/#{task_id}/comments.json
    # Request data:
    #
    # {"comment":{
    #   "text":"comment here",
    #   "user_id":123
    # }}
    # or:
    #
    # {"comment":{
    #   "text":"comment here",
    #   "email":"user@example.com"
    # }}

    def create_comment(self, project_id, task_id, comment, user_id):
        if not project_id or not task_id or not comment or not user_id:
            raise Exception
        url = "%s/projects/%s/tasks/%s/comments.json" % (self.url, project_id, task_id)
        tree = lambda: collections.defaultdict(tree)
        data = tree()
        data['comment']['text'] = comment
        data['comment']['user_id'] = user_id
        return self._post(url, data)


class Webhook(BaseAPI):
    def list_webhooks(self):
        return self.get('webhooks.json')

    def create_webhook(self, target_url, event, project_id=None):
        url = "%s/webhooks.json" % (self.url)
        tree = lambda: collections.defaultdict(tree)
        data = tree()
        if project_id:
            data['project_id'] = project_id
        data['target_url'] = target_url
        data['event'] = event
        return self._post(url, data)

    def delete_webhooks(self, webhook_id):
        url = "%s/webhooks/%s.json" % (self.url, webhook_id)
        return self._delete(url)

    def list_comments(self, project_id, task_id):
        url = "%s/projects/%s/tasks/%s/comments.json" % (self.url, project_id, task_id)
        return self._get(url)


def main():
    bh = BugHerd('sqpauk9fi9fk1qcvv0svdg', True)
    # bh.list_webhooks()
    # bh.delete_webhooks(3814)
    project_id = 56250
    # users = bh.list_users()
    projects = bh.projects()
    project_id = projects['projects'][0]['id']
    # for project in projects['projects']:
    #     print "%s:%s" % (project['id'], project['name'])
    # pass
    print project_id
    # project = bh.project(project_id)
    # pprint(project.details())
    pprint(bh.project(project_id).details())

    # bh.list_comments(project_id, 1687761)
    # results = bh.list_tasks(project_id)
    # print len(results['tasks'])


if __name__ == "__main__":
    main()