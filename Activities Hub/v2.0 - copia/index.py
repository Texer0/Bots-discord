import discord
from discord.ext import commands
import actividades
import asyncio
from variables import *
from time import sleep
from threading import Thread

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
user_choices = {}

@bot.event
@commands.has_permissions(manage_channels=True)
async def on_ready():
    print(f"I am {bot.user}\n")
    ctx =  bot.guilds[-1].channels[0]


@bot.command()
async def set_channel(ctx, channel_input):
    global channel
    try:
        if '#' in channel_input:
            channel = bot.get_channel(int(channel_input[2:-1]))
            # await channel.send(f"Hola, aparezco")
            await ctx.send(f"Canal establecido -> {channel_input}")
    except Exception as e:
        print(f"Error -> {e}")
        await ctx.send(f"Error, por favor ingrese un chat correctamente, ejemplo: #general")
    finally:
        return channel

@bot.command()
async def activity_time(ctx):
    tiempo_de_espera = actividades.tiempo_restante()
    await ctx.send(f"Tiempo restante: {int(tiempo_de_espera/60)} minutos")

@bot.command()
async def setup(ctx):
    embed = discord.Embed(
    title=f"Setup",
    description=f"Elija el idioma\nChoice the language",
    color=discord.Color.dark_purple()
    )
    
    emoji="✔"
    button_english = discord.ui.Button(label="English", style=discord.ButtonStyle.green, emoji=emoji)
    
    async def button_english_callback(interaction):

        await interaction.message.edit(embed=embed, view=None)
        await interaction.response.send_message("You chose English.", ephemeral=True)
        await select_language.callback(ctx, idioma='english')
        
    button_spanish = discord.ui.Button(label="Español", style=discord.ButtonStyle.blurple, emoji=emoji)
    
    async def button_spanish_callback(interaction):

        await interaction.message.edit(embed=embed, view=None)
        await interaction.response.send_message("Elegiste español.", ephemeral=True)
        await select_language.callback(ctx, idioma='spanish')

    button_english.callback = button_english_callback
    button_spanish.callback = button_spanish_callback

    view = discord.ui.View()
    view.add_item(button_spanish)
    view.add_item(button_english)
    mensaje = await ctx.send(embed=embed, view=view)
    
@bot.command()
async def select_language(ctx, idioma):
    if idioma == 'spanish':
        await ctx.send("Por favor seleccione el canal en el que desplegar las notificaciones de la siguiente manera: !set_channel #nombre_canal")
        sleep(10)
        # await ctx.send("Ahora seleccione el canal de logs de la siguiente manera: !set_channel_logs #nombre_canal")
        await setup_spanish(ctx)
    elif idioma == 'english':
        await setup_english(ctx)


async def setup_spanish(ctx):
    embed = discord.Embed(
    title=f"Inicialización",
    description=f"Seleccione la organización",
    color=discord.Color.dark_purple()
    )
    
    options = [
        discord.SelectOption(label="Transporte"),
        discord.SelectOption(label="Mecanico"),
        discord.SelectOption(label="Seguridad")
    ]
    
    select_spanish = discord.ui.Select(placeholder="Elige una opción...", options=options)

    async def select_spanish_callback(interaction):

        selected_option = interaction.data['values'][0]
        user_choices[interaction.user.id] = selected_option

        embed.add_field(name="Opción seleccionada", value=selected_option, inline=False)

        await interaction.message.edit(embed=embed, view=None)
        await interaction.response.send_message(f"Tu opción ha sido guardada: {selected_option}", ephemeral=True)
        actividades.selection_org(selected_option)
        try:
            await rol_question(ctx, selected_option)
        except Exception as e:
            print(f"Error -> {e}")

    select_spanish.callback = select_spanish_callback
    view = discord.ui.View()
    view.add_item(select_spanish)
    await ctx.send(embed=embed, view=view)


@bot.command()
async def mention_rol_in_text(ctx):
    roles = ctx.guild.roles
    roles_nombres = [role.name for role in roles if role.name != "@everyone"]

    opciones = "\n".join([f"{i}. {role}" for i, role in enumerate(roles_nombres, start=1)])
    

    await ctx.send(f"Elige un rol escribiendo su número:\n{opciones}")

    def check(m):
        return m.author == ctx.message.author and m.channel == ctx.message.channel

    try:
        respuesta = await bot.wait_for('message', check=check, timeout=30)
        eleccion = int(respuesta.content)
        if 0 < eleccion <= len(roles_nombres):
            await returns_role(ctx, roles_nombres[eleccion - 1])
        else:
            await ctx.send("Esa no es una opción válida.")
    except (ValueError, asyncio.TimeoutError):
        await ctx.send("Se ha agotado el tiempo de espera o la entrada no es válida. Intenta de nuevo.")

async def returns_role(ctx, rol_elegido):
    role = discord.utils.get(ctx.guild.roles, name=rol_elegido)
    if role:
        await ctx.send(f"Mencionando el rol {role.mention}")
        return role


async def rol_question(ctx, option):
    "Sends an embed message for question what rol to mention at every activity"
    embed = discord.Embed(
        title=f"Seleccione el rol a mencionar",
        description=f"para cada actividad",
        color=discord.Color.dark_purple()
    )

    roles = ctx.guild.roles
    roles_nombres = [role.name for role in roles if role.name != "@everyone"]

    options = [discord.SelectOption(label=rol) for rol in roles_nombres[:25] if rol]

    select_rol = discord.ui.Select(placeholder="Elige un rol...", options=options)

    async def select_rol_callback(interaction):
        selected_option = interaction.data['values'][0]
        await interaction.response.send_message(f"Rol seleccionado: {selected_option}", ephemeral=True)
        role = discord.utils.get(ctx.guild.roles, name=selected_option)
        print("\nLas variables son:", ctx, type(ctx), option, type(option), role, type(role))
        act_thread = Thread(target= function_async, args= (ctx, option, role))
        act_thread.start()
        pass
        
    def function_async(*args):
        async def executioner():
            try:
                print(args)
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_forever(await message_act.callback(args[0], args[1], args[2]))
            except Exception as e:
                print(f"Error -> {e}")
        asyncio.run(executioner())

    select_rol.callback = select_rol_callback

    view = discord.ui.View()
    view.add_item(select_rol)

    await ctx.send(embed=embed, view=view)

@bot.command()
async def setup_english(ctx):
    pass
  
@bot.command()
async def ping(ctx):
    sleep(0.3)
    await ctx.send('Te pensas que voy a decir "pong"?')
    sleep(2.5)
    await ctx.send("Pues sí")
    sleep(0.7)
    await ctx.send("Pong")

@bot.command()
async def mention(ctx, role_name: str, confirmacion=1):
    print(confirmacion)
    roles = ctx.guild.roles
    role_names = [role.name for role in roles]
    
    if role_name in role_names:
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if confirmacion == 1:
            await channel.send(f"Mencionando al rol {role.mention}!")
        return role
    else:
        await ctx.send("El rol especificado no está presente en el servidor.")
        await ctx.send("Los roles en el servidor son:")

        text = f""
        for rol in role_names:
            text = text + rol + "\n"
        await ctx.send(text[1:])

@bot.command()
async def message_act(ctx, option, rol):
    horas_faltantes = actividades.tiempo_restante()
    await ctx.send(f"Tiempo restante: {int(horas_faltantes/60)} minutos")
    while horas_faltantes > 0:
        await asyncio.sleep(7)
    
    actividad_en_curso = actividades.get_nombre(option)
    print("La actividad en curso es:", actividad_en_curso)
    await returns_role(ctx, rol)
    
    embed = discord.Embed(
        title=f"{actividad_en_curso}",
        description=f"Se libera la actividad {actividad_en_curso.lower()}. Por favor realizarla cuanto antes",
        color=discord.Color.dark_purple()
    )
    
    button = discord.ui.Button(label="Tomar actividad", style=discord.ButtonStyle.green)
    async def button_callback(interaction):
        try:
            embed.add_field(name="Actividad tomada por:", value=interaction.user.display_name, inline=False)

            await interaction.message.edit(embed=embed, view=None)
            await interaction.response.send_message("Tu nombre ha sido grabado.", ephemeral=True)
        except Exception as e:
            print(f"Error -> {e}")
        await ctx.send(f'Actividad: {actividad_en_curso.lower()} tomada por {interaction.user.display_name}')

    button.callback = button_callback

    view = discord.ui.View()
    view.add_item(button)

    if option == 'Mecanico':
        imagen = IMAGENES_MECANICO
    elif option == 'Transporte':
        imagen = IMAGENES_TRANSPORTE
    elif option == 'Seguridad':
        imagen = IMAGENES_SEGURIDAD
        
    embed.set_image(url=imagen[actividad_en_curso])

    embed.set_author(name="ACTIVIDAD EN CURSO", icon_url="https://media.discordapp.net/attachments/1231010439735935046/1244733603393573037/png-transparent-computer-icons-user-uber-logo-logo-black-share-icon-Photoroom.png-Photoroom_1.png?ex=6658d301&is=66578181&hm=5c0ad87e4c57df7ffc318addb564cdd2d6d36cd6d15463be7d2a1b6c6212dba6&=&format=webp&quality=lossless")
    
    
    await channel.send(embed=embed, view=view)
    await channel.send(f"{rol.mention}")


try:
    bot.run(TOKEN)
except Exception as e:
    print(f"Exception: {e}")


"""
TODO: in order
Documentation
Setup in english
"""