import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys
import threading
import time

class ScreenshotApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
        self.setup_hotkey()
        
    def setup_ui(self):
        self.root.title('Скриншотер')
        self.root.geometry('350x180')
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        title_label = tk.Label(
            self.root, 
            text='📸 Скриншотер', 
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0'
        )
        title_label.pack(pady=15)
        
    
        self.btn = tk.Button(
            self.root,
            text='Сделать скриншот (F2)',
            command=self.make_screenshot,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 12),
            padx=20,
            pady=10,
            width=20
        )
        self.btn.pack(pady=10)
        
        hotkey_info = tk.Label(
            self.root,
            text="F2 - быстрый скриншот\nCtrl+Q - выход из программы",
            font=('Arial', 9),
            bg='#f0f0f0',
            justify=tk.CENTER
        )
        hotkey_info.pack(pady=5)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_hotkey(self):
        """Настройка горячих клавиш в отдельном потоке"""
        def hotkey_listener():
            try:
                import keyboard
                keyboard.add_hotkey('f2', self.make_screenshot)
                keyboard.add_hotkey('ctrl+q', self.on_closing)
                keyboard.add_hotkey('ctrl+w', self.on_closing)
                
                while True:
                    if not self.root.winfo_exists():
                        break
                    time.sleep(0.1)
                        
            except ImportError:
                print("Библиотека keyboard не установлена")
            except Exception as e:
                print(f"Ошибка горячих клавиш: {e}")
        
        hotkey_thread = threading.Thread(target=hotkey_listener, daemon=True)
        hotkey_thread.start()
        
    def make_screenshot(self):
        """Создание скриншота"""
        try:
          
            self.show_notification("Запуск Snipping Tool...")
            process = subprocess.Popen(
                ['snippingtool', '/clip'], 
                shell=True, 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Ждем немного и показываем сообщение
            self.root.after(1000, lambda: self.show_success_message())
            
        except Exception as e:
            self.show_error_message(f"Ошибка: {str(e)}")
    
    def show_notification(self, message):
        """Показать уведомление в заголовке кнопки"""
        original_text = self.btn.cget('text')
        self.btn.config(text=message, bg='#FF9800')
        self.root.update()
        
        self.root.after(1000, lambda: self.btn.config(text=original_text, bg='#4CAF50'))
    
    def show_success_message(self):
        """Показать сообщение об успехе"""
        messagebox.showinfo(
            'Готово!', 
            'Snipping Tool запущен!\n\nВыделите область для скриншота,\nзатем используйте Ctrl+V для вставки.'
        )
    
    def show_error_message(self, error_text):
        """Показать сообщение об ошибке"""
        messagebox.showerror('Ошибка', error_text)
    
    def on_closing(self):
        """Закрытие приложения"""
        try:
            import keyboard
            keyboard.unhook_all()
        except:
            pass
        finally:
            self.root.destroy()
            os._exit(0)
    
    def run(self):
        """Запуск приложения"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()

if __name__ == "__main__":
    app = ScreenshotApp()
    app.run()
