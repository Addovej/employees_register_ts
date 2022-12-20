from aiohttp.test_utils import TestClient

from models import Employee

from .mixins import BaseTestCase


class BaseTestEmployee(BaseTestCase):
    _api_pref: str = '/api/v1/employees'

    VALIDATION_ERROR: dict[str, list[dict]] = {
        'detail': [
            {
                'loc': ['chief_id'],
                'msg': 'value is not a valid integer',
                'type': 'type_error.integer'
            },
            {
                'loc': ['hire_date'],
                'msg': 'invalid date format',
                'type': 'value_error.date'
            },
            {
                'loc': ['salary'],
                'msg': 'value is not a valid float',
                'type': 'type_error.float'
            }
        ]
    }


class TestEmployeeGetList(BaseTestEmployee):

    async def test_success_empty(self, client: TestClient) -> None:
        response = await client.get(f'{self._api_pref}/')
        res = await response.json()

        assert res == []

    async def test_success(self, client: TestClient, employee: dict) -> None:
        await Employee.create(**employee)

        response = await client.get(f'{self._api_pref}/')
        res = await response.json()

        assert len(res) == 1


class TestEmployeeGetItem(BaseTestEmployee):

    async def test_not_found(self, client: TestClient) -> None:
        response = await client.get(f'{self._api_pref}/999/')

        assert response.status == 404
        res = await response.json()
        assert res == {'detail': 'Not found item with id=999'}

    async def test_success(self, client: TestClient, employee: dict) -> None:
        _employee = await Employee.create(**employee)

        response = await client.get(f'{self._api_pref}/{_employee.id}/')
        assert response.status == 200
        res = await response.json()
        assert res['id'] == _employee.id


class TestEmployeeCreate(BaseTestEmployee):

    async def test_success(self, client: TestClient, employee: dict) -> None:
        response = await client.post(f'{self._api_pref}/', json=employee)

        assert response.status == 200
        res = await response.json()
        assert employee['first_name'] == res['first_name'] \
               and employee['last_name'] == res['last_name']

    async def test_validation_error(self, client: TestClient, employee: dict) -> None:
        response = await client.post(
            f'{self._api_pref}/', json={
                **employee,
                'chief_id': 'wrong_type',
                'salary': 'wrong_type',
                'hire_date': 'wrong_format'
            }
        )

        assert response.status == 400
        res = await response.json()
        assert res == self.VALIDATION_ERROR

    async def test_chief_not_found(self, client: TestClient, employee: dict) -> None:
        response = await client.post(
            f'{self._api_pref}/', json={**employee, 'chief_id': 999}
        )

        assert response.status == 404
        res = await response.json()
        assert res == {'detail': 'Chief with id=999 does not exists'}


class TestEmployeeUpdate(BaseTestEmployee):

    async def test_success(self, client: TestClient, employee: dict) -> None:
        _employee = await Employee.create(**employee)

        _new_position = 'New position'
        response = await client.put(
            f'{self._api_pref}/{_employee.id}/', json={'position': _new_position}
        )

        assert response.status == 200
        res = await response.json()
        assert res['position'] == _new_position
        assert res['position'] != _employee.position

    async def test_validation_error(self, client: TestClient, employee: dict) -> None:
        _employee = await Employee.create(**employee)

        response = await client.put(
            f'{self._api_pref}/{_employee.id}/', json={
                'chief_id': 'wrong_type',
                'salary': 'wrong_type',
                'hire_date': 'wrong_format'
            }
        )

        assert response.status == 400
        res = await response.json()
        assert res == self.VALIDATION_ERROR

    async def test_chief_not_found(self, client: TestClient, employee: dict) -> None:
        _employee = await Employee.create(**employee)

        response = await client.put(
            f'{self._api_pref}/{_employee.id}/', json={'chief_id': 999}
        )

        assert response.status == 404
        res = await response.json()
        assert res == {'detail': 'Chief with id=999 does not exists'}


class TestEmployeeDelete(BaseTestEmployee):

    async def test_success(self, client: TestClient, employee: dict) -> None:
        _employee = await Employee.create(**employee)

        response = await client.delete(f'{self._api_pref}/{_employee.id}/')

        assert response.status == 204

    async def test_not_found(self, client: TestClient) -> None:
        response = await client.delete(f'{self._api_pref}/999/')

        assert response.status == 404
        res = await response.json()
        assert res == {'detail': 'Not found item with id=999'}
