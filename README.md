# Генератор файлов для django приложения
Данная программа позволяет генерировать файлы сериализаторов, представлений,
тестов и административной панели исходя из информации о модели

# Примеры сгенерированных файлов

##### Сериализатор:
```python
from rest_framework import serializers

from server.apps.mobile_provision.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """Аккаунт."""

    class Meta(object):
        model = Account
        fields = ['user', 'photo', 'birth_date', 'passport_series', 'passport_number']


class AccountSerializer(serializers.Serializer):
    """Аккаунт."""

        user = serializers.None(__change_me__)
        photo = serializers.ImageField()
        birth_date = serializers.DateField()
        passport_series = serializers.CharField()
        passport_number = serializers.CharField()
```

##### Представление (доступно как с правами, так и без прав доступа)
```python
from rest_framework.viewsets import ModelViewSet

from server.apps.mobile_provision.api.serializers import AccountSerializer
from server.apps.mobile_provision.models import Account


class AccountViewSet(ModelViewSet):
    """Аккаунт."""

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    ordering_fields = ['user', 'photo', 'birth_date', 'passport_series', 'passport_number']
    search_fields = ['user', 'photo', 'birth_date', 'passport_series', 'passport_number']



from rest_framework.viewsets import ModelViewSet
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from server.apps.mobile_provision.api.serializers import AccountSerializer
from server.apps.mobile_provision.models import Account

class AccountViewSet(
    NestedViewSetMixin,
    AutoPermissionViewSetMixin,
    ModelViewSet,
):
    """Аккаунт."""

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    ordering_fields = ['user', 'photo', 'birth_date', 'passport_series', 'passport_number']
    search_fields = ['user', 'photo', 'birth_date', 'passport_series', 'passport_number']
    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        'list': 'list',
        'metadata': None,
    }
```

##### Права доступа
```python
import rules
from rules.predicates import is_authenticated


rules.add_perm('mobile_provision.view_account', is_authenticated)
rules.add_perm('mobile_provision.add_account', is_authenticated)
rules.add_perm('mobile_provision.change_account', is_authenticated)
rules.add_perm('mobile_provision.delete_account', is_authenticated)
rules.add_perm('mobile_provision.list_account', is_authenticated)
```

##### Тесты
```python
import pytest
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse

fake = Faker()


@pytest.mark.django_db()
def test_account_format(
    api_client,
    account,
    account_format,
):
    """Формат Account."""
    url = reverse(
        'api:mobile-provision:account-detail',
        [account.pk],
    )

    json_response = api_client.get(url).json()

    assert json_response == account_format(account)


@pytest.mark.django_db()
def test_account_post(
    api_client,
):
    """Создание Account."""
    url = reverse('api:mobile-provision:account-list')
    json_response = api_client.post(
        url,
        data={},
        format='json',
    )

    assert json_response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db()
def test_account_delete(
    api_client,
    account,
):
    """Удаление Account."""
    url = reverse(
        'api:mobile-provision:account-detail',
        [account.pk],
    )

    json_response = api_client.delete(url)

    assert json_response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_account_change(
    api_client,
    account,
):
    """Изменение Account."""
    url = reverse(
        'api:mobile-provision:account-detail',
        [account.pk],
    )

    json_response = api_client.put(
        url,
        data={},
        format='json',
    )

    assert json_response.status_code == status.HTTP_200_OK
```

##### Админка
```python
from django.contrib import admin
from server.apps.mobile_provision.model import Account


@admin.register(Account)
class ConfigurableAdmin(admin.ModelAdmin[Account]):
    """Аккаунт."""

    list_filter = ['user', 'photo', 'birth_date', 'passport_series', 'passport_number']
    search_fields = ['user', 'photo', 'birth_date', 'passport_series', 'passport_number']
    list_display = ['user', 'photo', 'birth_date', 'passport_series', 'passport_number']
```

##### Файл conftest для тестов
```python
import pytest
from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker
from pytest_factoryboy import register
from rest_framework.fields import DateTimeField
from rest_framework.test import APIClient

from server.apps.mobile_provision.models import Account

fake = Faker()


class AccountFactory(DjangoModelFactory):
    """Фабрика для Account."""

    class Meta(object):
        model = Account

    user = factory.SubFactory(__change_me__)
    photo = factory.LazyAttribute(lambda account: fake.file_name())
    birth_date = factory.LazyAttribute(lambda account: fake.date_between())
    passport_series = factory.LazyAttribute(lambda account: fake.paragraph())
    passport_number = factory.LazyAttribute(lambda account: fake.paragraph())


register(Account)


@pytest.fixture
def account_format():
    """Формат Account."""
    def _account_format(account: Account):
        return {
            'id': account.pk,
            'user': account.user,
            'photo': account.photo,
            'birth_date': account.birth_date,
            'passport_series': account.passport_series,
            'passport_number': account.passport_number,
        }
    return _account_format
```

## Получение результата
В файл **main** в переменную **tree** необходимо вставить код, который отвечает за 
создание модели и запустить его.
Сгенерированные файлы будут находиться в папке **src/done**.
Можно генерировать сразу несколько моделей, для каждой из них будут 
создаваться отдельные файлы, а файлы **src/done/admin.py** и 
**src/done/conftest.py** будут актуализироваться и дополняться нужными данными.

Запуск файла **clear** очищает директорию **src/done** и файлы 
**src/done/admin.py**, **src/done/conftest.py**.

## Особенности
1) При наличии документации в классе ("""Документация""") ее необходимо
изменить ("Документация").
2) При анализе кода будет учитываться только название класса, и его поля,
остальное (class Meta, property, функции) не анализируется
3) В файле **src/utils/utils.py** есть класс **Helper**. В нем установлена 
переменная **fields_django** в которой прописаны отношения между типом поля
модели и типом в сериализаторе и тестах. Данную переменную можно изменять и 
регулировать типы генерируемых полей.
4) При генерации файлов в импортах указывается путь без корневой папки. 
Не забудьте создать init файлы с импортами.

## Принцип работы
В директории **src/sample** лежат файлы-шаблоны, из которых и формируются 
исходные файлы. Их можно изменить под себя. Все что находится внутри **{{ }}** 
будет заменено на соответствующие данные. При добавлении новых **{{ }}** необходимо
актуализировать словарь **DICT_PARAMS** из которого и берутся данные
для подстановки.

Генерация самих файлов осуществляется в **src/generations**, а анализ модели в
**src/utils/analization.py**.

### Переменные получаемые из класса модели:
1) **{{list_main_fields}}** - список полей модели (['field1', 'field2'])
2) **fields_django_model** - словарь полей модели ({'name_field': 'type_field'})
3) **fields_for_serializers** - словарь полей для сериализатора 
({'name_field': 'type_field_for_serializers'})
4) **fields_for_conftest** - словарь полей для тестов 
({'name_field': 'type_field_for_test'})
5) **{{MainClass}}** - название класса (AccountModel)
6) **{{main_class}}** - название класса с _ (account_model)
7) **{{lower_MainClass}}** - название класса в нижнем регистре (accountmodel)
8) **{{main-class}}** - название класса с - (account-model)
9) **{{docs}}** - документация модели (документация модели вставляется во всех 
сгенерированных файлах)
