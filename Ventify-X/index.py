import discord
from discord.ext import commands
from discord.ui import Button, View
import sqlite3
from dotenv import load_dotenv
import os
import re

from bd import select_query

intents = discord.Intents.default()
intents.members = True

load_dotenv()

TOKEN = os.getenv('TOKEN')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"I am {bot.user}\n")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if 'https://' in message.content or 'http://' in message.content:
        await message.channel.send(f"Link recibido: \n- Autor: {message.author.mention}\n- Link: {message.content}\n- Chat: {message.channel.mention}.")
        await message.delete()
        return
        
    await bot.process_commands(message)


@bot.command()
async def set_channel(ctx, channel_input):
    global channel
    try:
        if '#' in channel_input:
            channel = bot.get_channel(int(channel_input[2:-1]))
            await channel.send(f"Hola, aparezco")
            await ctx.send(f"Canal establecido -> {channel_input}")
    except Exception as e:
        print(f"Error -> {e}")
        await ctx.send(f"Por favor ingrese el chat correctamente")
    finally:
        return channel


@bot.event
async def on_member_join(member):
    sanciones = select_query('sanciones', 'sanciones', f'user_id = {member.id}')
    
    if channel:
        permitir_button = Button(label="Permitir", style=discord.ButtonStyle.green)
        banear_button = Button(label="Banear", style=discord.ButtonStyle.red)
        
        async def permitir_callback(interaction):
            await interaction.response.send_message(f"Permitiendo a {member.name} continuar.")
        
        async def banear_callback(interaction):
            await interaction.response.send_message(f"Banear a {member.name}.")
            await member.ban(reason="Límite de sanciones excedido.")
        
        permitir_button.callback = permitir_callback
        banear_button.callback = banear_callback
        
        view = View()
        view.add_item(permitir_button)
        view.add_item(banear_button)
        
        await channel.send(
            f"Se unió {member.name} y tiene {sanciones} sanciones.",
            view=view
        )

def user_id_from_mention(mention):
    match = re.match(r'<@!?(\d+)>', mention)
    if match:
        return int(match.group(1))
    else:
        return None

@bot.command()
async def add_sancion(user, razon):
    try:
        user_id = user_id_from_mention(user)
        conexion = sqlite3.connect('sanciones.db')
        cursor = conexion.cursor()

        cursor.execute("SELECT sanciones FROM sanciones WHERE user_id = ?", (user_id,))
        resultado = cursor.fetchone()

        if resultado:
            sanciones_actuales = resultado[0]
            nueva_sancion = sanciones_actuales + 1
            query = "UPDATE sanciones SET sanciones = ?, razon = ? WHERE user_id = ?"
            params = (nueva_sancion, razon, user_id)
            cursor.execute(query, params)
            await channel.send('Sanción añadida.')
        else:
            query = "INSERT INTO sanciones (user_id, sanciones, razon) VALUES (?, ?, ?)"
            params = (user_id, 1, razon)
            cursor.execute(query, params)
            await channel.send('Sanción añadida.')
        
        conexion.commit()

    except sqlite3.Error as error:
        await channel.send("Error al añadir o actualizar la sanción.")
        print("Error al añadir o actualizar la sanción:", error)
    finally:
        conexion.close()

@bot.command()
async def sanciones(mention):
    try:
        user_id = user_id_from_mention(mention)
        if not user_id:
            await channel.send("Error: Mención no válida.")
            print("Error: Mención no válida.")
            return
        
        resultado = select_query('sanciones', 'sanciones, razon', f'user_id = {user_id}')

        if resultado:
            await channel.send(f"Reporte de sanciones para el usuario {mention} (ID: {user_id}):")
            for i, sancion in enumerate(resultado, start=1):
                cantidad_sanciones = sancion[0]
                motivo = sancion[1]
                await channel.send(f"Sanción {i}: {cantidad_sanciones} sanciones - Motivo: {motivo}")
        else:
            await channel.send(f"No se encontraron sanciones para el usuario {mention}.")
        
    except Exception as e:
        print("Error al generar el reporte:", e)
        await channel.send("Error al generar el reporte")

try:
    bot.run(TOKEN)
except Exception as e:
    print(f"Exception: {e}")