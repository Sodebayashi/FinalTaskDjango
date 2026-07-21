from django.shortcuts import render
from django.views import generic
from .models import Player,Game
from .forms import SearchForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class IndexView(generic.ListView):
    model = Game
    template_name = 'players/index.html'
    context_object_name = "games"

class DetailView(generic.DetailView):
    model = Player
    template_name = 'players/detail.html'
    context_object_name = "player"

class GameDetailView(generic.DetailView):
    model = Game
    template_name = 'players/game_detail.html'
    context_object_name = "game"


class CreateView(generic.CreateView):
    model = Player
    fields = ['name', 'team', 'country', 'profile', 'achievement']
    template_name = 'players/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["game"] = get_object_or_404(Game, pk=self.kwargs["game_pk"])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.game = get_object_or_404(Game, pk=self.kwargs["game_pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'players:game_detail',
            kwargs={'pk': self.object.game.pk}
        )


def search(request, pk):
    game = get_object_or_404(Game, pk=pk)

    players = None
    searchform = SearchForm(request.GET)

    if searchform.is_valid():
        query = searchform.cleaned_data["words"]
        players = Player.objects.filter(
            game=game,
            name__icontains=query
        )

    return render(request, "players/results.html", {
        "game": game,
        "players": players,
        "searchform": searchform,
    })

class PlayerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Player
    template_name = "players/player_confirm_delete.html"
    success_url = reverse_lazy("players:index")

    def test_func(self):
        return self.request.user == self.get_object().author