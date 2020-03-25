from django.db import models
from django.conf import settings
from django.template import loader, Context
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from datetime import datetime
from threading import Thread

class Request(models.Model):
	class Admin:
		list_display = ('opened', 'creator', 'title', 'updated', 'closed')
		list_display_links = ('title',)
		search_fields = ('title', 'description')
		date_hierarchy = 'opened'
	class Meta:
		verbose_name = _('Request')
		verbose_name_plural = _('Requests')
		ordering = ('-opened',)
	created = models.DateTimeField(blank=True, editable=False, verbose_name=_('Created'))
	creator = models.ForeignKey(User, related_name='created_request_set', editable=False, verbose_name=_('Creator'))
	opened = models.DateTimeField(blank=True, editable=False, verbose_name=_('Opened'))
	updated = models.DateTimeField(blank=True, editable=False, verbose_name=_('Updated'))
	updator = models.ForeignKey(User, related_name='updated_request_set', editable=False)
	closed = models.DateTimeField(blank=True, editable=False, null=True, verbose_name=_('Closed'))
	nosy = models.ManyToManyField(User, verbose_name=_('Interested Parties'))
	title = models.CharField(maxlength=256, verbose_name=_('Title'))
	description = models.TextField(maxlength=16384, verbose_name=_('Description'))
	def __str__(self):
		return self.title
	def get_absolute_url(self):
		return '/robot/%s/' % (self.id,)
	def timetrack(self):
		return sum(map(lambda x: x.timetrack, self.action_set.all()))
	def transcript(self, template="robot/request.txt"):
		if hasattr(settings, 'SITE_HTTPS') and settings.SITE_HTTPS:
			proto = 'https'
		else:
			proto = 'http'
		site = Site.objects.get(id=settings.SITE_ID)
		request_uri = '%s://%s%s' % (proto, site.domain, self.get_absolute_url())
		context = {
			'now' : datetime.now(),
			'request' : self,
			'request_uri' : request_uri,
		}
		c = Context(context)
		t = loader.get_template(template)
		message = t.render(c)
		return message
	def save(self):
		if not self.id: ### new request
			if not self.created:
				self.created = datetime.now()
			if not self.opened:
				self.opened = self.created
			if not self.updated:
				self.updated = self.created
			self.updator = self.creator
			super(Request, self).save()
			self.nosy.add(self.creator)
			admin = User.objects.get(username=settings.ROBOT_ADMIN)
			if not self.nosy.filter(id=admin.id):
				self.nosy.add(admin)
			Action.objects.create(
				request = self,
				creator = self.updator,
				description = self.title,
				explanation = 'Request has been created',
			)
		else: ### request object already exists
			old = Request.objects.get(pk=self.id)
			if self.closed and not old.closed:
				### request has been closed
				super(Request, self).save()
				Action.objects.create(
					request = self,
					creator = self.updator,
					description = 'Request has been closed',
					explanation = 'Automatically generated message',
				)
			elif not self.closed and old.closed:
				### request has been re-opened
				self.opened = datetime.now()
				super(Request, self).save()
				Action.objects.create(
					request = self,
					creator = self.updator,
					description = 'Request has been reopened',
					explanation = 'Automatically generated message',
				)
			else:
				super(Request, self).save()

class Action(models.Model):
	class Admin:
		list_display = ('created', 'request', 'description')
		date_hierarchy = 'created'
		search_fields = ('description', 'explanation')
	class Meta:
		verbose_name = _('Action')
		verbose_name_plural = _('Actions')
		ordering = ('-created',)
	created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
	creator = models.ForeignKey(User, verbose_name=_('Creator'))
	request = models.ForeignKey(Request)
	description = models.CharField(maxlength=256, verbose_name=_('Description'))
	explanation = models.TextField(maxlength=16384, verbose_name=_('Explanation'))
	timetrack = models.PositiveSmallIntegerField(
			default=0,
			verbose_name=_('Time Taken'),
	)
	def save(self):
		if not self.id:
			new = True
		else:
			new = False
		super(Action, self).save()
		if new:
			self.request.updated = self.created
			self.request.save()
			def _notify(*av):
				for user in av:
					self.notify(user)
			t = Thread(target=_notify, args=self.request.nosy.filter())
			t.run()

	def notify(self, user):
		if hasattr(settings, 'ROBOT_NOTIFY_TEMPLATE'):
			template = settings.ROBOT_NOTIFY_TEMPLATE
		else:
			template = 'robot/notify.txt'
		robot = User.objects.get(username = settings.ROBOT_ADMIN)
		if hasattr(settings, 'SITE_HTTPS') and settings.SITE_HTTPS:
			proto = 'https'
		else:
			proto = 'http'
		site = Site.objects.get(id=settings.SITE_ID)
		request_uri = '%s://%s%s' % (proto, site.domain, self.request.get_absolute_url())
		context = {
			'robot' : robot,
			'recipient' : user,
			'action' : self,
			'request_uri' : request_uri,
		}
		c = Context(context)
		t = loader.get_template(template)
		message = t.render(c)

		if not hasattr(settings, 'EMAIL_HOST'): ### debugging
			print message
			return

		from os import popen
		fp = popen('/usr/sbin/sendmail -t', 'w')
		fp.write(message)
		fp.close()
