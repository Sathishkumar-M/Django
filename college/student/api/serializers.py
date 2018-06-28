from rest_framework import serializers
from student.models import Course,Student,Fee

class CourseSerializer(serializers.ModelSerializer):
    fee = serializers.SerializerMethodField('get_fees')
    class Meta:
        model = Course
        fields = [
            'coursename', 'describtion','fee'
        ]
        # depth = 1
        read_only_fields = ['coursename','describtion']

    def get_fees(self, instance):
        obj = Fee.objects.get(id=instance.pk)
        context = {
            'amount': obj.amount,
            'details': obj.details
        }
        return context


class StudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,allow_blank=False)
    class Meta:
        model = Student
        fields = [
            'pk','firstname','middlename','lastname','dob','gender','qualification','email','phone','city','state','country','enroll_date','course'
        ]
        # depth = 1
        # fields = '__all__'

        read_only_fields = ['pk']

    def validate_email(self,value):
        qs = Student.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This email already exists")
        return value


class StudentSerializerlist(StudentSerializer):
    course = CourseSerializer(many=False,read_only=True)

    # def validate_leave_type(self,value):
    #     qs = LeaveRules.objects.filter(leave_type__iexact=value)
    #     if self.instance:
    #         qs = qs.exclude(pk=self.instance.pk)
    #     if qs.exists():
    #         raise serializers.ValidationError("The title must be unique")
    #     return value
