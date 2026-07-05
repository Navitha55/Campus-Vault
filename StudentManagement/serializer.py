from rest_framework import serializers
from .models import StudentDetail,EmployeeDetails

class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetail
        fields = "__all__"

        read_only_fields = ['id']
        extra_kwargs = {
            'place':{
                'required':False,
                'default':'India'
            }
        }

        def validate(self,data):
            if not data['name'].isalpha():
                raise serializers.ValidationError('Invalid Name')
            if len(data['roll']) != 10:
                raise serializers.ValidationError('Invalid Roll Number')
            return data
        
class EmployeeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDetails
        fields = "__all__"
        read_only_fields = ['id']

    def validate(self, data):
        name_val = data.get('emp_name', '')
        if not name_val.replace(" ", "").isalpha():
            raise serializers.ValidationError({'emp_name': 'Invalid Name'})
        phone_val = data.get('emp_phone', '')
        if not phone_val.isdigit() or len(phone_val) != 10:
            raise serializers.ValidationError({'emp_phone': 'Invalid phone number. Must be exactly 10 digits.'})
        return data