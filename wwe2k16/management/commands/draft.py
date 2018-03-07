import random
from django.core.management.base import BaseCommand
from wwe2k16.models import Championship, Wrestler, Brand

class Command(BaseCommand):
	def _generate_draft(self):
		championships = Championship.objects.filter(status = 1)
		wc, sc, ttc, exc, ch, top, sec, rest = [], [], [], [], [], [], [], []
		for championship in championships:
			for champion in championship.champion.all():
				if 'nxt' in championship.slug:
					exc.append(champion)
				elif championship.belt_type == 'PR':
					wc.append(champion)
				elif championship.belt_type == 'SE':
					sc.append(champion)
				elif championship.belt_type == 'TT':
					ttc.append(champion)
				ch.append(champion.name)
		wrestlers = Wrestler.objects.exclude(name__in = ch)
		sorted_wrestlers = sorted(wrestlers, key=lambda w: w.total_points(), reverse=True)
		for wrestler in sorted_wrestlers:
			if wrestler.ovr >= 90:
				top.append(wrestler)
			elif wrestler.ovr >= 87 and len(top) < 40:
				top.append(wrestler)
			elif wrestler.ovr >= 85 and len(sec) < 40:
				sec.append(wrestler)
			elif wrestler.ovr >= 84 and len(sec) < 40:
				sec.append(wrestler)
			else: rest.append(wrestler)

		for i in range(5):
			random.shuffle(wc)
			random.shuffle(sc)
			random.shuffle(ttc)
			random.shuffle(top)
			random.shuffle(sec)
			random.shuffle(rest)

		rest_count = (int)(len(rest) / 4)
		raw = [wc[0], sc[0], ttc[0], ttc[1]] + top[:10] + sec[:10] + rest[:rest_count]
		smackdown = [wc[1], sc[1], ttc[2], ttc[3]] + top[10:20] + sec[10:20] + rest[rest_count:2*rest_count]
		nxt = [wc[2], exc[0], exc[1], exc[2]] + top[20:30] + sec[20:30] + rest[2*rest_count:3*rest_count]
		legends = [wc[3], sc[2], ttc[4], ttc[5]] + top[30:] + sec[30:] + rest[3*rest_count:]

		raw_brand = Brand.objects.filter(name__icontains = 'raw')
		sd_brand = Brand.objects.filter(name__icontains = 'smack')
		nxt_brand = Brand.objects.filter(name__icontains = 'nxt')
		leg_brand = Brand.objects.filter(name__icontains = 'legend')
		for wrestler in raw:
			wrestler.brand = raw_brand
			wrestler.save()
		for wrestler in smackdown:
			wrestler.brand = sd_brand
			wrestler.save()
		for wrestler in nxt:
			wrestler.brand = nxt_brand
			wrestler.save()
		for wrestler in legends:
			wrestler.brand = leg_brand
			wrestler.save()

	def handle(self, *args, **kwargs):
		self._generate_draft()