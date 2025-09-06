from django.core.management.base import BaseCommand
from social.models import SocialProfile
from django.contrib.auth import get_user_model

User = get_user_model()


BOT_PERSONAS = [
  {
    "username": "HODLOrBust",
    "persona_name": "Crypto Believer",
    "personality": "Crypto enthusiast"
  },
  {
    "username": "KeynesWasRight",
    "persona_name": "Dr Doubtcoin",
    "personality": "Crypto skeptic economist"
  },
  {
    "username": "ChefSupreme99",
    "persona_name": "Chef Magnifique",
    "personality": "Professional chef with high self-esteem"
  },
  {
    "username": "SaltyCommenter",
    "persona_name": "Flame Thrower",
    "personality": "Internet Troll"
  },
  {
    "username": "FinalBossSlayer",
    "persona_name": "Pixel Paladin",
    "personality": "Videogame nerd"
  },
  {
    "username": "PanelByPanel",
    "persona_name": "ComicLoreKeeper",
    "personality": "Comic book nerd"
  },
  {
    "username": "SnackHackDaily",
    "persona_name": "QuickBites HQ",
    "personality": "Social Media Page with easy recipes"
  },
  {
    "username": "LegacyCoder",
    "persona_name": "Skeptical Engr",
    "personality": "AI skeptic software engineer"
  },
  {
    "username": "NeuralDreamer",
    "persona_name": "Code Prophet",
    "personality": "Vibe coder who adores AI, tries to implement it everywhere"
  },
  {
    "username": "StonksGuru",
    "persona_name": "Chart Whisperer",
    "personality": "Day trader who thinks they cracked the stock market"
  },
  {
    "username": "CinephileCritic",
    "persona_name": "FrameByFrame",
    "personality": "Film buff who analyzes every scene"
  },
  {
    "username": "EcoWarrior101",
    "persona_name": "Green Crusader",
    "personality": "Climate activist passionate about sustainability"
  },
  {
    "username": "MemeArchivist",
    "persona_name": "Meme Keeper",
    "personality": "Meme historian who tracks origins of memes"
  },
  {
    "username": "HistoryNerd42",
    "persona_name": "Past Explainer",
    "personality": "History buff who over-explains historical context"
  },
  {
    "username": "ZenGardener",
    "persona_name": "Bloom Sage",
    "personality": "Nature-loving hobbyist gardener with a peaceful vibe"
  },
  {
    "username": "SportsHotTake",
    "persona_name": "Couch Coach",
    "personality": "Overconfident sports fan who argues online"
  },
  {
    "username": "DIYDisaster",
    "persona_name": "Captain DuctTape",
    "personality": "Home improvement enthusiast who always messes things up"
  },
  {
    "username": "BookDragon",
    "persona_name": "Page Hoarder",
    "personality": "Voracious reader who hoards books"
  }
]


class Command(BaseCommand):
    help = "Create bot users"

    def handle(self, *args, **kwargs):
        for persona in BOT_PERSONAS:
            if not User.objects.filter(username=persona["username"]).exists():
                user = User.objects.create_user(
                    username=persona["username"],
                    password="botpassword123",
                    email=f"{persona['username']}@bots.local"
                )
                SocialProfile.objects.create(
                    account=user,
                    display_name=persona["persona_name"],
                    bot_personality=persona["personality"],
                )
                self.stdout.write(self.style.SUCCESS(f"Created bot {persona['username']}"))
