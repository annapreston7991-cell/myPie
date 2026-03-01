import os
import io
from contextlib import redirect_stdout
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.codeinput import CodeInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from pygments.lexers import PythonLexer
import jedi

# Android-specific storage path
from kivy.utils import platform
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
    SAVE_PATH = "/sdcard/MyPieScripts/"
else:
    SAVE_PATH = "./scripts/"

if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

class MyPieIDE(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.current_file = "untitled.py"

    def on_font_change(self, instance, value):
        # Update the actual editor font size
        self.editor.font_size = f"{int(value)}sp"
        # Update the label (you'll need to store the label as self.font_label)
        self.font_label.text = f"Font: {int(value)}sp"
        self.console.text = f">>> Font scaled to {int(value)}sp"

    def toggle_wordwrap(self, instance):
    	# Toggle the boolean state
        self.editor.do_wrap = not self.editor.do_wrap
    
        # Update button text to show current state
        if self.editor.do_wrap:
            instance.text = "WRAP: ON"
            instance.background_color = (0.2, 0.6, 0.2, 1) # Green for ON
            self.console.text = ">>> Word wrap enabled"
        else:
            instance.text = "WRAP: OFF"
            instance.background_color = (0.3, 0.3, 0.3, 1) # Gray for OFF
            self.console.text = ">>> Word wrap disabled"


        # --- 1. FULL FEATURED TOOLBAR ---
        toolbar = BoxLayout(size_hint_y=0.07, spacing=5, padding=5)
        
        btn_new = Button(text='NEW', background_color=(0.2, 0.2, 0.2, 1))
        btn_new.bind(on_release=self.new_file)
        
        btn_save = Button(text='SAVE', background_color=(0.2, 0.2, 0.7, 1))
        btn_save.bind(on_release=self.show_save_popup)
        
        btn_open = Button(text='OPEN', background_color=(0.2, 0.2, 0.2, 1))
        # btn_open logic can be added with a FileChooser
        
        self.run_btn = Button(text='▶ RUN', background_color=(0, 0.7, 0, 1), bold=True)
        self.run_btn.bind(on_release=self.run_code)

	# Create the Wrap Toggle Button
	self.btn_wrap = Button(text='WRAP: OFF', background_color=(0.3, 0.3, 0.3, 1))
	self.btn_wrap.bind(on_release=self.toggle_wordwrap)
	
	toolbar.add_widget(self.btn_wrap)
        toolbar.add_widget(btn_new)
        toolbar.add_widget(btn_save)
        toolbar.add_widget(btn_open)
        toolbar.add_widget(self.run_btn)

        # --- 2. SYMBOL BAR ---
        symbol_scroll = ScrollView(size_hint_y=0.07, do_scroll_y=False)
        symbols = BoxLayout(orientation='horizontal', size_hint_x=None, spacing=2)
        symbols.bind(minimum_width=symbols.setter('width'))
        for s in [':', '(', ')', '[', ']', '{', '}', '=', '"', "'", 'import', 'def', 'if', 'else']:
            btn = Button(text=s, width=110, size_hint_x=None, background_color=(0.15, 0.15, 0.15, 1))
            btn.bind(on_release=lambda b: self.editor.insert_text(b.text))
            symbols.add_widget(btn)
        symbol_scroll.add_widget(symbols)


	# Font Size Control Row
	font_row = BoxLayout(size_hint_y=0.05, padding=5, spacing=10)
	font_label = Label(text='Font: 14sp', size_hint_x=0.2)
	self.font_slider = Slider(min=10, max=30, value=14, step=1)
	self.font_slider.bind(value=self.on_font_change)

	font_row.add_widget(font_label)
	font_row.add_widget(self.font_slider)
	self.add_widget(font_row) # Add this before the editor

	

        # --- 3. EDITOR AREA ---
        self.editor = CodeInput(lexer=PythonLexer(), font_size='14sp', size_hint_y=0.55)
        
        # --- 4. SUGGESTION BAR ---
        suggest_scroll = ScrollView(size_hint_y=0.07, do_scroll_y=False)
        self.suggestions = BoxLayout(orientation='horizontal', size_hint_x=None, spacing=2)
        self.suggestions.bind(minimum_width=self.suggestions.setter('width'))
        suggest_scroll.add_widget(self.suggestions)
        self.editor.bind(text=self.update_suggestions)

        # --- 5. CONSOLE OUTPUT ---
        self.console = Label(
            text=">>> System Ready", 
            size_hint_y=0.24, 
            halign="left", 
            valign="top",
            color=(0, 1, 0, 1),
            padding=(10, 10)
        )
        self.console.bind(size=self.console.setter('text_size'))

        self.add_widget(toolbar)
        self.add_widget(symbol_scroll)
        self.add_widget(self.editor)
        self.add_widget(suggest_scroll)
        self.add_widget(self.console)

    def update_suggestions(self, instance, value):
        self.suggestions.clear_widgets()
        try:
            row, col = self.editor.cursor
            script = jedi.Script(value)
            completions = script.complete(row + 1, col)
            for c in completions[:6]:
                btn = Button(text=c.name, width=200, size_hint_x=None, background_color=(0.2, 0.4, 0.8, 1))
                btn.bind(on_release=lambda b, comp=c: self.editor.insert_text(comp.complete))
                self.suggestions.add_widget(btn)
        except: pass

    def run_code(self, instance):
        self.console.text = ">>> Executing...\n"
        output_buffer = io.StringIO()
        try:
            with redirect_stdout(output_buffer):
                exec(self.editor.text, {})
            result = output_buffer.getvalue()
            self.console.text = result if result else ">>> Success (No output)"
        except Exception as e:
            self.console.text = f">>> Error: {str(e)}"

    def new_file(self, instance):
        self.editor.text = ""
        self.current_file = "untitled.py"
        self.console.text = ">>> New file created"

    def show_save_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        filename_input = TextInput(text=self.current_file, multiline=False, size_hint_y=None, height=100)
        save_btn = Button(text='CONFIRM SAVE', size_hint_y=None, height=100)
        
        content.add_widget(Label(text="Enter filename:"))
        content.add_widget(filename_input)
        content.add_widget(save_btn)

        popup = Popup(title="Save Script", content=content, size_hint=(0.8, 0.4))
        
        def save_logic(btn):
            try:
                full_path = os.path.join(SAVE_PATH, filename_input.text)
                with open(full_path, 'w') as f:
                    f.write(self.editor.text)
                self.current_file = filename_input.text
                self.console.text = f">>> Saved to {full_path}"
                popup.dismiss()
            except Exception as e:
                self.console.text = f">>> Save Failed: {str(e)}"
        
        save_btn.bind(on_release=save_logic)
        popup.open()

class MyPieApp(App):
    def build(self):
        return MyPieIDE()

if __name__ == '__main__':
    MyPieApp().run()

