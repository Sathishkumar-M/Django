from rest_framework import generics,mixins,status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from student.models import Course,Student,Fee
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
# from .permissions import IsOwnerOrReadOnly
from .serializers import StudentSerializer,CourseSerializer,StudentSerializerlist

class CourseAPIView(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = CourseSerializer
    permission_classes = (IsAdminUser,)

    def get(self, request,*args,**kwargs):
        try:
            data = Course.objects.all()
            serializer = CourseSerializer(data, many=True)
            context = {
                'message': 'Course details.',
                'status': status.HTTP_200_OK,
                'data': serializer.data,
            }
            return Response(context, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            context = {
                'message': 'Error 404, page not found.',
                'status': status.HTTP_404_NOT_FOUND,
                'errors': {
                    'detail': "Error 404, page not found.."
                },
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)

class StudentAPIView(viewsets.ModelViewSet):
    lookup_field = 'pk'
    # serializer_class = StudentSerializer
    permission_classes = (IsAdminUser,)
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StudentSerializerlist
        return StudentSerializer

    def list(self, request):
        try:
            data = Student.objects.all()
            serializer = StudentSerializerlist(data, many=True)
            context = {
                'message': 'Student details.',
                'status': status.HTTP_200_OK,
                'data': serializer.data,
            }
            return Response(context, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            context = {
                'message': 'Error 404, page not found.',
                'status': status.HTTP_404_NOT_FOUND,
                'errors': {
                    'detail': "Error 404, page not found.."
                },
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    # def get_queryset(self):
    #     return Student.objects.all()

    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            context = {
                'message': 'Errors in your request.',
                'status': status.HTTP_400_BAD_REQUEST,
                'errors': {
                    'detail': serializer.errors,
                },
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        # result = self.create(request,*args,**kwargs)
        context = {
            'message': 'Successfully created.',
            'status': status.HTTP_201_CREATED,
            'data': serializer.data,
        }
        return Response(context, status.HTTP_201_CREATED)


    # def put(self,request,*args,**kwargs):
    #     return self.update(request,*args,**kwargs)
    # def patch(self,request,*args,**kwargs):
    #     return self.update(request,*args,**kwargs)

class StudentRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAdminUser,)

    def get(self, request, pk, format=None):
        try:
            data = Student.objects.get(pk=pk)
            serializer = StudentSerializer(data)
            context = {
                'message': 'Student details.',
                'status': status.HTTP_200_OK,
                'data': serializer.data,
            }
            return Response(context, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            context = {
                'message': 'Error 404, page not found.',
                'status': status.HTTP_404_NOT_FOUND,
                'errors': {
                    'detail': "Error 404, page not found.."
                },
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    def put(self,request, pk,*args,**kwargs):
        try:
            obj = Student.objects.get(pk=pk)
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                context = {
                    'message': 'Errors in your request.',
                    'status': status.HTTP_400_BAD_REQUEST,
                    'errors': {
                        'detail': serializer.errors,
                    },
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            # serializer.update(request.data,obj)
            self.update(request,*args,**kwargs)
            context = {
                'message': 'Successfully updated.',
                'status': status.HTTP_200_OK,
                'data': serializer.data,
            }
            return Response(context, status.HTTP_200_OK)
        except Student.DoesNotExist:
            context = {
                'message': 'Error 404, page not found.',
                'status': status.HTTP_404_NOT_FOUND,
                'errors': {
                    'detail': "Error 404, page not found.."
                },
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, *args,**kwargs):
        try:
            data = Student.objects.get(pk=pk)
            data.delete()
            context = {
                'message': 'Successfully removed.',
                'status': status.HTTP_200_OK,
                'data': {},
            }
            return Response(context, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            context = {
                'message': 'Error 404, page not found.',
                'status': status.HTTP_404_NOT_FOUND,
                'errors': {
                    'detail': "Error 404, page not found.."
                },
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
