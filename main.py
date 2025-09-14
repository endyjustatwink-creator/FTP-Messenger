from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle, Blur
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp
import ftplib
import threading
import json
import os
from datetime import datetime

# Стиль iOS 26 Liquid Glass + Telegram
COLORS = {
    'primary': '#0088CC',       # Telegram blue
    'secondary': '#6BC259',     # Telegram green
    'background': '#0F0F0F',    # Dark background
    'surface': '#1A1A1A',       # Card background
    'surface_light': '#2D2D2D', # Lighter surface
    'text_primary': '#FFFFFF',  # White text
    'text_secondary': '#A0A0A0',# Gray text
    'accent': '#FF9500',        # Orange accent
    'error': '#FF3B30',         # Red
    'success': '#34C759',       # Green
}

class GlassMorphism(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(rgba=(0.1, 0.1, 0.1, 0.6))  # Glass effect
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class LiquidButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.color = COLORS['text_primary']
        self.font_size = dp(16)
        self.bold = True
        self.size_hint_y = None
        self.height = dp(56)
        
        with self.canvas.before:
            Color(*self.hex_to_rgb(COLORS['primary']))
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])
        
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return [int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4)] + [0.9]

class MessageBubble(BoxLayout):
    text = StringProperty('')
    time = StringProperty('')
    is_outgoing = NumericProperty(0)  # 0 for incoming, 1 for outgoing

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(12), dp(8)]
        self.spacing = dp(4)

class ChatListItem(BoxLayout):
    name = StringProperty('')
    last_message = StringProperty('')
    time = StringProperty('')
    unread = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = [dp(16), dp(12)]
        self.spacing = dp(16)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Background with blur effect
        with self.canvas.before:
            Color(*self.hex_to_rgb(COLORS['background']))
            self.bg_rect = Rectangle(size=Window.size, pos=self.pos)
        
        # Main layout
        main_layout = FloatLayout()
        
        # Glass morphism container
        glass_container = GlassMorphism(size_hint=(0.85, 0.7), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        content_layout = BoxLayout(orientation='vertical', padding=dp(40), spacing=dp(30))
        
        # Logo
        logo = Label(text='📱', font_size=dp(60), size_hint_y=None, height=dp(100))
        
        # Title
        title = Label(text='FTP Messenger', font_size=dp(28), bold=True, 
                     color=COLORS['text_primary'], size_hint_y=None, height=dp(60))
        
        subtitle = Label(text='Telegram style • iOS 26 design', font_size=dp(14),
                        color=COLORS['text_secondary'], size_hint_y=None, height=dp(40))
        
        # Form
        form_layout = BoxLayout(orientation='vertical', spacing=dp(20))
        
        inputs = [
            ('🌐', 'FTP Server Address', 'host_input'),
            ('👤', 'Username', 'user_input'),
            ('🔒', 'Password', 'pass_input')
        ]
        
        for icon, hint, attr_name in inputs:
            input_layout = BoxLayout(orientation='horizontal', spacing=dp(12), size_hint_y=None, height=dp(60))
            icon_label = Label(text=icon, font_size=dp(20), size_hint_x=None, width=dp(40))
            input_field = TextInput(hint_text=hint, size_hint_x=1, height=dp(60),
                                  background_color=(0,0,0,0), foreground_color=COLORS['text_primary'],
                                  hint_text_color=COLORS['text_secondary'], padding=dp(15),
                                  cursor_color=COLORS['primary'])
            setattr(self, attr_name, input_field)
            input_layout.add_widget(icon_label)
            input_layout.add_widget(input_field)
            form_layout.add_widget(input_layout)
        
        # Connect button
        connect_btn = LiquidButton(text='Connect to Server')
        connect_btn.bind(on_press=self.connect)
        
        content_layout.add_widget(logo)
        content_layout.add_widget(title)
        content_layout.add_widget(subtitle)
        content_layout.add_widget(form_layout)
        content_layout.add_widget(connect_btn)
        
        glass_container.add_widget(content_layout)
        main_layout.add_widget(glass_container)
        self.add_widget(main_layout)
    
    def connect(self, instance):
        # FTP connection logic will be here
        print("Connecting to FTP server...")
        self.manager.current = 'chats'

class ChatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Background
        with self.canvas.before:
            Color(*self.hex_to_rgb(COLORS['background']))
            self.bg_rect = Rectangle(size=Window.size, pos=self.pos)
        
        main_layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(60), padding=[dp(16), 0])
        header.add_widget(Label(text='Chats', font_size=dp(20), bold=True, color=COLORS['text_primary']))
        
        # Search bar
        search_layout = BoxLayout(size_hint_y=None, height=dp(50), padding=[dp(16), dp(8)])
        search_input = TextInput(hint_text='Search', size_hint_x=1,
                               background_color=COLORS['surface'], foreground_color=COLORS['text_primary'],
                               hint_text_color=COLORS['text_secondary'])
        search_layout.add_widget(search_input)
        
        # Chats list
        scroll = ScrollView()
        chats_list = BoxLayout(orientation='vertical', size_hint_y=None)
        chats_list.bind(minimum_height=chats_list.setter('height'))
        
        # Sample chats
        sample_chats = [
            {'name': 'General Chat', 'message': 'Hello everyone!', 'time': '12:30', 'unread': 3},
            {'name': 'Support', 'message': 'How can I help?', 'time': '11:45', 'unread': 0},
            {'name': 'File Sharing', 'message': 'New file uploaded', 'time': '10:20', 'unread': 1}
        ]
        
        for chat in sample_chats:
            chat_item = ChatListItem(name=chat['name'], last_message=chat['message'],
                                   time=chat['time'], unread=chat['unread'])
            chats_list.add_widget(chat_item)
        
        scroll.add_widget(chats_list)
        
        main_layout.add_widget(header)
        main_layout.add_widget(search_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Chat interface will be here
        pass

class FTPMessengerApp(App):
    def build(self):
        Window.clearcolor = self.hex_to_rgb(COLORS['background'])
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ChatsScreen(name='chats'))
        sm.add_widget(ChatScreen(name='chat'))
        return sm

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return [int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4)]

if __name__ == '__main__':
    FTPMessengerApp().run()
