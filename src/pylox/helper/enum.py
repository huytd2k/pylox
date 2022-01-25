import enum


class AutoName(enum.Enum):
    def _generate_next_value_(name, _, __, ___):
        return name
