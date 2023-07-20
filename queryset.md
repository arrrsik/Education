1. Создание объектов (метод save())
```
- p = models.Person(name='Игорь', surname='Тестеров', patronymic='Тестерович')
- p.save()
```
1.1 Создание объектов (метод create())
```
p = models.Person.objects.create(name='Игорь', surname='Бутыкин', patronymic='Палыч')
```
1.2 get_or_create()
```
person_data = {
    'surname': 'Фамилия',
    'name': 'Имя',
    'patronymic': 'Отчество',
    'date': '1990-01-01',
    'phone': 123456789,
    'health': 'Практически здоров',
    'gender': 'M',
    'image': 'path/to/image.jpg',
}

person, created_person = Person.objects.get_or_create(
    surname=person_data['surname'],
    name=person_data['name'],
    patronymic=person_data['patronymic'],
    date=person_data['date'],
    defaults=person_data  # Данные, которые будут использоваться при создании объекта
)

```
1.3 update_or_create()
```
person, created = Person.objects.update_or_create(
    name='Имя',
    defaults={
        'surname': 'Новая фамилия',
        'patronymic': 'Новое отчество',
        'date': '1990-01-01',
        'phone': 987654321,
        'health': 'Новое состояние здоровья',
        'gender': 'W',
        'image': 'path/to/new_image.jpg',
    }
)

```
1.4 bulk_create()
```
emergency_data = [
    EmergencyService(name='Служба 1', code=1, phone='111-111-111'),
    EmergencyService(name='Служба 2', code=2, phone='222-222-222'),
    EmergencyService(name='Служба 3', code=3, phone='333-333-333'),
]
EmergencyService.objects.bulk_create(emergency_data)

```
2. Сохранение изменений в объектах
```
person.name = 'Евгентий'
person.save()
person.name
'Евгентий'

```
2.1 bulk_update()
```
people_to_update = [
    Person(id=1, surname='Новая фамилия 1', patronymic='Новое отчество 1'),
    Person(id=2, surname='Новая фамилия 2', patronymic='Новое отчество 2'),
    Person(id=3, surname='Новая фамилия 3', patronymic='Новое отчество 3'),
]
# Определяем поля, которые нужно обновить
fields_to_update = ['surname', 'patronymic']

# Выполняем обновление полей для выбранных объектов
Person.objects.bulk_update(people_to_update, fields_to_update)
```
2.2 update()
```
EmergencyService.objects.filter(name='Служба 1').update(phone='123-456-789')
```
3. Сохранение полей ForeignKey и ManyToManyField
- ForeignKey
``` 
person = models.Person.objects.last()
incident = models.Incident.objects.first()
incident.applicant = person
incident.save()
incident.applicant

<Person: Царев-Евгентий-Викторович-1999-11-11-Ковид>

```
- ManyToMany
``` 
set():
service_1 = EmergencyService.objects.create(name='Служба 1', code=1, phone='111-111-111')
service_2 = EmergencyService.objects.create(name='Служба 2', code=2, phone='222-222-222')
incident.service.set([service_1, service_2])

add():
emergency_service = EmergencyService.objects.create(name='Служба', code=1, phone='123-456-789')
person = Person.objects.create(surname='Фамилия', name='Имя', patronymic='Отчество')
incident = Incident.objects.create(applicant=person)
incident.service.add(emergency_service)
```
4. Получение объектов
- Получение всех объектов
``` 
models.Incident.objects.all()
```
- Получение определенных объектов с помощью фильтров
``` 
models.Person.objects.filter(name='Евгений')
```
- Исключение
``` 
models.Person.objects.exclude(name='Евгений')
```

- Получение одного объекта
``` 
person = models.Person.objects.last()
person = models.Person.objects.first()
person = models.Person.objects.get(id=1)

```
- Ограничение QuerySet
```  
Person.objects.all()[:5]
Person.objects.all()[5:10]
Person.objects.all()[:10:2]
Person.objects.order_by('name')[0]
```
- Поиск c помощью lookup
``` 
models.Person.objects.filter(phone__isnull=True)
models.Person.objects.filter(name__icontains='е')
models.Person.objects.filter(date__lte='2020-02-01')
```
- alias()
```
models.Person.objects.alias(count_of_incidents=Count('incidents')).filter(count_of_incidents__lt=3)
```
- order_by()
```
models.Person.objects.all().order_by('-id')
```
- reverse()
```
models.Person.objects.reverse()
```
- distinct()
```
models.Person.objects.all().distinct()
```
- values()
```
models.Person.objects.all().values()
```
- values_list()
```
 models.Person.objects.all().values_list()
```
- none()
```
models.Person.objects.none()
```
- union()
```
combined_queryset = models.Person.objects.all().union(models.EmergencyService.objects.all())
```
- intersection()
```
intersection_queryset = models.Person.objects.filter(name__startswith='A').intersection(models.EmergencyService.objects.filter(code=1))
```
- difference()
```
difference_queryset = models.Person.objects.exclude(id__in=models.EmergencyService.objects.values('id'))
```
- extra()
```
person = models.Person.objects.extra(select={'db': 'date > "2000-01-01"'})
```
- defer()
```
 person = models.Person.objects.defer('health')
```
- only()
```
person = models.Person.objects.only('surname', 'date')
```
- using()
```
models.EmergencyService.objects.using('default').all()

```
- select_for_update()
```
Блокируем объект Person для изменений внутри транзакции

from django.db import transaction
with transaction.atomic():
    person = Person.objects.select_for_update().get(id=1)
    person.name = 'Новое имя'
    person.save()

```
- count()
```
models.Person.objects.count()
```
- in_bulk()
```
models.Person.objects.in_bulk([1, 2]) - возвращает словарь 
```
- latest(), earliest()
```
models.Incident.objects.latest('date')
models.Incident.objects.earliest('date')
```
- aggregate()
```
 average_age = models.Person.objects.aggregate(avg_age=Avg('id'))
 average_age
 {'avg_age': 7.0}
```
- exists()
```
models.Person.objects.exists()
```
- delete()
```
models.Person.objects.all().delete()
```
- explain()
```
queryset = models.Person.objects.filter(name='John').explain()
print(queryset)

3 0 0 SCAN core_person
19 0 0 USE TEMP B-TREE FOR ORDER BY
```
- in
```
models.Person.objects.filter(id__in=[1,3,5])
```
- startswith (istartswith)
```
models.Person.objects.filter(phone__startswith='9')

```
- endswith (iendswith)
```
models.Person.objects.filter(phone__endswith='9')

```
- range
```
start_date = datetime.date(2005, 1, 1)
end_date = datetime.date(2015, 3, 31)
models.Incident.objects.filter(date__range=(start_date, end_date))

```
- date
```
models.Incident.objects.filter(date__date=datetime.date(2005, 1, 1))
```
- year
```
models.Incident.objects.filter(date__year=2021)
```
- iso_year
```
models.Incident.objects.filter(date__iso_year=2021)
```
- month
```
models.Incident.objects.filter(date__month=12)
```
- day
```
models.Incident.objects.filter(date__day__gte=7)
```
- week
```
models.Incident.objects.filter(date__week=1)
```
- week_day
```
models.Incident.objects.filter(date__week_day=1)
```
- iso_week_day
```
models.Incident.objects.filter(date__iso_week_day=1)```
- quarter
```
models.Incident.objects.filter(date__quarter=1)
- time
```
models.Incident.objects.filter(date__time=date.time(14,30))
```
- hour
```
models.Incident.objects.filter(date__hour=1)
```
- minute
```
models.Incident.objects.filter(date__minute=1)
```
- second 
```
models.Incident.objects.filter(date__second=1)
```
- isnull
```
models.Person.objects.filter(image__isnull=False)
```
- regex (iregex)
```
models.Person.objects.filter(surname__regex=r'^A')
models.EmergencyService.objects.filter(name__regex=r'служба')
models.Incident.objects.filter(number__regex=r'1')

```

- annotate
```
person = models.Person.objects.annotate(num_incidents=Count('incidents'))
person.last().num_incidents
3
```
