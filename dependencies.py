from typing import Any, Type, TypeVar, cast

T = TypeVar('T')


class DependencyContainer:
    def __init__(self) -> None:
        self.dependencies: dict = dict()

    def register_dependency(self, interface: Type[T], implementation: T) -> None:
        self.dependencies[interface] = implementation

    def get(self, interface: Type[T], *generics) -> T:
        if generics:
            instance: Any = self.dependencies[(interface, *generics)]
            return cast(T, instance)
        else:
            return self.dependencies[interface]

    def get_optional(self, interface: Type[T], *generics) -> T | None:
        if generics:
            instance: Any | None = self.dependencies.get((interface, *generics), None)
            if instance:
                return cast(T, instance)
            else:
                return None
        else:
            return self.dependencies.get(interface, None)
