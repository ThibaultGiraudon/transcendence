from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.files import File
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class Player(models.Model):
	currentGameID = models.IntegerField(default=None, null=True)
	allGames = ArrayField(models.IntegerField(), default=list)
	isReady = models.BooleanField(default=False)	
	soloPoints = ArrayField(models.IntegerField(), default=list)
	deathPoints = ArrayField(models.IntegerField(), default=list)
	tournamentPoints = ArrayField(models.IntegerField(), default=list)
	totalPoints = ArrayField(models.IntegerField(), default=list)
	averagePoints = models.FloatField(default=0)
	isInvited = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		if not self.soloPoints:
			self.soloPoints.append(0)
			self.deathPoints.append(0)
			self.tournamentPoints.append(0)
			self.totalPoints.append(0)
		super().save(*args, **kwargs)

	def join_game(self):
		self.isReady = True
		self.save()


class Game(models.Model):
	date = models.DateTimeField(default=timezone.now)
	duration = models.IntegerField()
	playerList = ArrayField(models.IntegerField())
	gameMode = models.CharField(max_length=50)
	isOver = models.BooleanField(default=False)
	scores = models.ManyToManyField('Score', related_name='scores')
	subGames = ArrayField(models.IntegerField(), default=list)
	finalGame = models.IntegerField(default=None, null=True)
	thirdPlaceGame = models.IntegerField(default=None, null=True)
	parentGame = models.IntegerField(default=None, null=True)

	def save(self, *args, **kwargs):
		super(Game, self).save(*args, **kwargs)


class Score(models.Model):
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	position = models.IntegerField()
	score = models.IntegerField()


class CustomUserManager(BaseUserManager):
	def create_user(self, email, username, password=None, photo=None, **extra_fields):
		
		if not email:
			raise ValueError('The Email field must be set')
		email = self.normalize_email(email)

		player = Player.objects.create(currentGameID=None)
		user = self.model(email=email, username=username, player=player, **extra_fields)

		if photo is None:
			with open(settings.DEFAULT_IMAGE_PATH, 'rb') as default_image_file:
				user.photo.save('default.jpg', File(default_image_file), save=False)
		else:
			user.photo = photo
		
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		return self.create_user(email, username, password=password, **extra_fields)


class CustomUser(AbstractUser):
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=150, unique=True)
	is42 = models.BooleanField(default=False)
	isOfficial = models.BooleanField(default=False)
	photo = models.ImageField(upload_to='', default='default.jpg')
	follows = ArrayField(models.IntegerField(), default=list)
	friendRequests = ArrayField(models.IntegerField(), default=list)
	status = models.CharField(max_length=150, default="online")
	nbNewNotifications = models.IntegerField(default=0)
	blockedUsers = ArrayField(models.IntegerField(), default=list)
	player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='user', null=True)
	favoritesChannels = ArrayField(models.TextField(), default=list)
	resetPasswordID = models.CharField(max_length=150, default='')
	emailAlerts = models.BooleanField(default=True)

	# Use the custom manager
	objects = CustomUserManager()

	class Meta:
		# Allow to change the AUTH_USER_MODEL in settings.py
		swappable = 'AUTH_USER_MODEL'

	def __str__(self):
		return self.username
	
	def save(self, *args, **kwargs):
		super(CustomUser, self).save(*args, **kwargs)
	
	def set_status(self, status):
		self.status = status
		self.save()


class Notification(models.Model):
	user = models.ForeignKey(CustomUser, related_name='notifications', on_delete=models.CASCADE)
	title = models.CharField(max_length=150, default='')
	message = models.TextField()
	date = models.DateTimeField(default=timezone.now)
	redirect = models.CharField(max_length=150, default='')
	interacted = models.BooleanField(default=False)
	read = models.BooleanField(default=False)
	type = models.CharField(max_length=150, default='')
	imageType = models.CharField(max_length=150, default='')
	imageUser = models.CharField(max_length=150, default='')
	userID = models.IntegerField(default=0)

	def save(self, *args, **kwargs):
		super(Notification, self).save(*args, **kwargs)
		self.user.nbNewNotifications += 1
		self.user.save()
		self.send_notification()

	def interact(self):
		Notification.objects.filter(id=self.id).update(interacted=True)
		self.user.save()
	
	def send_notification(self):
		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)(
			f"notifications_{self.user.id}",
			{
				"type": "notification_message"
			}
		)


class Channel(models.Model):
	private = models.BooleanField(default=False)
	tournament = models.BooleanField(default=False)
	room_id = models.CharField(max_length=150, unique=True)
	name = models.CharField(max_length=150)
	users = models.ManyToManyField(CustomUser, related_name='channels')
	creator = models.IntegerField(default=0)
	description = models.TextField(default='')
	last_interaction = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		super(Channel, self).save(*args, **kwargs)


class Message(models.Model):
	sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	message = models.TextField()
	timestamp = models.DateTimeField(default=timezone.now)
	channel = models.ForeignKey(Channel, related_name='messages', on_delete=models.CASCADE)

	def __str__(self):
		return self.message
	
	def save(self, *args, **kwargs):
		super(Message, self).save(*args, **kwargs)