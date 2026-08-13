import asyncio
import os

import discord
from asgiref.sync import sync_to_async
from discord.ext import commands
from dotenv import load_dotenv
from django.core.management.base import BaseCommand

from fights.models import Match

load_dotenv()


TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

notified_match_ids = set()

class Command(BaseCommand):
    help = "Starts the discord bot"
    def handle(self, *args, **options):
        if TOKEN is None:
            raise ValueError("DISCORD_TOKEN environment variable is not set")
        bot.run(TOKEN)
        self.stdout.write(self.style.SUCCESS("Successfully started discord bot"))

async def send_dm_to_user(user_id: int, message: str):
    user = bot.get_user(user_id) or await bot.fetch_user(user_id)
    if user is None:
        raise discord.NotFound(f"User not found: {user_id}")
    await user.send(message)
    return user

@sync_to_async
def get_next_match_info(player):
    """Get the next upcoming match for a player."""
    from django.db.models import Q
    
    upcoming_matches = Match.objects.filter(  # type: ignore
        Q(player1_id=player) | Q(player2_id=player),
        ~Q(match_state="complete")
    ).order_by("calculated_play_order")
    
    if not upcoming_matches.exists():
        return None
    
    next_match = upcoming_matches.first()
    opponent = next_match.player2_id if next_match.player1_id == player else next_match.player1_id
    
    match_info = "\n**Next Match:**\n"
    match_info += f"Match ID: {next_match.match_id}\n"
    if opponent:
        match_info += f"Opponent: {opponent.bot_name}\n"
    if next_match.estimated_start_time:
        match_info += f"Estimated Start: {next_match.estimated_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return match_info


@sync_to_async
def user_from_player(player):
    if player and getattr(player, "user_id", None):
        user = player.user
        social_account = user.socialaccount_set.filter(provider="discord").first()
        if getattr(social_account, "uid", None):
           return int(social_account.uid)
        else:
            extra_data = getattr(social_account, "extra_data", {}) or {}
            if extra_data.get("id"):
                return int(extra_data["id"])


# Find all complete matches that need to notify users
@sync_to_async
def get_completed_matches():
    completed_matches = (
        Match.objects.filter(  # type: ignore
            match_state="complete",
            updated_at__isnull=False            # updated_at__gte=timezone.now() - timedelta(seconds=300)
        )
        .exclude(match_id__in=notified_match_ids)
        .select_related("player1_id", "player1_id__user", "player2_id", "player2_id__user")
        .prefetch_related("player1_id__user__socialaccount_set", "player2_id__user__socialaccount_set")
        .order_by("updated_at")
    )

    return list(completed_matches)  # Convert to list to evaluate in sync context


async def monitor_completed_matches():
    while True:
        try:
            matches_to_notify = (
                await get_completed_matches()
            )

            for match in matches_to_notify:
                user1=await user_from_player(match.player1_id)
                user2=await user_from_player(match.player2_id)
                message = f"Your match {match.player1_id} vs {match.player2_id} has just finished."
                next_match1=await get_next_match_info(user1)
                next_match2=await get_next_match_info(user2)

                if user1:
                    await send_dm_to_user(user1,
                            message=message+(next_match1 or ""),
                        )
                if user2:
                    await send_dm_to_user(user2,
                            message=message+(next_match2 or ""),
                        )
                notified_match_ids.add(match.match_id)
        except Exception as exc:
            print(f"Error monitoring completed matches: {exc}")

        await asyncio.sleep(10)


@bot.event
async def on_ready():
    if bot.user is None:
        print("Error: bot.user is None")
        return
    print(f"Logged in as {bot.user} ({bot.user.id})")

    if CHANNEL_ID:
        channel = bot.get_channel(CHANNEL_ID)
        if channel is None:
            try:
                channel = await bot.fetch_channel(CHANNEL_ID)
            except discord.NotFound:
                print(f"Channel not found: {CHANNEL_ID}. The bot is not in that channel or the ID is invalid.")
            except discord.Forbidden:
                print(f"Channel found by ID, but the bot is forbidden from accessing channel {CHANNEL_ID}.")
            except discord.HTTPException as exc:
                print(f"Failed to fetch channel {CHANNEL_ID}: {exc}")

    if not getattr(bot, "_match_monitor_running", False):
        bot._match_monitor_running = True  # type: ignore
        asyncio.create_task(monitor_completed_matches())
