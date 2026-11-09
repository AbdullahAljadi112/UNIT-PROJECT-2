
import json
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.shortcuts import render


def load_data():

    file_path = settings.BASE_DIR / "esports" / "data" / "content.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def home(request):

    data = load_data()

    context = {
        "featured_games": data["featured_games"],
        "featured_tournaments": data["featured_tournaments"],
        "featured_teams": data["featured_teams"],
        "featured_players": data["featured_players"],
        "featured_achievements": data["featured_achievements"],
    }

    return render(request, "esports/home.html", context)


def tournaments(request):

    data = load_data()

    all_tournaments = data.get("featured_tournaments", [])

    search_query = request.GET.get("search", "").strip()
    selected_status = request.GET.get("status", "").strip()

    filtered_tournaments = all_tournaments

    if search_query:
        filtered_tournaments = [
            tournament
            for tournament in filtered_tournaments
            if search_query.lower() in tournament["name"].lower()
            or search_query.lower() in tournament["description"].lower()
            or search_query.lower() in tournament["game"]["name"].lower()
        ]

    if selected_status:
        filtered_tournaments = [
            tournament
            for tournament in filtered_tournaments
            if tournament["status"] == selected_status
        ]

    context = {
        "tournaments": filtered_tournaments,
        "search_query": search_query,
        "selected_status": selected_status,
    }

    return render(
        request,
        "esports/tournaments.html",
        context
    )

@require_POST
def toggle_theme(request):

    current_theme = request.COOKIES.get("saudiArenaTheme", "dark")

    new_theme = "light" if current_theme == "dark" else "dark"

    next_url = request.POST.get("next", "/")

    if not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure()
    ):
        next_url = "/"

    response = redirect(next_url)

    response.set_cookie(
        key="saudiArenaTheme",
        value=new_theme,
        max_age=31536000,
        path="/",
        httponly=True,
        secure=request.is_secure(),
        samesite="Lax"
    )

    return response



def teams(request):
    data = load_data()

    all_teams = data.get("featured_teams", [])
    search_query = request.GET.get("search", "").strip()

    filtered_teams = all_teams

    if search_query:
        filtered_teams = [
            team for team in all_teams
            if search_query.lower() in team["name"].lower()
            or search_query.lower() in team["description"].lower()
        ]

    context = {
        "teams": filtered_teams,
        "search_query": search_query,
        "total_teams": len(filtered_teams),
        "teams_page": data.get("teams_page", {}),
    }

    return render(request, "esports/teams.html", context)


def about(request):

    data = load_data()

    context = {
        "about": data.get("about", {})
    }

    return render(
        request,
        "esports/about.html",
        context
    )

def players(request):
    data = load_data()

    context = {
        "players": data.get("featured_players", [])
    }

    return render(request, "esports/players.html", context)


def games(request):
    data = load_data()

    context = {
        "games": data.get("featured_games", [])
    }

    return render(request, "esports/games.html", context)


def achievements(request):
    data = load_data()

    context = {
        "achievements": data.get("featured_achievements", [])
    }

    return render(request, "esports/achievements.html", context)

from django.http import Http404


def player_detail(request, slug):
    data = load_data()

    players = data.get("featured_players", [])

    player = next(
        (
            item for item in players
            if item.get("slug") == slug
        ),
        None
    )

    if player is None:
        raise Http404("Player not found")

    context = {
        "player": player
    }

    return render(
        request,
        "esports/player_detail.html",
        context
    )


