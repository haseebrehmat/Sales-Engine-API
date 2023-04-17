from rest_framework import serializers

from authentication.models.company import CompanyAPIIntegration, Company


class CompanySerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)

    class Meta:
        model = Company
        fields = "__all__"

    def create(self, validated_data):
        name = validated_data.get('name', None)
        status = validated_data.get('status', False)

        code = self.create_unique_code(name)
        obj = Company.objects.create(name=name, code=code, status=status)
        return obj

    def create_unique_code(self, name):
        # generate a unique code her with company first three letter
        name_part = name.upper()[:3]
        no_part = Company.objects.count() + 1
        return f"{name_part}_{no_part}"

class CompanyAPIIntegrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyAPIIntegration
        fields = "__all__"
        depth = 1

    def create(self, validated_data):
        company = validated_data.pop("company_id")
        return CompanyAPIIntegration.objects.create(**validated_data, company_id=company)
