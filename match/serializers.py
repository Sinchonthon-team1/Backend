from rest_framework import serializers

class MatchSerializer(serializers.Serializer):
	teamName = serializers.CharField()
	school = serializers.CharField()
	matchDate = serializers.DateTimeField()
	teamScore = serializers.IntegerField()