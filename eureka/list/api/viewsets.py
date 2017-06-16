from ..models import List
from .serializers import ListSerializer
from .permissions import IsAuthor

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
        else:
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
        else:
            data = serializer.data
            list_object = self.get_object(uuid)
            list_object.name=data['name']
            list_object.priority=data['priority']
            list_object.save()
            return Response(status=status.HTTP_200_OK)


    def delete(self, request, uuid, format=None):
        list_object = self.get_object(uuid)
        list_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)            




class AuthorListViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, version):
        """ Get all Lists """
        Lists = List.objects.filter(author=request.user)#
        serializer = ListSerializer(Lists, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Adding a new List. """
        serializer = ListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=
                status.HTTP_400_BAD_REQUEST)
        else:
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

