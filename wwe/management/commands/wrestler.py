# import pandas as pd
from django.core.management.base import BaseCommand
from wwe.models import Wrestler


class Command(BaseCommand):
	def _create_wrestler(self):
		# wrestler_data = pd.read_csv('wwe/management/wrestler.csv')
		# wrestler_data = wrestler_data.fillna(0)
		# wrestler_data['name'] = wrestler_data['name'].apply(lambda x: x.title())
		# wrestler_data = wrestler_data.as_matrix()

		# for wrestler in wrestler_data:
		# 	data = Wrestler(
		# 		name = wrestler[0],
		# 		ovr = wrestler[1],
		# 		original_primary = ((int)(wrestler[2])),
		# 		primary = ((int)(wrestler[3])),
		# 		secondary = ((int)(wrestler[4])),
		# 		tag_team = ((int)(wrestler[5]))
		# 	)
		# 	data.save()
		print('Done')

	def handle(self, *args, **kwargs):
		self._create_wrestler()
