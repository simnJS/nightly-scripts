@nightyScript(
    name="Crypto Address Info v1.10",
    author="simnJS",
    description="Fetches information about cryptocurrency addresses.",
    usage="<p>cryptoinfo <currency> <address>"
)
def CryptoScript():
    """
    CRYPTO ADDRESS INFO SCRIPT
    --------------------------
    
    This script allows users to search for cryptocurrency address information using blockchain APIs.
    
    COMMANDS:
    <p>cryptoinfo <currency> <address>  - Search for a crypto address (BTC, LTC, ETH, etc.)
    
    SUPPORTED CURRENCIES:
    - BTC (Bitcoin)
    - LTC (Litecoin)
    - ETH (Ethereum)
    - BCH (Bitcoin Cash)
    - DOGE (Dogecoin)
    - DASH (Dash)
    - ZEC (Zcash)
    - BTS (BitShares)
    
    EXAMPLES:
    <p>cryptoinfo btc 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa  - Shows BTC address info
    <p>cryptoinfo eth 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6  - Shows ETH address info
    
    NOTES:
    - Supports multiple major cryptocurrencies
    - Clean and fast address information lookup
    
    API ENDPOINTS USED:
    - https://blockchain.info/rawaddr/{address} - For Bitcoin addresses
    - https://api.blockcypher.com/v1/{currency}/main/addrs/{address} - For other currencies
    
    CHANGELOG:
    v1.10 - Added EURO conversion ( Thanks to 1gz )

    v1.0 - Initial release
         - Support for BTC, LTC, ETH, BCH, DOGE
         - Balance and transaction information
         - Clean error handling and logging
    """
    import aiohttp
    import asyncio
    import json
    from datetime import datetime
    
    SUPPORTED_CURRENCIES = {
        "btc": {"name": "Bitcoin", "api": "blockchain", "divisor": 100000000},
        "ltc": {"name": "Litecoin", "api": "blockcypher", "divisor": 100000000},
        "eth": {"name": "Ethereum", "api": "blockcypher", "divisor": 1000000000000000000},
        "bch": {"name": "Bitcoin Cash", "api": "blockcypher", "divisor": 100000000},
        "doge": {"name": "Dogecoin", "api": "blockcypher", "divisor": 100000000},
        "dash": {"name": "Dash", "api": "blockcypher", "divisor": 100000000},
        "zec": {"name": "Zcash", "api": "blockcypher", "divisor": 100000000},
        "bts": {"name": "BitShares", "api": "blockcypher", "divisor": 100000000}
    }
    


    async def get_bitcoin_info(session, address):
        url = f"https://blockchain.info/rawaddr/{address}"
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "address": data.get("address", address),
                        "balance": data.get("final_balance", 0) / 100000000,
                        "total_received": data.get("total_received", 0) / 100000000,
                        "total_sent": data.get("total_sent", 0) / 100000000,
                        "n_tx": data.get("n_tx", 0),
                        "currency": "BTC"
                    }
                else:
                    print(f"Error fetching Bitcoin info: Status {response.status}", type_="ERROR")
                    return None
        except Exception as e:
            print(f"Error fetching Bitcoin info: {str(e)}", type_="ERROR")
            return None

    async def get_blockcypher_info(session, currency, address):
        url = f"https://api.blockcypher.com/v1/{currency}/main/addrs/{address}"
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    divisor = SUPPORTED_CURRENCIES[currency]["divisor"]
                    
                    return {
                        "address": data.get("address", address),
                        "balance": data.get("final_balance", 0) / divisor,
                        "total_received": data.get("total_received", 0) / divisor,
                        "total_sent": data.get("total_sent", 0) / divisor,
                        "n_tx": data.get("n_tx", 0),
                        "currency": currency.upper()
                    }
                else:
                    print(f"Error fetching {currency} info: Status {response.status}", type_="ERROR")
                    return None
        except Exception as e:
            print(f"Error fetching {currency} info: {str(e)}", type_="ERROR")
            return None

    async def get_eur_conversion_rate(session, currency_symbol):
        """Get EUR conversion rate for a cryptocurrency"""
        url = f"https://api.coingecko.com/api/v3/simple/price"
        
        coingecko_ids = {
            "BTC": "bitcoin",
            "LTC": "litecoin", 
            "ETH": "ethereum",
            "BCH": "bitcoin-cash",
            "DOGE": "dogecoin",
            "DASH": "dash",
            "ZEC": "zcash",
            "BTS": "bitshares"
        }
        
        currency_id = coingecko_ids.get(currency_symbol.upper())
        if not currency_id:
            return None
            
        params = {
            "ids": currency_id,
            "vs_currencies": "eur"
        }
        
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get(currency_id, {}).get("eur")
                else:
                    print(f"Error fetching EUR rate for {currency_symbol}: Status {response.status}", type_="WARNING")
                    return None
        except Exception as e:
            print(f"Error fetching EUR rate for {currency_symbol}: {str(e)}", type_="WARNING")
            return None



    @bot.command(name="cryptoinfo", usage="<currency> <address>", description="Fetches crypto address info")
    async def crypto_info(ctx, *, args: str):
        await ctx.message.delete()
        
        parts = args.strip().split()
        if len(parts) < 2:
            supported_list = ", ".join(SUPPORTED_CURRENCIES.keys()).upper()
            await forwardEmbedMethod(
                channel_id=ctx.channel.id,
                content=f"❌ **Usage:** `<p>cryptoinfo <currency> <address>`\n\n**Supported currencies:** {supported_list}",
                title="Crypto Address Info"
            )
            return
        
        currency = parts[0].lower()
        address = " ".join(parts[1:])
        
        if currency not in SUPPORTED_CURRENCIES:
            supported_list = ", ".join(SUPPORTED_CURRENCIES.keys()).upper()
            await forwardEmbedMethod(
                channel_id=ctx.channel.id,
                content=f"❌ **Unsupported currency:** {currency.upper()}\n\n**Supported currencies:** {supported_list}\n\n**Want more currencies?** Contact **simnJS_** on Discord!",
                title="Crypto Address Info"
            )
            return
        
        min_length = 20
        
        if len(address) < min_length:
            await forwardEmbedMethod(
                channel_id=ctx.channel.id,
                content="❌ **Invalid address format.** Please provide a valid cryptocurrency address.",
                title="Crypto Address Info"
            )
            return
        
        print(f"Looking up {currency.upper()} address: '{address}'", type_="INFO")
        
        msg = await ctx.send(f"Getting {SUPPORTED_CURRENCIES[currency]['name']} information for address '{address[:10]}...', please wait...")
        
        current_private = getConfigData().get("private")
        updateConfigData("private", False)
        
        try:
            async with aiohttp.ClientSession() as session:
                currency_config = SUPPORTED_CURRENCIES[currency]
                
                if currency == "btc":
                    address_data = await get_bitcoin_info(session, address)
                else:
                    address_data = await get_blockcypher_info(session, currency, address)
                
                if not address_data:
                    await forwardEmbedMethod(
                        channel_id=ctx.channel.id,
                        content=f"❌ **Failed to fetch information for {currency.upper()} address.**\n\nThis could mean:\n• The address doesn't exist\n• The address format is invalid\n• The API is temporarily unavailable.",
                        title="Crypto Address Info"
                    )
                    await msg.delete()
                    updateConfigData("private", current_private)
                    return
                

                
                currency_name = SUPPORTED_CURRENCIES[currency]['name']
                
                if currency in ["btc", "ltc", "bch", "doge", "dash", "zec", "bts"]:
                    precision = 8
                elif currency == "eth":
                    precision = 6
                else:
                    precision = 8
                
                balance = f"{address_data['balance']:.{precision}f}"
                total_received = f"{address_data['total_received']:.{precision}f}"
                total_sent = f"{address_data['total_sent']:.{precision}f}"
                
                eur_rate = await get_eur_conversion_rate(session, address_data['currency'])
                
                balance_eur = ""
                total_received_eur = ""
                total_sent_eur = ""
                
                if eur_rate:
                    if address_data['balance'] > 0:
                        balance_eur_value = address_data['balance'] * eur_rate
                        balance_eur = f" (≈ €{balance_eur_value:,.2f})"
                    
                    if address_data['total_received'] > 0:
                        received_eur_value = address_data['total_received'] * eur_rate
                        total_received_eur = f" (≈ €{received_eur_value:,.2f})"
                    
                    if address_data['total_sent'] > 0:
                        sent_eur_value = address_data['total_sent'] * eur_rate
                        total_sent_eur = f" (≈ €{sent_eur_value:,.2f})"
                
                content = f"""**Currency:** {currency_name} ({address_data['currency']})
**Address:** `{address_data['address']}`
**Current Balance:** {balance} {address_data['currency']}{balance_eur}
**Total Received:** {total_received} {address_data['currency']}{total_received_eur}
**Total Sent:** {total_sent} {address_data['currency']}{total_sent_eur}
**Number of Transactions:** **{address_data['n_tx']}**"""

                explorer_links = {
                    "btc": f"https://blockstream.info/address/{address_data['address']}",
                    "ltc": f"https://live.blockcypher.com/ltc/{address_data['address']}/",
                    "eth": f"https://etherscan.io/address/{address_data['address']}",
                    "bch": f"https://live.blockcypher.com/bch/{address_data['address']}/",
                    "doge": f"https://live.blockcypher.com/doge/{address_data['address']}/",
                    "dash": f"https://live.blockcypher.com/dash/{address_data['address']}/",
                    "zec": f"https://live.blockcypher.com/zec/{address_data['address']}/",
                    "bts": f"https://live.blockcypher.com/bts/{address_data['address']}/"
                }
                
                if currency in explorer_links:
                    content += f"\n\n**Blockchain Explorer:**\n• [View Address Details]({explorer_links[currency]})"
                
                await forwardEmbedMethod(
                    channel_id=ctx.channel.id,
                    content=content,
                    title="Crypto Address Info"
                )
            
            updateConfigData("private", current_private)
            await msg.delete()
            
        except Exception as e:
            print(f"Error in cryptoinfo command: {str(e)}", type_="ERROR")
            await forwardEmbedMethod(
                channel_id=ctx.channel.id,
                content=f"❌ **Error occurred: {str(e)}**",
                title="Crypto Address Info"
            )
            updateConfigData("private", current_private)
            await msg.delete()

CryptoScript()
