
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

