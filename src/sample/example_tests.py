import pytest
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse

fake = Faker()


@pytest.mark.django_db()
def test_{{hump_main_class}}_format(
    api_client,
    {{hump_main_class}},
    {{hump_main_class}}_format,
):
    """Формат {{main_class}}"""
    url = reverse(
        'api:{{app-name}}:{{main-class}}-detail',
        [{{hump_main_class}}.pk],
    )

    json_response = api_client.get(url).json()

    assert json_response == {{hump_main_class}}_format({{hump_main_class}})


@pytest.mark.django_db()
def test_{{hump_main_class}}_post(
    api_client,
):
    """Создание {{main_class}}"""
    url = reverse('api:{{app-name}}:{{main-class}}-list')
    json_response = api_client.post(
        url,
        data={},
        format='json',
    )

    assert json_response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db()
def test_{{hump_main_class}}_delete(
    api_client,
    {{hump_main_class}},
):
    """Удаление {{main_class}}"""
    url = reverse(
        'api:{{app-name}}:{{main-class}}-detail',
        [{{hump_main_class}}.pk],
    )

    json_response = api_client.delete(url)

    assert json_response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_{{hump_main_class}}_change(
    api_client,
    {{hump_main_class}},
):
    """Изменение {{main_class}}"""
    url = reverse(
        'api:{{app-name}}:{{main-class}}-detail',
        [{{hump_main_class}}.pk],
    )

    json_response = api_client.put(
        url,
        data={},
        format='json',
    )

    assert json_response.status_code == status.HTTP_200_OK
