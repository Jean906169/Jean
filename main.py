from telethon import TelegramClient, events
import asyncio

api_id = 32111151
api_hash = "796d4ebf9ce44b431e804fe40d973f3a"
phone = "+51914811926"

GRUPO_ID = -1004429497986
BOT_USERNAME = "@OVIDATA_BOT"

COMANDOS_EXCLUIDOS = ["/cmds", "/start", "/me"]

client = TelegramClient("azulito_session", api_id, api_hash)

@client.on(events.NewMessage(chats=GRUPO_ID))
async def handler(event):
    msg = event.message
    if not msg.text or not msg.text.startswith('/'):
        return

    comando = msg.text.lower().split()[0]  
    if comando in [c.lower() for c in COMANDOS_EXCLUIDOS]:  
        print(f"⏭️ Excluido: {msg.text}")  
        return  

    me = await client.get_me()  
    if msg.sender_id == me.id:  
        return  

    print(f"🔄 Comando: {msg.text} → Iniciando cuenta regresiva...")  

    # Mensaje inicial
    espera_msg = await client.send_message(  
        GRUPO_ID,   
        "⏳ Extrayendo información, espera por favor... (15s)",   
        reply_to=msg.id  
    )  

    try:  
        bot_msg = await client.send_message(BOT_USERNAME, msg.text)  
        
        # ⏱️ CUENTA REGRESIVA DINÁMICA (15 segundos)
        for tiempo_restante in range(14, -1, -1):
            await asyncio.sleep(1)
            try:
                # Actualiza el mensaje con los segundos que quedan
                await client.edit_message(
                    GRUPO_ID, 
                    espera_msg.id, 
                    f"⏳ Extrayendo información, espera por favor... ({tiempo_restante}s)"
                )
            except Exception:
                # Si falla la edición (por límites de Telegram), continúa para no romper el flujo
                pass
        
        count = 0  
        last_id = bot_msg.id  
        
        # Revisión adicional de 5 segundos
        for _ in range(6):    
            async for resp in client.iter_messages(BOT_USERNAME, limit=10):  
                if resp.id > last_id:  
                    try:  
                        if resp.photo or resp.document or resp.video:  
                            await client.send_file(  
                                GRUPO_ID,   
                                resp.media,   
                                caption=resp.message or "",  
                                reply_to=msg.id  
                            )  
                        else:  
                            await client.send_message(  
                                GRUPO_ID,   
                                resp.message or "",  
                                reply_to=msg.id  
                            )  
                        count += 1  
                        last_id = resp.id  
                        await asyncio.sleep(0.7)  
                    except:  
                        await client.forward_messages(GRUPO_ID, resp)  
            
            await asyncio.sleep(1)
        
        # Eliminar mensaje de espera al terminar
        await client.delete_messages(GRUPO_ID, espera_msg.id)  
        print(f"✅ Reenviado completo ({count} mensajes)")  
        
    except Exception as e:  
        print(f"❌ Error: {e}")  
        try:  
            await client.edit_message(GRUPO_ID, espera_msg.id, "❌ Error al procesar el comando.")  
        except:  
            pass

async def main():
    while True:
        try:
            await client.start(phone=phone)
            print("🚀 PROXY 15 SEGUNDOS + CUENTA REGRESIVA ACTIVADA")
            await client.run_until_disconnected()
        except Exception as e:
            print(f"Reconectando... {e}")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())
