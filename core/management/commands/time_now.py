from django.core.management.base import BaseCommand
from datetime import datetime


class Command(BaseCommand):
	help = 'Отображение текущего времени'

	def handle(self, *args, **kwargs):
		date = datetime.now().strftime('%x')
		time = datetime.now().strftime('%X')
		print(f'Сегодня {date} {time}')
