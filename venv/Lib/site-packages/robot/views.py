from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.main import ChangeList
from django import newforms as forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import datetime
from robot.models import Request, Action

if not hasattr(settings, 'SITE_NAME'):
	SITE_NAME=_('Request Administration')
else:
	SITE_NAME=settings.SITE_NAME

class NewRequestForm(forms.Form):
	title = forms.CharField(min_length=8, max_length=256, label=_('Title'),
				help_text=_('A short descriptive title for this request.'))
	description = forms.CharField(min_length=16, max_length=8192, widget=forms.Textarea, label=_('Description'),
				help_text=_('A longer, more elaboratively descriptive summary of the issue or request. "textile"-style markup is permitted here, or simply free-form text.'))

class AnnotationForm(forms.Form):
	explanation = forms.CharField(min_length=16, max_length=8192, widget=forms.Textarea, label=_('Annotation'),
				help_text=_('Annotation text for this issue. "textile"-style markup is permitted here, or simply free form text.'))
	timetrack = forms.IntegerField(initial=0, label=_('Time Taken'),
				help_text=_('The time in hours taken responding to this request, if appropriate.'))

@login_required
def request_new(request, template='robot/request_new.html'):
	if request.POST:
		f = NewRequestForm(request.POST, prefix='new')
		if f.is_valid():
			r = Request(creator=request.user)
			for k in f.cleaned_data:
				setattr(r, k, f.cleaned_data[k])
			r.save()
			return HttpResponseRedirect('../%s/' % (r.id,))
	else:
		f = NewRequestForm(prefix='new')

	context = {
		'SITE_NAME' : SITE_NAME,
		'form' : f,
	}

	c = RequestContext(request, context)
	t = loader.get_template(template)
	return HttpResponse(t.render(c))

@login_required
def request_view(request, pk, template='robot/request_view.html'):
	try: r = Request.objects.get(pk=pk)
	except Request.DoesNotExist:
		raise Http404

	annotation = AnnotationForm(prefix="annotation")
	if request.POST and request.POST.has_key('close'):
		r.closed = datetime.now()
		r.updator = request.user
		r.save()
	elif request.POST and request.POST.has_key('reopen'):
		r.closed = None
		r.updator = request.user
		r.save()
	elif request.POST and request.POST.has_key('annotate'):
		annotation = AnnotationForm(request.POST, prefix='annotation')
		if annotation.is_valid():
			a = Action(request=r, creator=request.user, description='Annotation')
			for k in annotation.cleaned_data:
				setattr(a, k, annotation.cleaned_data[k])
			a.save()
			annotation = AnnotationForm(prefix="annotation")

	context = {
		'SITE_NAME' : SITE_NAME,
		'request' : r,
		'annotation' : annotation,
	}

	c = RequestContext(request, context)
	t = loader.get_template(template)
	return HttpResponse(t.render(c))

@login_required
def request_list(request, template='robot/request_list.html'):
	context = {
		'SITE_NAME' : SITE_NAME,
		'cl' : ChangeList(request, Request),
	}
	c = RequestContext(request, context)
	t = loader.get_template(template)
	return HttpResponse(t.render(c))

@login_required
def request_txt(request, pk):
	try: r = Request.objects.get(pk=pk)
	except Request.DoesNotExist:
		raise Http404
	return HttpResponse(r.transcript(), mimetype="text/plain")
