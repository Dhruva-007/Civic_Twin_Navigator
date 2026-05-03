import googlemaps
from typing import Dict, Any, List, Optional
import logging

from config.settings import settings

# Setup logging
logger = logging.getLogger(__name__)


class MapsService:
    """
    Google Maps service for Civic Twin Navigator.
    Handles polling station location, directions, and travel time.
    """

    def __init__(self):
        try:
            self.client = googlemaps.Client(key=settings.google_maps_api_key)
            logger.info("Google Maps Service initialized successfully")
        except Exception as e:
            logger.error(f"Maps initialization error: {e}")
            raise Exception(f"Maps setup failed: {str(e)}")


    def get_polling_stations(
        self,
        location: str,
        radius_meters: int = 5000
    ) -> List[Dict[str, Any]]:
        """
        Find nearby polling stations or government offices.

        Args:
            location: User location string or address
            radius_meters: Search radius in meters

        Returns:
            List of nearby polling related places
        """
        try:
            # Geocode the location first
            geocode_result = self.client.geocode(location)

            if not geocode_result:
                logger.warning(f"Could not geocode location: {location}")
                return []

            # Get lat/lng
            lat_lng = geocode_result[0]["geometry"]["location"]

            # Search for government offices near location
            places_result = self.client.places_nearby(
                location=lat_lng,
                radius=radius_meters,
                keyword="election booth polling station government office"
            )

            stations = []
            for place in places_result.get("results", [])[:5]:
                stations.append({
                    "name": place.get("name", ""),
                    "address": place.get("vicinity", ""),
                    "rating": place.get("rating", 0),
                    "location": place.get("geometry", {}).get("location", {}),
                    "place_id": place.get("place_id", "")
                })

            logger.info(f"Found {len(stations)} polling stations near {location}")
            return stations

        except Exception as e:
            logger.error(f"Get polling stations error: {e}")
            return []


    def get_directions(
        self,
        origin: str,
        destination: str,
        mode: str = "driving"
    ) -> Dict[str, Any]:
        """
        Get directions from origin to polling station.

        Args:
            origin: Starting location
            destination: Polling station address
            mode: driving, walking, transit, bicycling

        Returns:
            Directions with duration and distance
        """
        try:
            directions = self.client.directions(
                origin=origin,
                destination=destination,
                mode=mode
            )

            if not directions:
                return {
                    "success": False,
                    "error": "No directions found"
                }

            leg = directions[0]["legs"][0]

            return {
                "success": True,
                "origin": leg.get("start_address", origin),
                "destination": leg.get("end_address", destination),
                "distance": leg["distance"]["text"],
                "duration": leg["duration"]["text"],
                "duration_seconds": leg["duration"]["value"],
                "mode": mode,
                "steps": [
                    {
                        "instruction": step.get(
                            "html_instructions", ""
                        ).replace("<b>", "").replace("</b>", ""),
                        "distance": step["distance"]["text"],
                        "duration": step["duration"]["text"]
                    }
                    for step in leg.get("steps", [])[:5]
                ]
            }

        except Exception as e:
            logger.error(f"Get directions error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def get_travel_time(
        self,
        origin: str,
        destination: str
    ) -> Dict[str, Any]:
        """
        Get estimated travel time to polling station.

        Args:
            origin: User current location
            destination: Polling station address

        Returns:
            Travel time estimates for different modes
        """
        try:
            modes = ["driving", "walking", "transit"]
            results = {}

            for mode in modes:
                try:
                    directions = self.client.directions(
                        origin=origin,
                        destination=destination,
                        mode=mode
                    )
                    if directions:
                        leg = directions[0]["legs"][0]
                        results[mode] = {
                            "duration": leg["duration"]["text"],
                            "distance": leg["distance"]["text"]
                        }
                except Exception:
                    results[mode] = {
                        "duration": "unavailable",
                        "distance": "unavailable"
                    }

            return {
                "success": True,
                "origin": origin,
                "destination": destination,
                "travel_times": results,
                "recommendation": self._get_travel_recommendation(results)
            }

        except Exception as e:
            logger.error(f"Get travel time error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def geocode_location(
        self,
        location: str
    ) -> Dict[str, Any]:
        """
        Convert location string to coordinates.

        Args:
            location: Location string or address

        Returns:
            Geocoded location data
        """
        try:
            result = self.client.geocode(location)

            if not result:
                return {
                    "success": False,
                    "error": "Location not found"
                }

            location_data = result[0]
            return {
                "success": True,
                "formatted_address": location_data.get("formatted_address", ""),
                "lat": location_data["geometry"]["location"]["lat"],
                "lng": location_data["geometry"]["location"]["lng"],
                "city": self._extract_city(location_data),
                "state": self._extract_state(location_data),
                "country": self._extract_country(location_data)
            }

        except Exception as e:
            logger.error(f"Geocode error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def _get_travel_recommendation(
        self,
        travel_times: Dict
    ) -> str:
        """Get best travel mode recommendation"""
        try:
            if "transit" in travel_times:
                transit_duration = travel_times["transit"].get("duration", "")
                if transit_duration and transit_duration != "unavailable":
                    return f"Take public transport - {transit_duration}"

            if "driving" in travel_times:
                driving_duration = travel_times["driving"].get("duration", "")
                if driving_duration and driving_duration != "unavailable":
                    return f"Drive to polling station - {driving_duration}"

            return "Check local transport options"

        except Exception:
            return "Plan your route in advance"


    def _extract_city(self, location_data: Dict) -> str:
        """Extract city from geocode result"""
        for component in location_data.get("address_components", []):
            if "locality" in component["types"]:
                return component["long_name"]
        return ""


    def _extract_state(self, location_data: Dict) -> str:
        """Extract state from geocode result"""
        for component in location_data.get("address_components", []):
            if "administrative_area_level_1" in component["types"]:
                return component["long_name"]
        return ""


    def _extract_country(self, location_data: Dict) -> str:
        """Extract country from geocode result"""
        for component in location_data.get("address_components", []):
            if "country" in component["types"]:
                return component["long_name"]
        return ""


    def test_connection(self) -> Dict[str, Any]:
        """Test Google Maps connection"""
        try:
            result = self.client.geocode("Pune, Maharashtra, India")
            if result:
                return {
                    "connected": True,
                    "test_location": "Pune, Maharashtra, India",
                    "result": result[0].get("formatted_address", "")
                }
            return {
                "connected": False,
                "error": "No result returned"
            }
        except Exception as e:
            return {
                "connected": False,
                "error": str(e)
            }


# Single instance
maps_service = MapsService()