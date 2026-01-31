from Bot_Engine import Bot
from Adapters.Bitboard import Bitboard
from Adapters.Translator import Translator

# Crear una posición de jaque simple: Rey negro en e8, reina blanca en e7
# Usar bitboards directamente

# Bitboards iniciales (simplificado)
# Para negro: Rey en e8 (bit 4 de fila 0)
# Para blanco: Reina en e7 (bit 4 de fila 1)

# Crear lista de bitboards (16 elementos: 6 piezas x 2 colores + otros)
bitboards = [0] * 15  # Ajustar según constants.py

# Asumir índices: 0-6 blanco, 7-13 negro, etc. (ver constants.py)
# indice 6 -> Bitboard de poscicion global de piezas blancas
# indice 13 -> Bitboard de poscicion global de piezas Negras
# BK = negro king, WQ = blanco queen
# Supongamos BK en índice 7 (rey negro), WQ en 5 (reina blanca)

# Posición: e8 = fila 0, col 4 -> bit 4
bitboards[7] = 1 << 4  # Rey negro en e8 (índice 7: KING + B)

# e7 = fila 1, col 4 -> bit 4 + 8 = 12
bitboards[5] = 1 << 12  # Reina blanca en e7 (índice 5: QUEEN + W)

# Setear bitboards ocupados
bitboards[6] = bitboards[5]  # Ocupado blanco (IDX_WHITE_BITBOARD=6)
bitboards[13] = bitboards[7]  # Ocupado negro (IDX_BLACK_BITBOARD=13)
bitboards[14] = bitboards[6] | bitboards[13]  # Total ocupado (IDX_OCCUPIED=14)

# Crear bot negro
bot = Bot.bot("B", "W", 4)

# Llamar alphaBetaSearch directamente
score = bot.alphaBetaSearch(0, bitboards, -10000, 10000)
print(f"Score en posición de jaque: {score}")
print(f"Mejor movimiento crudo: {bot.BestMovementFound}")

# Traducir el movimiento
if bot.BestMovementFound != 0:
    translated_move = Translator.translateMove(bot.BestMovementFound)
    print(f"Mejor movimiento traducido: {translated_move}")
else:
    print("No se encontró movimiento")

# Si score es ~9999, es mate detectado