# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .models import List,Item
from django.contrib.auth.models import User
from list.forms import ListForm,ItemForm
from json import loads
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.hashers import make_password
from list.api.viewsets import (
    AllListViewSet,ObjectListViewSet,AuthorListViewSet,ObjectAuthorListViewSet,
    AllItemViewSet,CompletedItemViewSet,ObjectItemViewSet,AllItemForListViewSet
)

class ListAndItemCase(TestCase):
    def setUp(self):
        self.user_author = User.objects.create(email="autor@mail.com",username="name_author")
        self.one_list = List.objects.create(name="ToDo One", author=self.user_author,priority=3)

    def test_list_author(self):
        """Cantidad de autores"""

        one_list = List.objects.get(name="ToDo One")
        self.assertEqual(one_list.count_by_author(one_list.author), 1)
        self.assertEqual(
        	self.one_list.count_by_author(self.one_list.author),
        	one_list.count_by_author(one_list.author))

    def test_list_equal_by_name(self):
        """Por el mismo nombre"""

        one_list = List.objects.get(name="ToDo One")
        self.assertEqual(one_list,self.one_list)

    def test_list_priority(self):
        """Prioridad limitada 1-4"""
        self.assertTrue(self.one_list.priority >= 0 and self.one_list.priority <= 4)




class RegistrationTest(APITestCase):
    """Testing the registration of new users and login"""

    def test_register(self):
        """ Register a user acccount. """
        response = self.client.post(reverse_lazy('list_app:new_user',
        kwargs={'version':'v1'}),
        {
            "username":"userapi",
            "password":"clave"
        })


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




class ListApiTest(APITestCase):

    def setUp(self):
        self.user_author = User.objects.create(
            email="autor@mail.com",username="name_author",is_staff=True,
            password=make_password('JPjp1234'),is_superuser=True)

        self.factory = APIRequestFactory()

    def create_todo(self,data):

        view = AllListViewSet.as_view()
        request = self.factory.post('api/v1/list/',data)
        force_authenticate(request, user=self.user_author)
        response = view(request)   
        return response

    def test_create_todo_201(self):


        data = {
            'name':'remember the milk',
            'priority':2,
            'author':self.user_author
        }
        response = self.create_todo(data)
    
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_todo_400(self):
        """ bad request in post"""

        data = {
            'name':'list bad request',
        }
        response = self.create_todo(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_todo_200(self):

        view = AllListViewSet.as_view()
        # Make an authenticated request to the view...
        request = self.factory.get('api/v1/list/')
        force_authenticate(request,user=self.user_author)
        response = view(request,'v1')        

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_todo_200(self):

        view = ObjectListViewSet.as_view()

        data = {
            'name':'other list',
            'priority':3,
            'author':self.user_author
        }        
        response = self.create_todo(data)

        url = 'api/v1/list/%s/' % response.data['uuid']
        request = self.factory.get(url)
        force_authenticate(request,user=self.user_author)
        response = view(request,'v1',response.data['uuid'])        

        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_update_todo_200(self):

        view = ObjectListViewSet.as_view()

        data = {
            'name':'bad name list',
            'priority':1,
            'author':self.user_author
        }        
        response = self.create_todo(data)

        url = 'api/v1/list/%s/' % response.data['uuid']

        new_data = {
            'name':'Good name list',
            'priority':1,            
        }
        request = self.factory.put(url,new_data)
        force_authenticate(request,user=self.user_author)
        response = view(request,'v1',response.data['uuid'])        

        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_delete_todo_204(self):

        view = ObjectListViewSet.as_view()

        data = {
            'name':'other list',
            'priority':3,
            'author':self.user_author
        }        
        response = self.create_todo(data)

        url = 'api/v1/list/%s/' % response.data['uuid']
        request = self.factory.delete(url)
        force_authenticate(request,user=self.user_author)
        response = view(request,'v1',response.data['uuid'])        

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 

    def test_todos_author_200(self):

        view = AuthorListViewSet.as_view()

        all_data = [
            {'name':'By author 1','priority':1,'author':self.user_author},
            {'name':'By author 2','priority':1,'author':self.user_author},
            {'name':'By author 3','priority':1,'author':self.user_author}
        ]
        for data in all_data:
            self.create_todo(data)

        # Make an authenticated request to the view...
        request = self.factory.get('api/v1/author_list/')
        force_authenticate(request,user=self.user_author)
        response = view(request,'v1')

        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_create_todo_author_201(self):
        """ Autor by request """

        data = {
            'name':'Automatic author',
            'priority':2
        }
        view = AuthorListViewSet.as_view()
        request = self.factory.post('api/v1/author_list/',data)
        force_authenticate(request, user=self.user_author)
        response = view(request) 

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)        




class ItemApiTest(ListApiTest):

    def setUp(self):
        super(ItemApiTest,self).setUp()

        list = self.create_todo({
            'name':'List whith items',
            'priority':3,
            'author':self.user_author
        })

        self.list= list.data['uuid']


    def create_item(self,data):
        view = AllItemViewSet.as_view()
        request = self.factory.post('api/v1/item/',data)
        force_authenticate(request, user=self.user_author)
        response = view(request,'v1') 
        return response

    def test_create_item_201(self):
        """ Create item for list"""

        data = {
            'author':self.user_author,
            'note':'Note 1 for one activity',
            'priority':2,
            'title':'activity 1',
            'uuid_list':self.list,
            'assigned_to':self.user_author
        }

        response = self.create_item(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 



    def test_list_all_item_200(self):
            
        all_data = [
        {   
            'author':self.user_author,'note':'Note 1 for one activity','priority':2,
            'title':'activity 1','uuid_list':self.list,'assigned_to':self.user_author},
        {'author':self.user_author,'note':'Note 2 for','priority':3,'title':'activity 2','uuid_list':self.list,'assigned_to':self.user_author}       
        ]

        for data in all_data:
            self.create_item(data)            


        view = AllItemViewSet.as_view()
        request = self.factory.get('api/v1/item/')
        force_authenticate(request, user=self.user_author)
        response = view(request,'v1')  
                   
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_completed_item_200(self):
        """ Create item for list"""

        data = {
            'author':self.user_author,
            'note':'Note 1 for one activity',
            'priority':2,
            'title':'activity 1',
            'uuid_list':self.list,
            'assigned_to':self.user_author
        }

        response = self.create_item(data)
        view = CompletedItemViewSet.as_view()
        request = self.factory.put('api/v1/item/%s/completed' % response.data['uuid'])
        force_authenticate(request, user=self.user_author)
        response = view(request,'v1',response.data['uuid']) 

        self.assertEqual(response.status_code, status.HTTP_200_OK)         


    def test_detail_item_200(self):
        """ detail item"""

        data = {
            'author':self.user_author,
            'note':'Note 1 for one activity',
            'priority':2,
            'title':'activity 1',
            'uuid_list':self.list,
            'assigned_to':self.user_author
        }

        response = self.create_item(data)
        view = ObjectItemViewSet.as_view()
        request = self.factory.get('api/v1/item/%s/' % response.data['uuid'])
        force_authenticate(request, user=self.user_author)
        response = view(request,'v1',response.data['uuid']) 

        self.assertEqual(response.status_code, status.HTTP_200_OK)     

        
    def test_update_todo_200(self):

        view = ObjectItemViewSet.as_view()

        data = {
            'author':self.user_author,
            'note':'Note 1 for one activity',
            'priority':2,
            'title':'activity 1',
            'uuid_list':self.list,
            'assigned_to':self.user_author
        }

        response = self.create_item(data)

        url = 'api/v1/item/%s/' % response.data['uuid']

        new_data = {
            'author':self.user_author,
            'note':'Note 1 for one activity updated',
            'priority':1,
            'title':'activity 1',
            'uuid_list':self.list,
            'assigned_to':self.user_author
        }
        request = self.factory.put(url,new_data)
        force_authenticate(request,user=self.user_author)
        response = view(request,'v1',response.data['uuid'])        

        self.assertEqual(response.status_code, status.HTTP_200_OK)     


    def test_delete_item_204(self):

        view = ObjectItemViewSet.as_view()

        data = {
            'author':self.user_author,
            'note':'Note 1 for one activity',
            'priority':2,
            'title':'activity 1',
            'uuid_list':self.list,
            'assigned_to':self.user_author
        }        
        response = self.create_item(data)

        url = 'api/v1/item/%s/' % response.data['uuid']
        request = self.factory.delete(url)
        force_authenticate(request,user=self.user_author)
        response = view(request,'v1',response.data['uuid'])        

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 

    def test_all_item_for_list_200(self):
            
        all_data = [
        {   
            'author':self.user_author,'note':'Note 1 for one activity','priority':2,
            'title':'activity 1','uuid_list':self.list,'assigned_to':self.user_author},
        {
            'author':self.user_author,'note':'Note 2 for','priority':3,'title':'activity 2','uuid_list':self.list,'assigned_to':self.user_author}       
        ]

        for data in all_data:
            self.create_item(data)            


        view = AllItemForListViewSet.as_view()
        request = self.factory.get('api/v1/item/list/%s' % self.list)
        force_authenticate(request, user=self.user_author)
        response = view(request,'v1',self.list)  
                   
        self.assertEqual(response.status_code, status.HTTP_200_OK)
