from rest_framework import serializers
from bboard.models import Rubric


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        # fields = ('id', 'name')
        fields = '__all__'
