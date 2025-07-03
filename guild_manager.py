guild_data = {}
is_loading = False

@nightyScript(
    name="Guilds Manager v1.0",
    author="simnJS",
    description="Discord server management interface with visual guild listing and leave functionality.",
    usage="UI Script - Use the Guild Manager tab to view and leave servers"
)
def GuildManagerScript():
    """
    GUILDS MANAGER SCRIPT v1.0
    --------------------------
    
    Discord server management interface for viewing and leaving servers.
    Displays all joined Discord servers in an organized two-column layout
    with individual Leave buttons for each server.
    
    FEATURES:
    - Visual server listing with server names and icons
    - Leave servers with one click
    - Toast notifications for feedback
    - Automatic interface updates
    - Alphabetically sorted server list
    
    USAGE:
    Access the "Guilds Manager" tab in Nighty to:
    • View all servers the bot is connected to
    • Click "Leave" next to any server to disconnect
    • Get instant feedback through notifications
    
    NOTES:
    - Interface automatically refreshes after leaving servers
    - Leave operations are safe and include error handling
    - Supports any number of servers with scroll functionality
    
    CHANGELOG:
    v1.0 - Initial release
         - Complete guild management interface
         - Leave functionality with notifications
         - Two-column layout with server cards
    """
    import asyncio

    global guild_data, is_loading

    def debug_log(message):
        print(f"[Guild Manager Debug] {message}")

    def log_message(message, level="INFO"):
        print(f"[{level}] {message}")

    def leave_guild_sync(guild_id):
        """Leave a guild synchronously"""
        try:
            guild = bot.get_guild(int(guild_id))
            if not guild:
                return False, "Guild not found"
            name = guild.name
            future = asyncio.run_coroutine_threadsafe(guild.leave(), bot.loop)
            future.result(timeout=10)
            guild_data.pop(guild_id, None)
            return True, name
        except Exception as e:
            return False, str(e)

    def leave_guild_handler(guild_id):
        """Handler to leave a specific guild"""
        success, result = leave_guild_sync(guild_id)
        if success:
            gm_tab.toast(
                title="Left Server",
                description=f"You have left {result}",
                type="SUCCESS"
            )
            load_guild_data()
        else:
            gm_tab.toast(
                title="Error",
                description=f"Failed to leave server: {result}",
                type="ERROR"
            )

    def make_leave_handler(guild_id):
        """Create a unique handler with __name__ defined"""
        def handler():
            leave_guild_handler(guild_id)
        handler.__name__ = f"leave_handler_{guild_id}"
        return handler

    def initialize_ui():
        """Initialize or reset the Tab and main container"""
        nonlocal gm_tab, main_container
        gm_tab = Tab(name="Guilds Manager", icon="preferences", title="Guilds Manager")
        main_container = gm_tab.create_container(
            type="rows",
            gap=4,
            height="auto",
            width="full",
            vertical_align="start",
            overflow="auto"
        )

    def load_guild_data():
        """Load guild data and create cards in pairs"""
        global guild_data, is_loading
        if is_loading:
            return
        is_loading = True
        guild_data.clear()

        try:
            initialize_ui()

            guilds = sorted(bot.guilds, key=lambda g: g.name.lower())
            for i in range(0, len(guilds), 2):
                pair = guilds[i:i+2]
                row_container = main_container.create_container(
                    type="columns",
                    gap=4,
                    horizontal_align="start",
                    vertical_align="start"
                )
                for guild in pair:
                    current_guild_id = guild.id
                    current_guild_name = guild.name
                    guild_data[current_guild_id] = {
                        "name": current_guild_name,
                        "guild_object": guild
                    }

                    guild_card = row_container.create_card(gap=4)

                    header_group = guild_card.create_group(
                        type="columns",
                        gap=2,
                        vertical_align="center"
                    )
                    header_group.create_ui_element(
                        UI.Text,
                        content=f"🏛️ {current_guild_name}",
                        size="lg",
                        full_width=True
                    )
                    header_group.create_ui_element(
                        UI.Button,
                        label="Leave",
                        variant="solid",
                        color="danger",
                        onClick=make_leave_handler(current_guild_id)
                    )

        except Exception as e:
            log_message(f"Error loading guilds: {e}", "ERROR")
        finally:
            is_loading = False
            gm_tab.render()

    try:
        main_container = None
        gm_tab = None
        load_guild_data()
        log_message("✅ Guild Manager UI initialized successfully")
    except Exception as e:
        print(f"Initialization error: {e}", type_="ERROR")

GuildManagerScript()
