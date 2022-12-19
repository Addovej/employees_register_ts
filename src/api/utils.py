from aiohttp.web import Request

from exceptions import ValidationException


def extract_id(request: Request, field_name: str = 'id') -> int:
    try:
        _id_value = request.match_info.get(field_name)
        if _id_value:
            return int(_id_value)
        raise ValidationException(text={'detail': 'ID must not be an empty'})
    except ValueError:
        raise ValidationException(text={'detail': 'ID must be integer'})
