from oxapy import serializer  # type: ignore


class TravelSerializer(serializer.Serializer):
    primus = serializer.CharField()
    terminus = serializer.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
