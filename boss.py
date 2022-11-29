from discord.ext import commands
from overkill import *

class MyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name='transformer', description="補償刀換算器的說明")
    async def tr_desc(self, context: commands.Context):
        await context.send(overkill.err_msg)

    @commands.command(name='tr', description="補償刀轉換器, time輸入補償刀秒數1~90秒, content輸入抄作業的原始內容", aliases=['TR', 'Tr'])
    async def tr(self, context: commands.Context):
        msg = context.message.content
        tr = re.match(r"<@\d+>\s*tr\s*(\d+)\s*\n([\s\S]+)", msg.lower())
        time = None
        content = None
        try:
            if tr:
                time = int(tr.group(1))
                if 1 <= time <= 90:
                    content = tr.group(2).split("\n")
                    await context.send(overkill.overkill_transformer(time, content))
                else:
                    raise
            else:
                raise
        except:
            await context.send(f"{overkill.err_msg}\n"
                               f"本次指令內取得剩餘秒數: {time}\n"
                               f"作業內容: {content}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MyCog(bot))
