from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from kumquat.utils import LoginRequiredMixin
from models import Account
from forms import AccountUpdateForm

class AccountList(LoginRequiredMixin, ListView):
	model = Account

class AccountCreate(LoginRequiredMixin, CreateView):
	model = Account
	success_url = reverse_lazy('ftp_account_list')
	
	def form_valid(self, form):
		password = form.cleaned_data.get('password')
		self.object = form.save(commit=False)
		self.object.set_password(password)
		self.object.save()
		return super(AccountCreate, self).form_valid(form)


class AccountUpdate(LoginRequiredMixin, UpdateView):
	model = Account
	form_class = AccountUpdateForm
	success_url = reverse_lazy('ftp_account_list')
	
	def form_valid(self, form):
		new_password = form.cleaned_data.get('new_password')
		if new_password:
			self.object = form.save(commit=False)
			self.object.set_password(new_password)
			self.object.save()
		return super(AccountUpdate, self).form_valid(form)


class AccountDelete(LoginRequiredMixin, DeleteView):
	model = Account
	success_url = reverse_lazy('ftp_account_list')