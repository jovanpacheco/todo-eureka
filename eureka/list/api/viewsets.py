from ..models import List,Item
from .serializers import ListSerializer,ItemSerializer,UserSerializer
from .permissions import IsAuthor
from django.contrib.auth.models import User

# REST Framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from django.shortcuts import Http404

class AllListViewSet(APIView):
    permission_classes = (IsAuthenticated,IsAdminUser)

    def get(self, request,version):
        """ Get all Lists """
        Lists = List.objects.filter()#
        serializer = ListSerializer(Lists, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Adding a new List. """
        serializer = ListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=
                status.HTTP_400_BAD_REQUEST)

        data = serializer.data
        author = request.user
        l = List(
            author=author, name=data['name'],
            priority=data['priority'],
            active=True)
        l.save()
        request.data['uuid'] = l.uuid # return id
        return Response(request.data, status=status.HTTP_201_CREATED)


class ObjectListViewSet(APIView):
    permission_classes = (IsAuthenticated,IsAdminUser)

    def get_object(self, uuid):
        try:
            return List.objects.get(uuid=uuid)
        except List.DoesNotExist:
            raise Http404

    def get(self, request, version, uuid):
        """ Get List by uuid """
        list_object = self.get_object(uuid)
        serializer = ListSerializer(list_object)
        return Response(serializer.data)

    def put(self, request, uuid):
        """ Update a List """
        serializer = ListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data
        list_object = self.get_object(uuid)
        list_object.name=data['name']
        list_object.priority=data['priority']
        list_object.save()
        return Response(status=status.HTTP_200_OK)


    def delete(self, request, version, uuid, format=None):
        list_object = self.get_object(uuid)
        list_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)            




class AuthorListViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, version):
        """ Get all Lists by author"""
        Lists = List.objects.filter(author=request.user)#
        serializer = ListSerializer(Lists, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Adding a new List. """
        serializer = ListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=
                status.HTTP_400_BAD_REQUEST)

        data = serializer.data
        author = request.user
        l = List(
            author=author, name=data['name'],
            priority=data['priority'],
            active=True)
        l.save()
        request.data['uuid'] = l.uuid # return id
        return Response(request.data, status=status.HTTP_201_CREATED)


class ObjectAuthorListViewSet(ObjectListViewSet):
    permission_classes = (IsAuthenticated,IsAuthor)



class AllItemViewSet(APIView):
    permission_classes = (IsAuthenticated,IsAdminUser)

    def get(self, request,version):
        """ Get all items """
        objects_list = Item.objects.filter()#
        serializer = ItemSerializer(objects_list, many=True,context={'request': request})
        return Response(serializer.data)

    def post(self, request,version):
        """ Adding a new Item. """
        serializer = ItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=
                status.HTTP_400_BAD_REQUEST)
        data = serializer.data
        author = request.user

        try:
            list = List.objects.get(uuid=data['uuid_list'])
        except List.DoesNotExist:
            return Response({'detail':'List does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            assigned_to = User.objects.get(username=data['assigned_to'])
        except User.DoesNotExist:
            return Response({'detail':'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        l = Item(
            author=author,
            note=data['note'],
            priority=data['priority'],
            active=True,
            title=data['title'],
            list=list,
            assigned_to=assigned_to,
            due_date=data['due_date']
            )
        l.save()

        request.data['uuid'] = l.uuid # return id
        return Response(request.data, status=status.HTTP_201_CREATED)




class AllItemForListViewSet(APIView):

    permission_classes = (IsAuthenticated,IsAuthor)

    def get(self, request,version,uuid):
        """ Get all items for one list by uuid """

        completed = self.request.query_params.get('completed', None)
        objects_list = Item.objects.filter(list__uuid=uuid)#
        if completed is not None:
            objects_list = objects_list.filter(completed=True)

        serializer = ItemSerializer(objects_list, many=True)
        return Response(serializer.data)


class ObjectItemViewSet(APIView):

    permission_classes = (IsAuthenticated,IsAuthor)

    def get_object(self, uuid):
        try:
            return Item.objects.get(uuid=uuid)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, version, uuid):
        """ Get Item by uuid """
        list_object = self.get_object(uuid)
        serializer = ItemSerializer(list_object)
        return Response(serializer.data)

    def put(self, request, version,uuid):
        """ Update a Item """
        serializer = ItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data
        list_object = self.get_object(uuid)
        list_object.note = data['note']
        list_object.title = data['title']
        list_object.priority = data['priority']
        list_object.due_date = data['due_date']
        list_object.completed = data['completed']   
        list_object.save()
        return Response(status=status.HTTP_200_OK)


    def delete(self, request, version, uuid, format=None):
        list_object = self.get_object(uuid)
        list_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CompletedItemViewSet(APIView):

    permission_classes = (IsAuthenticated,IsAuthor)

    def get_object(self, uuid):
        try:
            return Item.objects.get(uuid=uuid)
        except Item.DoesNotExist:
            raise Http404        


    def put(self, request, version,uuid):
        """ completed a Item """

        list_object = self.get_object(uuid)
        list_object.completed = True  
        list_object.save()
        return Response(status=status.HTTP_200_OK)



class RegistrationView(APIView):
    """ Allow registration of new users. """
    permission_classes = ()

    def post(self, request,version):
        serializer = UserSerializer(data=request.data)

        # Check format and unique constraint
        if not serializer.is_valid():
            return Response(serializer.errors,\
                            status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data

        u = User.objects.create(username=data['username'])
        u.set_password(data['password'])
        u.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)