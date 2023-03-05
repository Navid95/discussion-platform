from flask import Response
from main.models import User, Topic, Post
from extensions import db
import json as j


"""
Account view tests
"""


class TestAccountView:

    def test_account_test(self, client):
        response = client.get(path='/api/v1/user/test')
        print(response)
        assert response.status_code == 200

    def test_account_create(self, client):
        json = {"user": {"email": "navid.mhkh@hotmail.com", "password": "1234"}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

    def test_account_login(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1
        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None

    def test_account_logout(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']

        headers = {"Authorization": "Bearer " + str(access_token)}
        response = client.delete(path='/api/v1/user/logout', headers=headers)
        assert response.status_code == 200

    def test_account_getbyid(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        response = client.get(path=f'/api/v1/user/{id}', headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user'] is not None
        assert j.loads(response.get_data())['user']['id'] == id

    def test_account_update_user(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        password2 = '6666'
        json = {'user': {'email': email, 'password': password2}}
        response = client.patch(path=f'/api/v1/user/{id}', json=json, headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == id
        assert j.loads(response.get_data())['user']['email'] == email

    def test_account_delete(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        response = client.delete(path=f'/api/v1/user/{id}', headers=headers)
        assert response.status_code == 200


"""
Topic view tests
"""


class TestTopicView:

    def test_topic_init_topic(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        title = 'topic id 1 for user id 1'
        json = {'topic': {'title': title}}
        response = client.post(path='/api/v1/topic/', json=json, headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title

    def test_topic_getbyid(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        title = 'topic id 1 for user id 1'
        json = {'topic': {'title': title}}
        response = client.post(path='/api/v1/topic/', json=json, headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        topic_id = j.loads(response.get_data())['topic']['id']

        response = client.get(path=f'/api/v1/topic/{topic_id}', headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        assert j.loads(response.get_data())['topic']['id'] == topic_id

    def test_topic_update_topic(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        title = 'topic id 1 for user id 1'
        json = {'topic': {'title': title}}
        response = client.post(path='/api/v1/topic/', json=json, headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        topic_id = j.loads(response.get_data())['topic']['id']

        title2 = 'title 1 that is edited by user id 1'
        json = {'topic': {'title': title2}}
        response = client.patch(path=f'/api/v1/topic/{topic_id}', json=json, headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title2

    def test_topic_delete_topic(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        title = 'topic id 1 for user id 1'
        json = {'topic': {'title': title}}
        response = client.post(path='/api/v1/topic/', json=json, headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        topic_id = j.loads(response.get_data())['topic']['id']

        response = client.delete(path=f'/api/v1/topic/{topic_id}', headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['message'] == 'successful'
        assert j.loads(response.get_data())['status'] == 200

    def test_topic_invite_user_to_topic(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        title = 'topic id 1 for user id 1'
        json = {'topic': {'title': title}}
        response = client.post(path='/api/v1/topic/', json=json, headers=headers)

        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        assert j.loads(response.get_data())['topic']['owner_id'] == id
        topic_id = j.loads(response.get_data())['topic']['id']

        response = client.get(path=f'/api/v1/topic/{topic_id}/invite/{id}', headers=headers)
        assert response.status_code == 400

        user2 = User(email='navid.mhkh@yahoo.com', password='1234')
        db.session.add(user2)
        db.session.commit()
        response = client.get(path=f'/api/v1/topic/{topic_id}/invite/{user2.id}', headers=headers)
        topic = Topic.get(topic_id)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        assert user2.has_in_waiting_list(topic=topic)

    def test_topic_follow_topic(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        title = 'topic id 1 for user id 1'
        json = {'topic': {'title': title}}
        response = client.post(path='/api/v1/topic/', json=json, headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        assert j.loads(response.get_data())['topic']['owner_id'] == id
        topic_id = j.loads(response.get_data())['topic']['id']

        user2 = User(email='navid.mhkh@yahoo.com', password='1234')
        db.session.add(user2)
        db.session.commit()
        response = client.get(path=f'/api/v1/topic/{topic_id}/invite/{user2.id}', headers=headers)
        topic = Topic.get(topic_id)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        assert user2.has_in_waiting_list(topic=topic)

        json = {'email': user2.email, 'password': '1234'}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        response = client.get(path=f'/api/v1/topic/{topic_id}/follow', headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        assert user2.has_followed(Topic.get(topic_id))

    def test_topic_reject_invitation(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        title = 'topic id 1 for user id 1'
        json = {'topic': {'title': title}}
        response = client.post(path='/api/v1/topic/', json=json, headers=headers)

        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        assert j.loads(response.get_data())['topic']['owner_id'] == id
        topic_id = j.loads(response.get_data())['topic']['id']

        user2 = User(email='navid.mhkh@yahoo.com', password='1234')
        db.session.add(user2)
        db.session.commit()
        response = client.get(path=f'/api/v1/topic/{topic_id}/invite/{user2.id}', headers=headers)
        topic = Topic.get(topic_id)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        assert user2.has_in_waiting_list(topic=topic)

        json = {'email': user2.email, 'password': '1234'}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        response = client.delete(path=f'/api/v1/topic/{topic_id}/reject', headers=headers)
        assert response.status_code == 200
        assert not user2.has_followed(topic=topic)
        assert not user2.has_in_waiting_list(topic=topic)
        assert user2 not in Topic.get(topic_id).invites
        assert user2 not in Topic.get(topic_id).followers

    def test_topic_add_post(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        title = 'topic id 1 for user id 1'
        json = {'topic': {'title': title}}
        response = client.post(path='/api/v1/topic/', json=json, headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        assert j.loads(response.get_data())['topic']['owner_id'] == id
        topic_id = j.loads(response.get_data())['topic']['id']

        content = 'blah blah'
        json = {'post': {'content': content}}
        response = client.put(path=f'/api/v1/topic/{topic_id}/post', json=json, headers=headers)
        assert response.status_code == 200
        assert Post.get(1).author_id == id
        assert Post.get(1).topic_id == topic_id


"""
Post view tests
"""


class TestPostView:

    def test_post_getbyid(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        title = 'topic id 1 for user id 1'
        json = {'topic': {'title': title}}
        response = client.post(path='/api/v1/topic/', json=json, headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        assert j.loads(response.get_data())['topic']['owner_id'] == id
        topic_id = j.loads(response.get_data())['topic']['id']

        content = 'blah blah'
        json = {'post': {'content': content}}
        response = client.put(path=f'/api/v1/topic/{topic_id}/post', json=json, headers=headers)
        assert response.status_code == 200
        assert Post.get(1).author_id == id
        assert Post.get(1).topic_id == topic_id
        post_id = 1

        response = client.get(path=f'/api/v1/post/{post_id}', headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['post']['content'] == content
        assert j.loads(response.get_data())['post']['id'] == post_id
        assert j.loads(response.get_data())['post']['topic_id'] == topic_id
        assert j.loads(response.get_data())['post']['author_id'] == id

    def test_post_update_post(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        title = 'topic id 1 for user id 1'
        json = {'topic': {'title': title}}
        response = client.post(path='/api/v1/topic/', json=json, headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        assert j.loads(response.get_data())['topic']['owner_id'] == id
        topic_id = j.loads(response.get_data())['topic']['id']

        content = 'blah blah'
        json = {'post': {'content': content}}
        response = client.put(path=f'/api/v1/topic/{topic_id}/post', json=json, headers=headers)
        assert response.status_code == 200
        assert Post.get(1).author_id == id
        assert Post.get(1).topic_id == topic_id
        post_id = 1

        content2 = 'content 2'
        json = {'post': {'content': content2}}
        response = client.patch(path=f'/api/v1/post/{post_id}', json=json, headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['post']['content'] == content2

    def test_post_delete_post(self, client):
        email = "navid.mhkh@hotmail.com"
        password = "1234"
        json = {"user": {"email": email, "password": password}}
        response = client.post(path='/api/v1/user/', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['user']['id'] == 1

        id = j.loads(response.get_data())['user']['id']
        json = {'email': email, 'password': password}
        response = client.post(path='/api/v1/user/login', json=json)
        assert response.status_code == 200
        assert j.loads(response.get_data())['access_token'] is not None
        access_token = j.loads(response.get_data())['access_token']
        headers = {"Authorization": "Bearer " + str(access_token)}

        title = 'topic id 1 for user id 1'
        json = {'topic': {'title': title}}
        response = client.post(path='/api/v1/topic/', json=json, headers=headers)
        assert response.status_code == 200
        assert j.loads(response.get_data())['topic']['title'] == title
        assert j.loads(response.get_data())['topic']['owner_id'] == id
        topic_id = j.loads(response.get_data())['topic']['id']

        content = 'blah blah'
        json = {'post': {'content': content}}
        response = client.put(path=f'/api/v1/topic/{topic_id}/post', json=json, headers=headers)
        assert response.status_code == 200
        assert Post.get(1).author_id == id
        assert Post.get(1).topic_id == topic_id
        post_id = 1

        response = client.delete(path=f'/api/v1/post/{post_id}', headers=headers)
        assert response.status_code == 200
        assert not Post.get(1)
