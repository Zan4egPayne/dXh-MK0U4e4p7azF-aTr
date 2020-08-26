from discord.ext import commands
import discord
 
from datebase.datebase import datebase as dt
 
 
class base( commands.Cog ):
 
    base = dt()
 
    def __init__( self, client ):
        self.client = client
 
    @commands.command()
    async def warn( self, ctx, member: discord.Member, guild: discord.Guild = None ):
        guild = ctx.guild if not guild else guild
 
        self.base.guild = guild.id
        self.base.user = member.id
        self.base.warn()
 
        await ctx.send( f"Успешно выдан варн пользователю { member.name }" )
 
    @commands.command()
    async def rep( self, ctx, member: discord.Member, guild: discord.Guild = None ):
        guild = ctx.guild if not guild else guild
 
        self.base.guild = guild.id
        self.base.user = member.id
        self.base.rep()
 
        await ctx.send( f"Успешно повышена репутация пользователю { member.name }" )
 
    @commands.command()
    async def search( self, ctx ):
        self.base.search()
 
        emb = discord.Embed( title = "Статистика репутаций и варнов" )
        emb.add_field( name = "id guild:", value = self.base.search1 )
        emb.add_field( name = "id user:", value = self.base.search2 )
        emb.add_field( name = "warns:", value = self.base.search3 )
        emb.add_field( name = "rep:", value = self.base.search4 )
 
        await ctx.send( embed = emb )
 
 
def setup( client ):
    client.add_cog( base( client ) ) 

