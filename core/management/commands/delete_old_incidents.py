import logging
from core import models
from datetime import timedelta
from time import sleep
from django.core.management import BaseCommand
from django.utils.timezone import now

UPDATE_TIME_DAYS = 7  # Через сколько дней будет повторяться проверка
INACTIVE_INCIDENTS_DAYS = 30  # Через сколько дней удалять происшествия

''' Каждый месяц команда будет чистить старые инциденты '''

class Command(BaseCommand):
    args = ''
    help = ''' Проверка данных о происшествиях '''
    logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument(
            '--infinitely',
            '-i',
            dest='infinitely',
            action='store_true',
            default=False,
            help='Регулярная обработка', )

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        if verbosity:
            self.logger.setLevel(logging.DEBUG)

        while True:
            date_to_check = now() - timedelta(days=INACTIVE_INCIDENTS_DAYS)

            self.logger.debug('Начинаю проверку наличие старых происшествий.')
            old_incidents = models.Incident.objects.filter(date__lt=date_to_check)
            self.logger.debug(f'Найдено происшествий в количестве {old_incidents.count()} штук')
            if old_incidents.count():
                self.logger.debug('Произвожу удаление')
                old_incidents.delete()

            if not options.get('infinitely'):
                self.logger.debug('Старых происшествий не обнаружено, для регулярной проверки укажите -i при запуске команды')
                break

            self.logger.debug(f'Новых происшествий не обнаружно, повторная проверка будет через {UPDATE_TIME_DAYS} дней')
            sleep(60 * 60 * 24 * UPDATE_TIME_DAYS)
