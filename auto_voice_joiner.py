is_running = False
current_task = None
current_attempts = 0
start_time = None

# --- Configuration (in-memory only) ---
target_channel_id = ""
check_interval = 3
max_attempts = 50
debug_mode = False

@nightyScript(
    name="Auto Voice Channel Joiner v2.0",
    author="simnJS",
    description="Automatically joins voice channels when a free slot becomes available with advanced UI and logging.",
    usage="UI Script - Use the Auto Voice Joiner tab to configure and control the auto joiner"
)
def AutoVoiceJoinerScript():
    """
    AUTO VOICE CHANNEL JOINER SCRIPT
    --------------------------------
    
    This script automatically joins voice channels when a free slot becomes available.
    Features a modern UI for configuration and real-time monitoring.
    
    FEATURES:
    - Modern UI interface for easy configuration
    - Real-time status monitoring and logging
    - Detailed statistics tracking
    - Automatic retry with configurable limits
    - Smart channel validation and testing
    - Logs and stats are NOT persisted (in-memory only)
    
    SETUP:
    1. Open the Auto Voice Joiner tab in the UI
    2. Enter the target voice channel ID
    3. Configure check interval and max attempts
    4. Click "Start Auto Joiner" to begin
    
    The script will automatically:
    - Check for available slots at your specified interval
    - Attempt to join when space becomes available
    - Stop when successfully joined or max attempts reached
    - Log all activities with timestamps (in-memory only)
    - Track success/failure statistics (in-memory only)
    """
    import asyncio
    import time
    from datetime import datetime
    import threading

    global is_running, current_task, current_attempts, start_time
    global target_channel_id, check_interval, max_attempts, debug_mode

    def debug_log(message):
        if debug_mode:
            print(f"[AVJ Debug] {message}")

    def log_message(message, log_type="INFO"):
        # Affiche seulement les erreurs ou infos importantes
        if log_type == "ERROR" or debug_mode:
            print(f"[{log_type}] {message}")

    def get_channel_info(channel_id):
        try:
            channel = bot.get_channel(int(channel_id))
            if not channel:
                return None, "Channel not found"
            if not hasattr(channel, 'user_limit'):
                return None, "Not a voice channel"
            current_members = len(channel.members)
            user_limit = channel.user_limit
            server_name = channel.guild.name if hasattr(channel, 'guild') and channel.guild else "Unknown"
            return {
                "name": channel.name,
                "server": server_name,
                "current_members": current_members,
                "user_limit": user_limit,
                "has_space": user_limit == 0 or current_members < user_limit,
                "member_names": [member.display_name for member in channel.members[:5]]
            }, None
        except Exception as e:
            return None, f"Error: {str(e)}"

    def joiner_tick():
        global is_running
        if not is_running:
            return
        try:
            if not target_channel_id:
                log_message("No target channel configured", "ERROR")
                is_running = False
                return
            channel_info, error = get_channel_info(target_channel_id)
            if error:
                log_message(error, "ERROR")
                is_running = False
                return
            if channel_info["has_space"]:
                if join_voice_channel_sync():
                    log_message("Successfully joined - Auto Joiner completed")
                    is_running = False
                    return
            if is_running:
                timer = threading.Timer(check_interval, joiner_tick)
                timer.start()
        except Exception as e:
            log_message(f"Error in auto joiner: {str(e)}", "ERROR")
            if is_running:
                timer = threading.Timer(check_interval, joiner_tick)
                timer.start()

    def join_voice_channel_sync():
        try:
            channel = bot.get_channel(int(target_channel_id))
            if not channel:
                log_message(f"Channel {target_channel_id} not found", "ERROR")
                return False
            for vc in bot.voice_clients:
                if vc.channel and vc.channel.id == int(target_channel_id):
                    log_message(f"Already connected to {channel.name}")
                    is_running = False
                    return True
            try:
                future = asyncio.run_coroutine_threadsafe(channel.connect(), bot.loop)
                future.result(timeout=10)
                log_message(f"Successfully joined {channel.name}!")
                # Send DM to user
                try:
                    user = bot.user
                    if user:
                        # Get DM channel in a thread-safe way
                        if not user.dm_channel:
                            dm_channel_future = asyncio.run_coroutine_threadsafe(user.create_dm(), bot.loop)
                            dm_channel = dm_channel_future.result(timeout=10)
                        else:
                            dm_channel = user.dm_channel
                        embed_content = f"✅ Bot has joined the voice channel: **{channel.name}**"
                        embed_title = "Auto Voice Joiner"
                        future_embed = asyncio.run_coroutine_threadsafe(
                            forwardEmbedMethod(
                                channel_id=dm_channel.id,
                                content=embed_content,
                                title=embed_title
                            ),
                            bot.loop
                        )
                        future_embed.result(timeout=10)
                except Exception as dm_e:
                    log_message(f"Error while sending DM: {str(dm_e)}", "ERROR")
                return True
            except Exception as e:
                log_message(f"Failed to join voice channel: {str(e)}", "ERROR")
                return False
        except Exception as e:
            log_message(f"Failed to join voice channel: {str(e)}", "ERROR")
            return False

    def update_ui_status():
        try:
            if is_running:
                status_text.content = "🟢 Auto Joiner is running"
                status_text.color = "success"
            else:
                status_text.content = "🔴 Auto Joiner is stopped"
                status_text.color = "default"
            if target_channel_id:
                channel_info, error = get_channel_info(target_channel_id)
                if channel_info:
                    channel_status_text.content = f"Channel: #{channel_info['name']} in {channel_info['server']}"
                    channel_status_text.color = "default"
                else:
                    channel_status_text.content = f"Channel: {target_channel_id} (Error: {error})"
                    channel_status_text.color = "danger"
            else:
                channel_status_text.content = "Channel: None configured"
                channel_status_text.color = "muted"
        except Exception as e:
            debug_log(f"Error updating UI status: {e}")

    # --- UI creation (identique, mais on lit/écrit dans les variables locales/globales) ---
    try:
        avj_tab = Tab(name="Auto Voice Joiner", icon="mic", title="Auto Voice Joiner")
        main_container = avj_tab.create_container(type="columns")
        left_container = main_container.create_container(type="rows")
        config_card = left_container.create_card(gap=4)
        config_card.create_ui_element(
            UI.Text,
            content="🎤 Auto Voice Channel Joiner",
            size="lg"
        )
        config_card.create_ui_element(
            UI.Text,
            content="Automatically joins voice channels when a free slot becomes available",
            size="tiny"
        )
        channel_input = config_card.create_ui_element(
            UI.Input,
            label="Voice Channel ID",
            placeholder="Enter channel ID (e.g., 123456789)",
            value=target_channel_id,
            description="The voice channel you want to join automatically"
        )
        settings_group = config_card.create_group(type="columns", gap=4, vertical_align="center")
        interval_input = settings_group.create_ui_element(
            UI.Input,
            label="Check Interval (seconds)",
            placeholder="3",
            value=str(check_interval),
            description="How often to check for free slots"
        )
        button_group = config_card.create_group(type="columns", gap=4, vertical_align="center")
        start_button = button_group.create_ui_element(
            UI.Button,
            label="Start Auto Joiner",
            variant="solid"
        )
        stop_button = button_group.create_ui_element(
            UI.Button,
            label="Stop",
            variant="solid"
        )
        leave_button = button_group.create_ui_element(
            UI.Button,
            label="Leave Channel",
            variant="solid"
        )
        right_container = main_container.create_container(type="columns")
        status_card = right_container.create_card(gap=4)
        status_card.create_ui_element(
            UI.Text,
            content="Status & Activity",
            size="lg"
        )
        status_text = status_card.create_ui_element(
            UI.Text,
            content="🔴 Auto Joiner is stopped",
            size="base"
        )
        channel_status_text = status_card.create_ui_element(
            UI.Text,
            content="Channel: None configured",
            size="base"
        )
        def start_handler():
            global is_running, current_task, target_channel_id, check_interval
            try:
                if is_running:
                    avj_tab.toast(title="Already Running", description="Auto Voice Joiner is already running", type="INFO")
                    return
                channel_id = channel_input.value.strip()
                if not channel_id.isdigit():
                    avj_tab.toast(title="Error", description="Please enter a valid numeric voice channel ID", type="ERROR")
                    return
                channel_info, error = get_channel_info(channel_id)
                if error:
                    avj_tab.toast(title="Channel Error", description=error, type="ERROR")
                    return
                target_channel_id = channel_id
                is_running = True
                joiner_tick()
                update_ui_status()
                avj_tab.toast(title="Started", description=f"Auto Voice Joiner started for #{channel_info['name']}", type="SUCCESS")
            except Exception as e:
                avj_tab.toast(title="Error", description=f"Failed to start: {str(e)}", type="ERROR")
        def stop_handler():
            global is_running, current_task, current_attempts
            try:
                if not is_running:
                    avj_tab.toast(title="Not Running", description="Auto Voice Joiner is not currently running", type="INFO")
                    return
                is_running = False
                if current_task:
                    current_task.cancel()
                    current_task = None
                update_ui_status()
                avj_tab.toast(title="Stopped", description="Auto Voice Joiner has been stopped", type="INFO")
            except Exception as e:
                avj_tab.toast(title="Error", description=f"Error stopping: {str(e)}", type="ERROR")
        def leave_handler():
            try:
                channel = bot.get_channel(int(target_channel_id)) if target_channel_id else None
                if not channel:
                    avj_tab.toast(title="Error", description="No valid channel to leave", type="ERROR")
                    return
                for vc in bot.voice_clients:
                    if vc.channel and vc.channel.id == int(target_channel_id):
                        future = asyncio.run_coroutine_threadsafe(vc.disconnect(), bot.loop)
                        future.result(timeout=10)
                        avj_tab.toast(title="Left Channel", description=f"Bot has left {channel.name}", type="SUCCESS")
                        update_ui_status()
                        return
                avj_tab.toast(title="Not Connected", description="Bot is not connected to this channel", type="INFO")
            except Exception as e:
                avj_tab.toast(title="Error", description=f"Failed to leave channel: {str(e)}", type="ERROR")
        start_button.onClick = start_handler
        stop_button.onClick = stop_handler
        leave_button.onClick = leave_handler
        update_ui_status()
        status_card.create_ui_element(
            UI.Text,
            content="*Made by simnJS*",
            size="tiny"
        )
        avj_tab.render()
        log_message("✅ Auto Voice Joiner UI initialized successfully")
    except Exception as e:
        print(f"Error initializing Auto Voice Joiner UI: {e}", type_="ERROR")
        import traceback
        print(traceback.format_exc(), type_="ERROR")

AutoVoiceJoinerScript() 