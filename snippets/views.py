from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status, generics
from .models import Snippet
from .serializers import SnippetSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .permissions import IsOnwerOrReadOnly

# Create your views here.


# not that genric classes makes use of implicit mixins, check the docs
class SnippetList(generics.ListCreateAPIView):
    """List all code snippets or create a new snippet"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # Ensures that only authenticated users are able to create a snippet
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    # Associating snippet with the user that created it
    # overriding this implicit method enables changing how the instance save is managed
    # and handle any information that is implicit in the incoming request url
    # the create() method of the serializer will now be passed an additional 'owner' field along with the validated
    # data from the request
    # since the owner is read only from the serializer, we are updating the owner with the user instance from the
    # django request.user
    # The create() method of our serializer will now be passed an additional 'owner' field, along with
    # the validated data from the request.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a code snippet"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # Ensures that only authenticated users are able to update, or delete a snippet
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOnwerOrReadOnly, )


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class SnippetList(APIView):
#     """List all code snippets or create a new snippet"""
#
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class SnippetDetail(APIView):
#     """Retrieve, update or delete a code snippet"""
#
#     def get_objects(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_objects(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_objects(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_objects(pk)
#         snippet.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)
#
#
