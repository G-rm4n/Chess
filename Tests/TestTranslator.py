from Adapters.Translator import Translator

print("movimient not translated: (1125899906842624, 2251799813685248, 'K')")

print(f"movimiento translated: {Translator.translateMove((1125899906842624, 2251799813685248, 'K'))}")