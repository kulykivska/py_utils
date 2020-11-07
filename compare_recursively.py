from common.domain.value import ConstrainedString


def is_objects_same(expected_result: dict[str, object], actual_result: dict[str, object]) -> bool:
    result: list[bool] = list()
    for key, expected_value in expected_result.items():
        if type(actual_result) == dict:
            actual_value: object = actual_result.get(key, None)
        else:
            raise AssertionError(f'Unknown type {type(actual_result)}')

        if isinstance(expected_value, dict) and isinstance(actual_value, dict):
            is_objects_same(expected_value, actual_value)
        else:
            if isinstance(actual_value, ConstrainedString):
                result.append(expected_value == actual_value.value)
            else:
                result.append(expected_value == actual_value)

    return all(result)
