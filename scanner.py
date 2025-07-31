
import os
import asyncio


import time
from dotenv import load_dotenv
from telegram import Bot
from binance.client import Client
import pandas as pd

# Binance API anahtarı gerekmiyor, sadece public endpointler kullanılıyor
client = Client()

# .env dosyasını yükle
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
bot = Bot(token=BOT_TOKEN) if BOT_TOKEN else None

def get_futures_symbols():
    info = client.futures_exchange_info()
    symbols = [s['symbol'] for s in info['symbols'] if s['contractType'] == 'PERPETUAL' and s['quoteAsset'] == 'USDT']
    return symbols

def get_klines(symbol, interval='15m', limit=100):
    klines = client.futures_klines(symbol=symbol, interval='1h', limit=100)
    df = pd.DataFrame(klines, columns=[
        'open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
    return df

def heikin_ashi(df):
    ha_open = []
    ha_close = []
    ha_high = []
    ha_low = []
    for i in range(len(df)):
        o = df['open'].iloc[i]
        h = df['high'].iloc[i]
        l = df['low'].iloc[i]
        c = df['close'].iloc[i]
        close = (o + h + l + c) / 4
        if i == 0:
            open_ = (o + c) / 2
        else:
            open_ = (ha_open[i-1] + ha_close[i-1]) / 2
        high = max(h, open_, close)
        low = min(l, open_, close)
        ha_open.append(open_)
        ha_close.append(close)
        ha_high.append(high)
        ha_low.append(low)
    ha_df = pd.DataFrame({
        'open': ha_open,
        'high': ha_high,
        'low': ha_low,
        'close': ha_close
    }, index=df.index)
    return ha_df

def get_ha_color(row):
    return 'green' if row['close'] > row['open'] else 'red'

def analyze_symbol(symbol):
    df = get_klines(symbol)
    ha = heikin_ashi(df)
    ha['color'] = ha.apply(get_ha_color, axis=1)
    colors = ha['color'].tolist()
    # Son 2 HA mum kırmızı ve ondan önceki HA mum yeşil ise Short
    if len(colors) >= 3:
        if colors[-1] == 'red' and colors[-2] == 'red' and colors[-3] == 'green':
            return f"{symbol}: Short Sinyali 🔴"
        if colors[-1] == 'green' and colors[-2] == 'green' and colors[-3] == 'red':
            return f"{symbol}: Long Sinyali 🟢"
    return None





async def get_signals_for_telegram(send_to_channel=True, user_chat_id=None, user_bot=None, only_summary=False):
    symbols = get_futures_symbols()
    total_signals = 0
    signal_texts = []
    for symbol in symbols:
        try:
            result = analyze_symbol(symbol)
            if result:
                signal_texts.append(result)
                total_signals += 1
                # Sinyali Telegram kanalına gönder (sadece send_to_channel True ise)
                if send_to_channel and bot and CHANNEL_ID:
                    try:
                        await bot.send_message(chat_id=CHANNEL_ID, text=result)
                    except Exception as e:
                        pass
                # Eğer kullanıcıya tek tek mesaj gönderilecekse
                elif not send_to_channel and user_chat_id and user_bot:
                    try:
                        await user_bot.send_message(chat_id=user_chat_id, text=result)
                    except Exception:
                        pass
            await asyncio.sleep(0.1)
        except Exception:
            pass
    summary = f"Tarama tamamlandı ✅\nTaranan coin sayısı: {len(symbols)}\nBulunan sinyal sayısı: {total_signals}"
    # Eğer sadece özet mesajı isteniyorsa (handlers.py'dan çağrılırken)
    if only_summary == True:
        return summary
    # Eğer hem sinyaller anlık hem de en sonda özet mesajı isteniyorsa
    if only_summary == 'with_last' and not send_to_channel and user_chat_id and user_bot:
        await user_bot.send_message(chat_id=user_chat_id, text=summary)
        return None
    if not send_to_channel and user_chat_id is not None and user_bot is not None:
        return summary
    if signal_texts:
        return '\n'.join(signal_texts) + '\n' + summary
    else:
        return summary


# Ana fonksiyon: scanner.py doğrudan çalıştırıldığında sinyal sonuçlarını kanala gönderir
if __name__ == "__main__":
    async def main():
        result = await get_signals_for_telegram(send_to_channel=True)
        # Sonuçları ayrıca kanala topluca gönder
        if bot and CHANNEL_ID:
            try:
                await bot.send_message(chat_id=CHANNEL_ID, text="Sinyal Taraması Sonucu:\n" + result)
            except Exception:
                pass
        print(result)
    asyncio.run(main())

