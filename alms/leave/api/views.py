from rest_framework import generics,mixins
from leave.models import LeaveRules
from .permissions import IsOwnerOrReadOnly
from .serializers import LeaveRulesSerializer

class LeaveRulesAPIView(mixins.CreateModelMixin,generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = LeaveRulesSerializer

    def get_queryset(self):
        return LeaveRules.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    # def put(self,request,*args,**kwargs):
    #     return self.update(request,*args,**kwargs)
    # def patch(self,request,*args,**kwargs):
    #     return self.update(request,*args,**kwargs)

class LeaveRulesRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = LeaveRulesSerializer
    # permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return LeaveRules.objects.all()
