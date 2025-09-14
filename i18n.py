import json
import os

class I18n:
    def __init__(self):
        self.current_language = 'en'  # Lingua predefinita: inglese
        self.translations = {
            'en': {
                # Menu principale
                'game_title': '★ Space Shooter ★',
                'start_game': 'Start Game',
                'instructions': 'Instructions',
                'commands': 'Commands',
                'graphics_options': 'Graphics Options',
                'language': 'Language',
                'exit': 'Exit',
                
                # Menu istruzioni
                'instructions_title': 'Welcome to Space Shooter!',
                'game_objective': 'Game Objective:',
                'game_objective_text': 'Survive as long as possible by destroying asteroids.',
                'controls': 'Controls:',
                'control_left': ' - Left Arrow: Move spaceship left',
                'control_right': ' - Right Arrow: Move spaceship right',
                'control_space': ' - Spacebar: Shoot',
                'control_pause': ' - P: Pause/Resume game',
                'mouse_mode': 'Mouse Mode Active:',
                'mouse_move': ' - Move mouse to move spaceship',
                'mouse_click': ' - Left click to shoot',
                'powerups': 'Power-ups:',
                'powerups_text': 'Collect power-ups to get bonuses like extra lives\nor enhanced projectiles.',
                'good_luck': 'Good luck, pilot!',
                'back_to_menu': 'Press Esc to return to Menu',
                
                # Menu comandi
                'commands_settings': 'Command Settings',
                'mouse_control': 'Move spaceship with mouse',
                
                # Menu opzioni grafiche
                'graphics_options_title': 'Graphics Options',
                'very_low': 'Very Low',
                'high': 'High',
                'graphics_desc': 'Very Low: Vector graphics (better performance)\nHigh: PNG images (better quality)',
                
                # Menu lingua
                'language_selection': 'Language Selection',
                'english': 'English',
                'italian': 'Italiano',
                'chinese': '中文',
                
                # Gioco
                'score': 'Score',
                'lives': 'Lives',
                'final_score': 'Final Score',
                'game_over': 'GAME OVER',
                'you_win': 'YOU WIN',
                'paused': 'PAUSED',
                'pause_instruction': 'Press P to resume',
                
                # Power-ups
                'double_fire': 'Double Fire!',
                'extra_life': 'Extra Life!',
                'power_up': 'Power-up!'
            },
            'it': {
                # Menu principale
                'game_title': '★ Space Shooter ★',
                'start_game': 'Inizia Partita',
                'instructions': 'Istruzioni',
                'commands': 'Comandi',
                'graphics_options': 'Opzioni grafiche',
                'language': 'Lingua',
                'exit': 'Esci',
                
                # Menu istruzioni
                'instructions_title': 'Benvenuto in Space Shooter!',
                'game_objective': 'Obiettivo del Gioco:',
                'game_objective_text': 'Sopravvivi il più a lungo possibile distruggendo gli asteroidi.',
                'controls': 'Controlli:',
                'control_left': ' - Freccia Sinistra: Muovi la navicella a sinistra',
                'control_right': ' - Freccia Destra: Muovi la navicella a destra',
                'control_space': ' - Barra Spaziatrice: Spara',
                'control_pause': ' - P: Pausa/Riprendi il gioco',
                'mouse_mode': 'Modalità Mouse Attiva:',
                'mouse_move': ' - Muovi il mouse per muovere la navicella',
                'mouse_click': ' - Clicca con il tasto sinistro per sparare',
                'powerups': 'Power-up:',
                'powerups_text': 'Raccogli i power-up per ottenere bonus come vite extra\no proiettili potenziati.',
                'good_luck': 'Buona fortuna, pilota!',
                'back_to_menu': 'Premi Esc per tornare al Menù',
                
                # Menu comandi
                'commands_settings': 'Impostazioni Comandi',
                'mouse_control': 'Sposta la navicella attraverso il mouse',
                
                # Menu opzioni grafiche
                'graphics_options_title': 'Opzioni Grafiche',
                'very_low': 'Molto basso',
                'high': 'Alto',
                'graphics_desc': 'Molto basso: Grafica vettoriale (prestazioni migliori)\nAlto: Immagini PNG (qualità migliore)',
                
                # Menu lingua
                'language_selection': 'Selezione Lingua',
                'english': 'English',
                'italian': 'Italiano',
                'chinese': '中文',
                
                # Gioco
                'score': 'Punteggio',
                'lives': 'Vite',
                'final_score': 'Punteggio finale',
                'game_over': 'GAME OVER',
                'you_win': 'HAI VINTO',
                'paused': 'IN PAUSA',
                'pause_instruction': 'Premi P per riprendere',
                
                # Power-ups
                'double_fire': 'Fuoco Doppio!',
                'extra_life': 'Vita Extra!',
                'power_up': 'Power-up!'
            },
            'zh': {
                # Menu principale
                'game_title': '★ 太空射击 ★',
                'start_game': '开始游戏',
                'instructions': '游戏说明',
                'commands': '控制设置',
                'graphics_options': '图形选项',
                'language': '语言',
                'exit': '退出',
                
                # Menu istruzioni
                'instructions_title': '欢迎来到太空射击！',
                'game_objective': '游戏目标：',
                'game_objective_text': '通过摧毁小行星尽可能长时间地生存。',
                'controls': '控制：',
                'control_left': ' - 左箭头：向左移动飞船',
                'control_right': ' - 右箭头：向右移动飞船',
                'control_space': ' - 空格键：射击',
                'control_pause': ' - P：暂停/继续游戏',
                'mouse_mode': '鼠标模式激活：',
                'mouse_move': ' - 移动鼠标来移动飞船',
                'mouse_click': ' - 左键点击射击',
                'powerups': '道具：',
                'powerups_text': '收集道具获得奖励，如额外生命\n或增强弹药。',
                'good_luck': '祝你好运，飞行员！',
                'back_to_menu': '按Esc返回菜单',
                
                # Menu comandi
                'commands_settings': '控制设置',
                'mouse_control': '用鼠标移动飞船',
                
                # Menu opzioni grafiche
                'graphics_options_title': '图形选项',
                'very_low': '很低',
                'high': '高',
                'graphics_desc': '很低：矢量图形（更好的性能）\n高：PNG图像（更好的质量）',
                
                # Menu lingua
                'language_selection': '语言选择',
                'english': 'English',
                'italian': 'Italiano',
                'chinese': '中文',
                
                # Gioco
                'score': '得分',
                'lives': '生命',
                'final_score': '最终得分',
                'game_over': '游戏结束',
                'you_win': '你赢了',
                'paused': '已暂停',
                'pause_instruction': '按P继续',
                
                # Power-ups
                'double_fire': '双重射击！',
                'extra_life': '额外生命！',
                'power_up': '道具！'
            }
        }
        
        # Carica la lingua salvata se esiste
        self.load_language_preference()
    
    def get_text(self, key):
        """Ottiene il testo tradotto per la chiave specificata"""
        return self.translations.get(self.current_language, {}).get(key, key)
    
    def set_language(self, language_code):
        """Imposta la lingua corrente"""
        if language_code in self.translations:
            self.current_language = language_code
            self.save_language_preference()
            return True
        return False
    
    def get_current_language(self):
        """Restituisce il codice della lingua corrente"""
        return self.current_language
    
    def get_available_languages(self):
        """Restituisce la lista delle lingue disponibili"""
        return list(self.translations.keys())
    
    def save_language_preference(self):
        """Salva la preferenza della lingua in un file"""
        try:
            with open('language_preference.json', 'w', encoding='utf-8') as f:
                json.dump({'language': self.current_language}, f, ensure_ascii=False)
        except Exception:
            pass  # Ignora errori di salvataggio
    
    def load_language_preference(self):
        """Carica la preferenza della lingua dal file"""
        try:
            if os.path.exists('language_preference.json'):
                with open('language_preference.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'language' in data and data['language'] in self.translations:
                        self.current_language = data['language']
        except Exception:
            pass  # Usa la lingua predefinita se c'è un errore

# Istanza globale del sistema di internazionalizzazione
i18n = I18n()

# Funzione di convenienza per ottenere testi tradotti
def _(key):
    """Funzione di convenienza per ottenere testi tradotti"""
    return i18n.get_text(key)