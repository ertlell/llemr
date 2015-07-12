from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import resolve_url
from django.utils.decorators import available_attrs
from django.utils.six.moves.urllib.parse import urlparse
from django.http import HttpResponseRedirect


def provider_exists(user):
    print "Chekcing provider", hasattr(user, 'provider')
    return hasattr(user, 'provider')


def clintype_set(session):
    print "Checking clintype", 'clintype_pk' in session
    return 'clintype_pk' in session


def session_passes_test(test_func, fail_url,
                        redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the session passes the given test,
    redirecting to the choice page if necessary. The test should be a callable
    that takes the session object and returns True if the session passes. It's
    nearly a carbon copy of django.contrib.auth.decorators.user_passes_test.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.session):
                return view_func(request, *args, **kwargs)

            path = request.build_absolute_uri()
            resolved_url = resolve_url(fail_url)

            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.

            scheme, netloc = urlparse(resolved_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not scheme or scheme == current_scheme) and
                    (not netloc or netloc == current_netloc)):
                path = request.get_full_path()

            from django.contrib.auth.views import redirect_to_login
            print "next", path
            print "redirecting based on failed session", resolved_url
            print "redirect_field_name", redirect_field_name
            return redirect_to_login(
                path, resolved_url, redirect_field_name)

        return _wrapped_view
    return decorator


def provider_required(func):
    '''Provides composite multi-decorator support for the standard login
    procedure wrapping most views.'''

    func = session_passes_test(clintype_set,
                               fail_url=reverse_lazy('choose-clintype'))(func)

    func = user_passes_test(provider_exists,
                            login_url=reverse_lazy('new-provider'))(func)

    func = login_required(func)

    return func
