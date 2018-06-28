from rest_framework import serializers
from leave.models import LeaveRules

class LeaveRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRules
        fields = [
            'pk',
            'leave_type',
            'leave_rules',
        ]

        # read_only_fields = ['pk','leave_type']

    def validate_leave_type(self,value):
        qs = LeaveRules.objects.filter(leave_type__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("The title must be unique")
        return value
