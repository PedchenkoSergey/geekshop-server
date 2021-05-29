from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin


from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket
# Create your views here.


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'title': 'GeekShop - Авторизация', 'form': form}
    return render(request, 'authapp/login.html', context)


class RegisterCreateView(SuccessMessageMixin, CreateView):
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:profile')
    success_message = 'Вы успешно зарегистрировались!'

    def get_context_data(self, **kwargs):
        context = super(RegisterCreateView, self).get_context_data(**kwargs)
        context.update({'title': 'GeekShop - Регистрация'})
        return context


# def register(request):
#     if request.method == "POST":
#         form = UserRegisterForm(data=request.POST)
#
#         if form.is_valid() and form.clean_first_name():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрировались!')
#             return HttpResponseRedirect(reverse('users:login'))
#         else:
#             # Выводит ошибки по которым форма не проходит валидацию:
#             print(form.errors)
#     else:
#         form = UserRegisterForm()
#     context = {'title': 'GeekShop - Регистрация', 'form': form}
#     return render(request, 'authapp/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    # Первый способ:
    baskets = Basket.objects.filter(user=request.user)
    # total_quantity = 0
    # total_sum = 0
    # for basket in baskets:
    #     total_quantity += basket.quantity
    #     total_sum += basket.sum()

    # второй способ:
    # total_quantity = sum(basket.quantity for basket in baskets)
    # total_sum = sum(basket.sum() for basket in baskets)

    context = {
        'title': 'GeekShop- Личный кабинет',
        'form': form,
        'baskets': baskets,
        # Третий способ:
        # 'total_quantity': sum(basket.quantity for basket in baskets),
        # 'total_sum': sum(basket.sum() for basket in baskets),
    }
    return render(request, 'authapp/profile.html', context)
