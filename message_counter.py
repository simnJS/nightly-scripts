@nightyScript(
    name="Message Counter v1.0",
    author="simnJS",
    description="Count messages between a specific message ID and now for safe purging operations.",
    usage="<p>count <message_id>"
)
def MessageCounterScript():
    """
    MESSAGE COUNTER SCRIPT v1.0
    ---------------------------
    
    This script counts messages between a specific message ID and the current time.
    Perfect for calculating how many messages to purge without doing damage.
    
    COMMANDS:
    <p>count <message_id>  - Count messages in current channel
    <p>count <channel_id> <message_id>  - Count messages in specific channel
    <p>count <guild_id> <channel_id> <message_id>  - Count messages in specific guild/channel
    
    FEATURES:
    - Counts messages from a specific message to the most recent
    - Provides safe purge count calculation
    - Shows message details and timestamp information
    - Error handling for invalid message IDs
    - Works from any channel/server with proper IDs
    
    EXAMPLES:
    <p>count 1234567890123456789  - Count in current channel
    <p>count 987654321098765432 1234567890123456789  - Count in specific channel
    <p>count 111222333444555666 987654321098765432 1234567890123456789  - Count in specific server/channel
    
    USAGE SCENARIO:
    1. Find the message ID you want to purge FROM
    2. Use <p>count <message_id> to see how many messages would be affected
    3. Use the count for safe purging operations
    
    NOTES:
    - Only counts messages in the current channel
    - Includes the target message in the count
    - Provides timestamp information for verification
    
    CHANGELOG:
    v1.0 - Initial release
         - Message counting functionality
         - Timestamp and date information
         - Safe purge calculation
         - Error handling for invalid IDs
    """
    import discord
    from datetime import datetime, timezone
    
    async def send_embed_safely(channel_id, content, title):
        """Helper function to send embed while temporarily disabling private mode"""
        # Backup and disable private mode for embed
        current_private = getConfigData().get("private")
        updateConfigData("private", False)
        
        try:
            await forwardEmbedMethod(
                channel_id=channel_id,
                content=content,
                title=title
            )
        finally:
            updateConfigData("private", current_private)
    
    def format_timestamp(timestamp):
        """Format timestamp to readable date/time"""
        try:
            if isinstance(timestamp, datetime):
                dt = timestamp
            else:
                dt = datetime.fromisoformat(str(timestamp).replace('Z', '+00:00'))
            
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except:
            return "Unknown"
    
    def format_time_ago(timestamp):
        """Calculate and format how long ago a message was sent"""
        try:
            if isinstance(timestamp, datetime):
                dt = timestamp
            else:
                dt = datetime.fromisoformat(str(timestamp).replace('Z', '+00:00'))
            
            now = datetime.now(timezone.utc)
            diff = now - dt.replace(tzinfo=timezone.utc)
            
            days = diff.days
            hours, remainder = divmod(diff.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            if days > 0:
                return f"{days} day(s), {hours} hour(s) ago"
            elif hours > 0:
                return f"{hours} hour(s), {minutes} minute(s) ago"
            else:
                return f"{minutes} minute(s) ago"
        except:
            return "Unknown"

    @bot.command(name="count", usage="<message_id> OR <channel_id> <message_id> OR <guild_id> <channel_id> <message_id>", description="Count messages from message ID to now")
    async def count_messages(ctx, *, args: str = None):
        await ctx.message.delete()
        
        if not args:
            await send_embed_safely(
                ctx.channel.id,
                "❌ **Usage:**\n• `<p>count <message_id>` - Count in current channel\n• `<p>count <channel_id> <message_id>` - Count in specific channel\n• `<p>count <guild_id> <channel_id> <message_id>` - Count in specific server/channel\n• `<p>count help` - Show detailed help\n\n**Examples:**\n• `<p>count 1234567890123456789`\n• `<p>count 987654321098765432 1234567890123456789`\n• `<p>count 111222333444555666 987654321098765432 1234567890123456789`",
                "Message Counter"
            )
            return
        
        parts = args.strip().split()
        
        if len(parts) == 1 and parts[0].lower() in ["help", "?", "-h", "--help"]:
            await send_embed_safely(
                ctx.channel.id,
                """📚 **Message Counter - Detailed Help**

**🎯 Purpose:**
Count messages between a specific message ID and now for safe purging operations.

**📝 Command Formats:**

**1. Current Channel:**
`<p>count <message_id>`
• Counts messages in the channel where you run the command
• **Example:** `<p>count 1234567890123456789`

**2. Specific Channel:**
`<p>count <channel_id> <message_id>`
• Counts messages in any channel you have access to
• **Example:** `<p>count 987654321098765432 1234567890123456789`

**3. Specific Server/Channel:**
`<p>count <guild_id> <channel_id> <message_id>`
• Counts messages in any server/channel combination
• **Example:** `<p>count 111222333444555666 987654321098765432 1234567890123456789`

**🔍 How to get IDs:**
• **Message ID:** Right-click message → Copy ID (need Developer Mode)
• **Channel ID:** Right-click channel → Copy ID
• **Server ID:** Right-click server icon → Copy ID

**⚠️ What you get:**
• Number of messages after your target message
• Total messages to purge (including target)
• Message author and time information
• Safe count for bulk delete/purge commands

**💡 Pro Tips:**
• Always test with a small range first
• Discord bulk delete limit: 100 messages at once
• Messages older than 14 days can't be bulk deleted
• Use the "Total to purge" number for your purge command""",
                "Message Counter Help"
            )
            return
        
        if len(parts) == 1:
            message_id = parts[0]
            target_channel = ctx.channel
            location_info = f"current channel ({ctx.channel.name})"
        elif len(parts) == 2:
            channel_id, message_id = parts
            try:
                target_channel = bot.get_channel(int(channel_id))
                if not target_channel:
                    await send_embed_safely(
                        ctx.channel.id,
                        f"❌ **Channel not found.** Cannot access channel with ID `{channel_id}`. Make sure the bot has access to this channel.",
                        "Message Counter"
                    )
                    return
                location_info = f"channel #{target_channel.name} in {target_channel.guild.name}"
            except ValueError:
                await send_embed_safely(
                    ctx.channel.id,
                    "❌ **Invalid channel ID format.** Please provide a valid Discord channel ID (numeric).",
                    "Message Counter"
                )
                return
        elif len(parts) == 3:
            guild_id, channel_id, message_id = parts
            try:
                target_guild = bot.get_guild(int(guild_id))
                if not target_guild:
                    await send_embed_safely(
                        ctx.channel.id,
                        f"❌ **Server not found.** Cannot access server with ID `{guild_id}`. Make sure the bot is in this server.",
                        "Message Counter"
                    )
                    return
                target_channel = target_guild.get_channel(int(channel_id))
                if not target_channel:
                    await send_embed_safely(
                        ctx.channel.id,
                        f"❌ **Channel not found.** Cannot access channel with ID `{channel_id}` in server `{target_guild.name}`.",
                        "Message Counter"
                    )
                    return
                location_info = f"channel #{target_channel.name} in {target_guild.name}"
            except ValueError:
                await send_embed_safely(
                    ctx.channel.id,
                    "❌ **Invalid ID format.** Please provide valid Discord server and channel IDs (numeric).",
                    "Message Counter"
                )
                return
        else:
            await send_embed_safely(
                ctx.channel.id,
                "❌ **Invalid argument count.** Please use one of these formats:\n• `<p>count <message_id>`\n• `<p>count <channel_id> <message_id>`\n• `<p>count <guild_id> <channel_id> <message_id>`",
                "Message Counter"
            )
            return
        
        try:
            msg_id = int(message_id)
        except ValueError:
            await send_embed_safely(
                ctx.channel.id,
                "❌ **Invalid message ID format.** Please provide a valid Discord message ID (numeric).",
                "Message Counter"
            )
            return
        
        try:
            print(f"Counting messages from ID {message_id} to now in {location_info}", type_="INFO")
            
            try:
                target_message = await target_channel.fetch_message(msg_id)
                target_timestamp = target_message.created_at
                target_author = target_message.author.display_name
                target_content_preview = target_message.content[:50] + "..." if len(target_message.content) > 50 else target_message.content
                if not target_content_preview.strip():
                    target_content_preview = "[Attachment/Embed]"
            except discord.NotFound:
                await send_embed_safely(
                    ctx.channel.id,
                    f"❌ **Message not found.** The specified message ID doesn't exist in {location_info} or you don't have permission to access it.",
                    "Message Counter"
                )
                return
            except discord.Forbidden:
                await send_embed_safely(
                    ctx.channel.id,
                    f"❌ **Access denied.** You don't have permission to access the specified message in {location_info}.",
                    "Message Counter"
                )
                return
            
            message_count = 0
            async for message in target_channel.history(after=target_message, limit=None):
                message_count += 1
            
            total_purge_count = message_count + 1
            
            target_time_formatted = format_timestamp(target_timestamp)
            target_time_ago = format_time_ago(target_timestamp)
            current_time = format_timestamp(datetime.now(timezone.utc))
            
            content = f"""📊 **Message Count Results**

**Target Message:** `{message_id}` by {target_author}
**Location:** {location_info}
**Time:** {target_time_ago}

**📈 Count:**
• Messages after target: **{message_count:,}**
• **Total to purge: {total_purge_count:,}** (including target)

💡 Use `{total_purge_count}` for your purge command."""

            await send_embed_safely(
                ctx.channel.id,
                content,
                "Message Counter Results"
            )
            
            print(f"✅ Message count completed: {total_purge_count} messages to purge ({message_count} after target + 1 target)", type_="SUCCESS")
            
        except discord.HTTPException as e:
            await send_embed_safely(
                ctx.channel.id,
                f"❌ **Discord API Error:** {str(e)}\n\nThis might be due to rate limits or channel permissions.",
                "Message Counter"
            )
            print(f"Discord API error during message counting: {str(e)}", type_="ERROR")
            
        except Exception as e:
            await send_embed_safely(
                ctx.channel.id,
                f"❌ **Unexpected Error:** {str(e)}\n\nPlease try again or contact support if the issue persists.",
                "Message Counter"
            )
            print(f"Unexpected error during message counting: {str(e)}", type_="ERROR")

    print("✅ Message Counter script loaded successfully", type_="SUCCESS")

MessageCounterScript() 