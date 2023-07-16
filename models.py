"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = info["pdes"] or ""  # primary designation for object
        self.name = info["name"] or None  # None if not named
        self.diameter = (
            float(info["diameter"]) if info["diameter"] else float("nan")
        )  # The diameter (presented in kilometers) of the NEO
        # pha is potentially hazardous asteroid
        self.hazardous = info["pha"] == "Y"

        # Initial collection of linked approaches to this NEO. Initially is an empty list.
        # A collection of this NearEarthObjects close approaches to Earth.
        self.approaches = []

    @property
    def fullname(self):
        """Return a string representation of the full name of this NEO.

        Use `self.designation` and `self.name` to build a fullname for this object.

        Return `(No name specified)` if both are empty."""
        if self.name:
            return f"{self.designation} ({self.name})"
        elif self.designation:
            return f"{self.designation}"
        else:
            return "(No name specified)"

    def __str__(self):
        """Return `str(self)`."""
        # TODO: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        isHazardous = "is" if self.hazardous else "is not"
        return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and {isHazardous} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def serialize(self):
        """Return a dictionary containing the instance's data."""
        return {
            "designation": self.designation,
            "name": self.name,
            "diameter_km": self.diameter,
            "potentially_hazardous": self.hazardous,
        }


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        :param _designation: The primary designation for the referenced NEO, default is "".
        :param time: The date and time, in UTC, at which the NEO passes closest to Earth, default is None.
        :param distance: The nominal approach distance, in astronomical units, of the NEO to Earth at the closest point, default is 0.0.
        :param velocity: The velocity, in kilometers per second, of the NEO relative to Earth at the closest point, default is 0.0.


        """
        self._designation = info["designation"] or ""
        self.time = cd_to_datetime(info["time"]) if info["time"] else None
        self.distance = float(
            info["distance"]) if info["distance"] else float(0.0)
        self.velocity = float(
            info["velocity"]) if info["velocity"] else float(0.0)

        # Create an attribute for the referenced NEO, initialize as None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        # Return a human-readable string representation.
        return f"At {self.time_str}, '{self.neo.fullname}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def serialize(self):
        """Return a dictionary containing this object's attributes for clarity"""
        return {
            "datetime_utc": self.time_str,
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
        }
