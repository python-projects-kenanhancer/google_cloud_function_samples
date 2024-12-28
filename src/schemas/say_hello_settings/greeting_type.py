from enum import Enum


class GreetingType(str, Enum):
    BASIC = "basic"
    TIME_BASED = "time_based"
    HOLIDAY = "holiday"
