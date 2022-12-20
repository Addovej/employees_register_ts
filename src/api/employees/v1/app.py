from aiohttp.web import Request, Response, RouteTableDef
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from api.utils import extract_id
from conf import settings
from exceptions import NotFoundException, ValidationException
from models import Employee
from schemas import EmployeeListSchema, EmployeeSchema, EmployeeUpdateSchema
from utils import JsonResponse

API_PREFIX = f'{settings.API_ROOT}/v1/employees'
router = RouteTableDef()


@router.get(f'{API_PREFIX}/')
async def get_list(request: Request) -> JsonResponse:
    employees_list: list[Employee] = await Employee.get_list()

    return JsonResponse(
        text=EmployeeListSchema(__root__=[employee for employee, *_ in employees_list])
    )


@router.get(f'{API_PREFIX}/{{id}}/')
async def get_item(request: Request) -> JsonResponse:
    _id = extract_id(request)
    employee: list[Employee] = await Employee.get(_id)
    if not employee:
        raise NotFoundException(text={'detail': f'Not found item with id={_id}'})

    return JsonResponse(text=EmployeeSchema.from_orm(employee))


@router.post(f'{API_PREFIX}/')
async def create_item(request: Request) -> JsonResponse:
    try:
        employee_data: EmployeeSchema = EmployeeSchema(**await request.json())
    except ValidationError as e:
        raise ValidationException(text={'detail': e.errors()})

    try:
        employee = await Employee.create(**employee_data.dict(exclude={'id'}))
    except IntegrityError:
        raise NotFoundException(
            text={'detail': f'Chief with id={employee_data.chief_id} does not exists'}
        )

    return JsonResponse(text=EmployeeSchema.from_orm(employee))


@router.put(f'{API_PREFIX}/{{id}}/')
async def update_item(request: Request) -> Response:
    _id = extract_id(request)
    try:
        employee_data: EmployeeUpdateSchema = EmployeeUpdateSchema(**await request.json())
    except ValidationError as e:
        raise ValidationException(text={'detail': e.errors()})

    employee: Employee = await Employee.get(_id)
    if not employee:
        raise NotFoundException(text={'detail': f'Not found item with id={_id}'})

    try:
        return JsonResponse(text=EmployeeSchema.from_orm(
            await employee.update(employee_data))
        )
    except IntegrityError:
        raise NotFoundException(
            text={'detail': f'Chief with id={employee_data.chief_id} does not exists'}
        )


@router.delete(f'{API_PREFIX}/{{id}}/')
async def delete_item(request: Request) -> Response:
    _id = extract_id(request)
    employee: Employee = await Employee.get(_id)
    if not employee:
        raise NotFoundException(text={'detail': f'Not found item with id={_id}'})

    await employee.delete()
    return Response(status=204)
