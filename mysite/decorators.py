"""
from django.core.exceptions import PermissionDenied
from financ.models import Despesa
from functools import wraps

def user_financ(f):
	@wraps(f)
	def wrap(request, *args, **kwargs):        		
		despesa = Despesa.objects.get(pk=kwargs['pk'])
		if despesa.usuario == request.user:			
			return f(request, *args, **kwargs)
		else:
			raise PermissionDenied			
	return wrap
"""