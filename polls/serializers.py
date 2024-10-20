from rest_framework import serializers
from .models import Question,Choice

class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Question
        fields=['id','question_text','pub_date','owner']

class ChoiceSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only = True) # type: ignore
    question_id = serializers.PrimaryKeyRelatedField(
        queryset = Question.objects.all(), source='question', write_only =True
    )
    
    class Meta:
        model=Choice
        fields=['id','choice_text','votes', 'question', 'question_id']
        
class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, source='choice_set')
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model=Question
        fields=['id','question_text','pub_date', 'owner','choices']
        
        
# class QuestionSerializer(serializers.ModelSerializer):  
#      class Meta:
#         model=Question
#         fields=['id','question_text','pub_date']  
        
def validate_question_text(self, value):
        if 'spam' in value.lower():
            raise serializers.ValidationError("N spam allowed in question text")
        return value