from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from groq import Groq
import threading

# Teri Groq API Key
API_KEY = "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"
client = Groq(api_key=API_KEY)

class RengokuChatApp(App):
    def build(self):
        self.messages_history = [
            {"role": "system", "content": "Tera naam Rengoku hai! Tu ek cool AI assistant hai. Hinglish me baat kar."}
        ]
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_logs = Label(text="🔥 Rengoku AI App Ready! 🔥\n\n", size_hint_y=None, markup=True)
        self.chat_logs.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.chat_logs.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        self.scroll.add_widget(self.chat_logs)
        main_layout.add_widget(self.scroll)
        
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=5)
        self.user_input = TextInput(hint_text="Kuch poocho bhai...", multiline=False)
        send_btn = Button(text="Send 🚀", size_hint=(0.3, 1), background_color=(0.2, 0.6, 1, 1))
        send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.user_input)
        input_layout.add_widget(send_btn)
        main_layout.add_widget(input_layout)
        
        return main_layout

    def send_message(self, instance):
        text = self.user_input.text.strip()
        if text:
            self.chat_logs.text += f"[b]Aap:[/b] {text}\n"
            self.user_input.text = ""
            threading.Thread(target=self.get_ai_response, args=(text,)).start()

    def get_ai_response(self, text):
        self.messages_history.append({"role": "user", "content": text})
        try:
            chat_completion = client.chat.completions.create(
                messages=self.messages_history,
                model="llama-3.3-70b-versatile",
            )
            reply = chat_completion.choices[0].message.content
            self.messages_history.append({"role": "assistant", "content": reply})
            self.chat_logs.text += f"[b]Rengoku:[/b] {reply}\n\n"
        except Exception as e:
            self.chat_logs.text += f"[color=ff0000]Error: {e}[/color]\n\n"

if __name__ == "__main__":
    RengokuChatApp().run()
      
