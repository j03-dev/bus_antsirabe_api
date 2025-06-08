from oxapy import serializer  # type: ignore


class TravelSerializer(serializer.Serializer):
    primus = serializer.CharField()
    terminus = serializer.CharField()
