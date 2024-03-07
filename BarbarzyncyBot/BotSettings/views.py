from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings as project_settings
from BotSettings.forms import BotTokenForm, ServerIDForm, ChannelsSettingsForm, RolesSettingsForm
from dotenv import dotenv_values
import discord
from asgiref.sync import async_to_sync
import os
   
from functools import partial



async def get_discord_servers_data(bot_token):
    intents = discord.Intents.default()
    intents.guilds = True
    client = discord.Client(intents=intents)
    data = {}
    @client.event
    async def on_ready():
        guilds = [(str(guild.id), guild.name) for guild in client.guilds]
        channels = {}
        categories = {}
        roles = {}
        for guild in client.guilds:
            channels[str(guild.id)] = [(str(channel.id), channel.name) for channel in guild.channels if isinstance(channel, discord.TextChannel)]
            categories[str(guild.id)] = [(str(category.id), category.name) for category in guild.categories]
            roles[str(guild.id)] = [(str(role.id), role.name) for role in guild.roles]
        data['guilds'] = guilds
        data['channels'] = channels
        data['categories'] = categories
        data['roles'] = roles
        await client.close()
        
    await client.start(bot_token)
    return data


async def get_from_request_or_function(request, key , func=None):
    if ret := request.session.get(key, None):
        return ret
    elif func:
        return await func()
    else:
        return None

def add_and_save_settings(settings, forms):
    for form in forms:
        if form.is_valid() and form.has_changed():
            for key, value in form.cleaned_data.items():
                settings[key] = value
            with open(project_settings.ENV_PATH, 'w') as env_file:
                for key, value in settings.items():
                    env_file.write(f'{key}={value}\n')
                    os.environ[key] = value


@login_required
@async_to_sync
async def bot_settings_view(request):
    context = {"is_authenticated": request.user.is_authenticated}

    settings = dotenv_values(project_settings.ENV_PATH)

    if request.method == 'POST':
        bot_token_form = BotTokenForm(request.POST, initial=settings)
        if bot_token_form.has_changed():
            add_and_save_settings(settings, [bot_token_form])
            if 'guilds_data' in request.session:
                del request.session['guilds_data']
    else:    
        bot_token_form = BotTokenForm(settings)


    if 'DISCORD_BOT_TOKEN' not in settings:
        context['forms'] = [BotTokenForm()]
        return render(request, 'bot_settings.html', context)

    guilds_data = None
    try:
        if 'DISCORD_BOT_TOKEN' in settings or request.method == 'POST':
            partial_get_discord_servers_data =  partial(get_discord_servers_data, settings['DISCORD_BOT_TOKEN'])
            guilds_data = await get_from_request_or_function(request, 'guilds_data', partial_get_discord_servers_data)
            if guilds_data:
                request.session['guilds_data'] = guilds_data
    except Exception as e:
        context['forms'] = [BotTokenForm()]
        context['error_message'] = e
        return render(request, 'bot_settings.html', context)

    if request.method == 'POST':
        server_id_form = ServerIDForm(request.POST, guilds=guilds_data['guilds'], initial=settings)
        if server_id_form.is_valid():
            guild_id=server_id_form.cleaned_data['GUILD_ID']
        else:
            context['forms'] = [bot_token_form, server_id_form]
            context['error_message'] = 'Zły serwer'
            return render(request, 'bot_settings.html', context)
        if server_id_form.is_valid() and server_id_form.has_changed():
            add_and_save_settings(settings, [server_id_form])
            channels_settings_form = ChannelsSettingsForm(settings, channels=guilds_data['channels'][guild_id], categories=guilds_data['categories'][guild_id])
            roles_settings_form = RolesSettingsForm(settings, roles=guilds_data['roles'][guild_id])
        elif server_id_form.is_valid():
            channels_settings_form = ChannelsSettingsForm(request.POST, channels=guilds_data['channels'][guild_id], categories=guilds_data['categories'][guild_id], initial=settings)
            roles_settings_form = RolesSettingsForm(request.POST, roles=guilds_data['roles'][guild_id], initial=settings)
            add_and_save_settings(settings, [channels_settings_form, roles_settings_form])

        
    else: 
        server_id_form = ServerIDForm(settings, guilds=guilds_data['guilds'])
        if 'GUILD_ID' in settings:
            channels_settings_form = ChannelsSettingsForm(settings, channels=guilds_data['channels'][settings['GUILD_ID']], categories=guilds_data['categories'][settings['GUILD_ID']])
            roles_settings_form = RolesSettingsForm(settings, roles=guilds_data['roles'][settings['GUILD_ID']])
    
    
    if not server_id_form.is_valid():
        context['forms'] = [bot_token_form, server_id_form]
        return render(request, 'bot_settings.html', context)
    else:
        context['forms'] = [bot_token_form, server_id_form, channels_settings_form, roles_settings_form]
        return render(request, 'bot_settings.html', context)