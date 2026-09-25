# src/pyhabitat/adapters/__init__.py

from __future__ import annotations

all = [
    "is_android_kivy"
]
_KIVY_EXPORTS = {
    "is_android_kivy",
}
def __getattr__(name: str):

    if name in _KIVY_EXPORTS:
        from . import kivy
        value = getattr(kivy, name)

    else:
        raise AttributeError(
            f"module {__name__!r} has no attribute {name!r}"
        )

    # Cache resolved attribute for future lookups
    globals()[name] = value

    return value


def __dir__():
    return sorted(
        __all__ + [
            "__all__",
            "__builtins__",
            "__cached__",
            "__doc__",
            "__file__",
            "__getattr__",
            "__loader__",
            "__name__",
            "__package__",
            "__path__",
            "__spec__",
        ]
    )
