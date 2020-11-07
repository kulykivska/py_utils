from dataclasses import dataclass
from typing import TypedDict


@dataclass(frozen=True, eq=True)
class CityData:
    country: str
    region: str | None
    subregion: str | None
    city: str

    def make_query(self) -> str:
        if self.subregion and self.region:
            return f'{self.city}, {self.subregion}, {self.region}, {self.country}'
        elif self.region:
            return f'{self.city}, {self.region}, {self.country}'
        else:
            return f'{self.city}, {self.country}'


class GeocodeAddressComponent(TypedDict):
    long_name: str
    short_name: str
    types: list[str]


class GeocodeLocation(TypedDict):
    lat: float
    lng: float


class GeocodeRectangle(TypedDict):
    northeast: GeocodeLocation
    southwest: GeocodeLocation


class GeocodeGeometry(TypedDict):
    bounds: GeocodeRectangle
    location: GeocodeLocation
    location_type: str
    viewport: GeocodeRectangle


class GeocodeResult(TypedDict):
    address_components: list[GeocodeAddressComponent]
    geometry: GeocodeGeometry
    formatted_address: str
    place_id: str
    types: list[str]
