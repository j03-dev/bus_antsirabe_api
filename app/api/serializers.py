from oxapy import serializer


class TravelSerializer(serializer.Serializer):
    primus = serializer.CharField()
    terminus = serializer.CharField()
