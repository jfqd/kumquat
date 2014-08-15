from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from kumquat.utils import LoginRequiredMixin
from kumquat.models import Domain
from models import Account, Redirect
from forms import AccountUpdateForm
import json

# Accounts

class AccountList(LoginRequiredMixin, ListView):
	model = Account

class AccountCreate(LoginRequiredMixin, CreateView):
	model = Account
	success_url = reverse_lazy('mail_account_list')
	
	def form_valid(self, form):
		password = form.cleaned_data.get('password')
		self.object = form.save(commit=False)
		self.object.set_password(password)
		self.object.save()
		return super(AccountCreate, self).form_valid(form)


class AccountUpdate(LoginRequiredMixin, UpdateView):
	model = Account
	form_class = AccountUpdateForm
	success_url = reverse_lazy('mail_account_list')
	
	def form_valid(self, form):
		new_password = form.cleaned_data.get('new_password')
		if new_password:
			self.object = form.save(commit=False)
			self.object.set_password(new_password)
			self.object.save()
		return super(AccountUpdate, self).form_valid(form)


class AccountDelete(LoginRequiredMixin, DeleteView):
	model = Account
	success_url = reverse_lazy('mail_account_list')

# Redirects

class RedirectList(LoginRequiredMixin, ListView):
	model = Redirect

class RedirectCreate(LoginRequiredMixin, CreateView):
	model = Redirect
	success_url = reverse_lazy('mail_redirect_list')

class RedirectUpdate(LoginRequiredMixin, UpdateView):
	model = Redirect
	fields = ['to']
	success_url = reverse_lazy('mail_redirect_list')

class RedirectDelete(LoginRequiredMixin, DeleteView):
	model = Redirect
	success_url = reverse_lazy('mail_redirect_list')


# core.io json export

def export(request):
	if request.GET.get('token', False) != settings.CORE_MAIL_TOKEN:
		raise PermissionDenied
	
	data = {}
	for domain in Domain.objects.all():
		data[unicode(domain)] = {
			"account": [],
			"alias":   [],
		}
		for account in domain.mail_accounts.all():
			data[unicode(domain)]["account"] += [{
				"name":     account.name,
				"password": account.password,
			}]
		for redirect in domain.redirect_set.all():
			data[unicode(domain)]["alias"] += [{
				"name": redirect.name,
				"to":   redirect.to,
			}]

	return HttpResponse(json.dumps(data), content_type='application/json')