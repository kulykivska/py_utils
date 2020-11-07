from abc import ABC
from dataclasses import dataclass
from typing import TypeVar, Generic

from common.domain.value import ConstrainedString

T = TypeVar("T")


@dataclass
class BaseDifferencesValue(Generic[T], ABC):
    old_version: T
    new_version: T

    def to_dict(self) -> dict[str, object]:
        return {
            "old_version": self.old_version.to_dict(),  # type:ignore
            "new_version": self.new_version.to_dict()  # type:ignore
        }


class NameDifferencesValue(BaseDifferencesValue[ConstrainedString]):
    pass


class TitleDifferencesValue(BaseDifferencesValue[ConstrainedString]):
    pass
