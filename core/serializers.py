from rest_framework import serializers
from .models import Customer, Profession, DataSheet, Document


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'dtype', 'doc_number', 'customer')

        # read_only_fields = ['customer']


class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ('id', 'description', 'historical_data')


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id', 'description')


class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField()
    data_sheet = DataSheetSerializer()
    profession = ProfessionSerializer(many=True)
    doc_num = DocumentsSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'name', 'address', 'profession', 'data_sheet',
                  'active', 'status_message', 'num_professions', 'doc_num')

    def create(self, validate_data):
        profession = validate_data['profession']
        del validate_data['profession']

        data_sheet = validate_data['data_sheet']
        del validate_data['data_sheet']

        d_sheet = DataSheet.objects.create(**data_sheet)

        customer = Customer.objects.create(**validate_data)

        customer.data_sheet = d_sheet

        # for doc in doc_num:
        #     Document.objects.create(
        #         dtype=doc_num['dtype'],
        #         doc_number=doc_num['doc_number']
        #     )

        for pro in profession:
            prof = Profession.objects.create(**pro)
            customer.profession.add(prof)

        customer.save()

        return customer

    def get_num_professions(self, obj):
        return obj.num_professions()

    def get_data_sheet(self, obj):
        return obj.data_sheet.description
