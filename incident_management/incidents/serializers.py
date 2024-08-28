from rest_framework import serializers
from .models import User, Incident


from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",  # Use email as the username
            "first_name",
            "last_name",
            "password",
            "phone_number",
            "address",
            "pin_code",
            "city",
            "country",
            "state",
            "user_category",
        ]
        extra_kwargs = {
            "password": {"write_only": True},  # Password should be write-only
            "email": {"required": True},  # Ensure email is required
        }

    def create(self, validated_data):
        # Pop the password out of the validated data to handle it separately
        password = validated_data.pop("password")

        # Create the user object without saving to the database yet
        user = User(**validated_data)

        # Set the user's password (this hashes it)
        user.set_password(password)

        # Save the user to the database
        user.save()

        return user


class IncidentSerializer(serializers.ModelSerializer):
    reporter_user_type = serializers.CharField(
        source="reporter.user_category", read_only=True
    )
    reporter_first_name = serializers.CharField(
        source="reporter.first_name", read_only=True
    )
    reporter_email = serializers.EmailField(source="reporter.email", read_only=True)
    entity_type = serializers.ChoiceField(choices=Incident.ENTITY_TYPE_CHOICES)

    class Meta:
        model = Incident
        fields = [
            "id",
            "incident_id",
            "reporter",
            "reporter_user_type",
            "reporter_email",
            "entity_type",
            "details",
            "reported_date",
            "priority",
            "status",
            "reporter_first_name",
        ]
        read_only_fields = ["id", "incident_id", "reporter", "reported_date"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["reporter"] = user
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["reporter_first_name"] = instance.reporter.first_name
        representation["reporter_user_type"] = instance.reporter.user_category
        representation["reporter_email"] = instance.reporter.email
        return representation
