from factory import DictFactory, Sequence
from faker import Factory as FakerFactory

faker = FakerFactory.create()  # type: ignore


class Employee(DictFactory):
    chief_id: int = Sequence(lambda _: None)
    first_name: str = faker.first_name()
    last_name: str = faker.last_name()
    middle_name: str = Sequence(lambda _: None)

    position: str = 'Job Position'
    hire_date: str = faker.date()
    salary: float = faker.random_number(digits=4)
