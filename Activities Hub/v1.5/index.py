import discord
from discord.ext import commands
import asyncio
import actividades
from variables import TOCKEN, IMAGENES
from time import sleep

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"I am {bot.user}")

    #Para mostrar los id de los canales
    # for guild in bot.guilds:
    #     print(f"Servidor: {guild.name}")
    # for channel in guild.channels:
    #     print(f"Canal: {channel.name}, ID: {channel.id}")


@bot.command()
async def start(ctx):
    print(f"Starting {bot.user}")

    await ctx.send("El bot está iniciando")
    # thread = threading.Thread(target=actividad, args=(ctx,))
    # thread.start()
    # asyncio.run_coroutine_threadsafe(actividad(), bot.loop)
    await bot.loop.create_task(actividad())


@bot.command()
async def ping(ctx):
    sleep(0.3)
    await ctx.send('Te pensas que voy a decir "pong"?')
    sleep(2.5)
    await ctx.send("Pues sí")
    sleep(0.7)
    await ctx.send("Pong")

@bot.command()
async def mention_role(ctx, role_name: str):
    # Obtener la lista de roles en el servidor
    roles = ctx.guild.roles
    role_names = [role.name for role in roles]
    
    # Verificar si el nombre del rol está en la lista de roles
    if role_name in role_names:
        # Buscar el rol por su nombre en el servidor
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        
        # Mencionar al rol en el mensaje
        await ctx.send(f"Mencionando al rol {role.mention}!")
    else:
        await ctx.send("El rol especificado no está presente en el servidor.")

@bot.event
async def actividad():
    channel_id = 1231010439933198362
    channel = bot.get_channel(channel_id)
    from datetime import datetime
    print(f"{datetime.now()}")
    
    await asyncio.sleep(actividades.tiempo_restante())
    actividad_en_curso = actividades.get_nombre()
    print("La actividad en curso es:", actividad_en_curso)
    
    role = discord.utils.get(channel.guild.roles, name='Conductor a prueba')
    
    embed = discord.Embed(
        title=f"{actividad_en_curso}",
        description=f"Se libera la actividad {actividad_en_curso}. Por favor realizarla cuanto antes.",
        color=discord.Color.dark_purple()
    )
    
    button = discord.ui.Button(label="Tomar actividad", style=discord.ButtonStyle.green)
    async def button_callback(interaction):
        # Grabar el nombre del usuario que presionó el botón
        embed.add_field(name="Actividad tomada por:", value=interaction.user.display_name, inline=False)
        
        # Actualizar el mensaje original para ocultar el botón
        await interaction.message.edit(embed=embed, view=None)
        await interaction.response.send_message("Tu nombre ha sido grabado.", ephemeral=True)

    button.callback = button_callback

    view = discord.ui.View()
    view.add_item(button)
    try:
        embed.set_image(url=IMAGENES[actividad_en_curso])
    except Exception as e:
        print("Ocurrió un error con la imagen", e)
    
    embed.set_author(name="ACTIVIDAD EN CURSO", icon_url="https://media.discordapp.net/attachments/1231010439735935046/1244733603393573037/png-transparent-computer-icons-user-uber-logo-logo-black-share-icon-Photoroom.png-Photoroom_1.png?ex=6658d301&is=66578181&hm=5c0ad87e4c57df7ffc318addb564cdd2d6d36cd6d15463be7d2a1b6c6212dba6&=&format=webp&quality=lossless")
    await channel.send(embed=embed, view=view)
    await channel.send(f"{role.mention}")
    await asyncio.sleep(60*60)
    await actividad()

@bot.command()
async def embed(ctx):
    

    embed = discord.Embed(
        title=f'Nombre_Actividad',
        description=f'Se libera la actividad Nombre_Actividad. Por favor realizarla cuanto antes.',
        color=discord.Color.blue()  # Puedes usar otros colores
    )
    
    # Añadir campos al embed
    # embed.add_field(name="Nombre_Actividad", value="Se libera la actividad Nombre_Actividad. Por favor realizarla cuanto antes", inline=False)
    
    # Añadir una imagen, thumbnail, footer y author
    # embed.set_thumbnail(url="https://example.com/thumbnail.jpg")
    embed.set_image(url="")
    # embed.set_footer(text="Este es el pie de página del embed")
    embed.set_author(name="ACTIVIDAD EN CURSO", icon_url="https://media.discordapp.net/attachments/1231010439735935046/1244733603393573037/png-transparent-computer-icons-user-uber-logo-logo-black-share-icon-Photoroom.png-Photoroom_1.png?ex=6658d301&is=66578181&hm=5c0ad87e4c57df7ffc318addb564cdd2d6d36cd6d15463be7d2a1b6c6212dba6&=&format=webp&quality=lossless")
    
    # Enviar el embed
    await ctx.send(embed=embed)

try:
    bot.run(TOCKEN)
except Exception as e:
    print(f"Exception: {e}")