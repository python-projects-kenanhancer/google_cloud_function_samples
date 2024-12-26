from enum import Enum


class GreetingType(str, Enum):
    BASIC = "basic"
    TIMEBASED = "timebased"
    HOLIDAY = "holiday"
