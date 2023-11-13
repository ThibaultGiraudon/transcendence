from django.db import models

Class	Player(models.Model):
	firstName = models.CharField(max_length=20);
	name = models.CharField(max_length=20);
	idName = models.CharField(max_length=20);
	# TODO : img = models.ImageField(upload_to='images/')

Class	Game(models.Model):
	date = models.DateField();
	hour = models.TimeField();
	duration = models.IntegerField();
	# TODO (pas utile puisqu'on a players.size() je pense) : nbRealPlayers = models.IntegerField(min=1);
	players = models.ManyToManyField(Player);

Class	Score(models.Model):
	players = models.ForeignKey(Player, on_delete=models.CASCADE);
	game = models.ForeignKey(Game, on_delete=models.CASCADE);
	points = models.IntegerField();