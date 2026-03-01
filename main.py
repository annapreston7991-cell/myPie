from kivy.app import App
from kivy.uix.codeinput import CodeInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from pygments.lexers import PythonLexer
import jedi

class PythonEditor(CodeInput):
    def __init__(self, **kwargs):
        super().__init__(lexer=PythonLexer(), font_size='14sp', **kwargs)

    def get_suggestions(self):
        """Triggers Jedi to look at the current code and cursor position."""
        row, col = self.cursor
        script = jedi.Script(self.text)
        try:
            # Returns completions based on the current line/column
            return script.complete(row + 1, col)
        except:
            return []

class IDEInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        # 1. The Editor
        self.editor = PythonEditor(size_hint_y=0.9)
        
        # 2. Suggestion Bar (Scrollable)
        self.scroll_view = ScrollView(size_hint_y=0.1, do_scroll_y=False, do_scroll_x=True)
        self.suggestion_layout = BoxLayout(orientation='horizontal', size_hint_x=None)
        self.suggestion_layout.bind(minimum_width=self.suggestion_layout.setter('width'))
        
        self.scroll_view.add_widget(self.suggestion_layout)
        
        # Bind text change to update suggestions
        self.editor.bind(text=self.update_bar)
        
        self.add_widget(self.editor)
        self.add_widget(self.scroll_view)

    def update_bar(self, instance, value):
        self.suggestion_layout.clear_widgets()
        completions = self.editor.get_suggestions()
        
        for c in completions[:8]: # Show top 8 suggestions
            btn = Button(text=c.name, size_hint_x=None, width=200)
            # When clicked, complete the word
            btn.bind(on_release=lambda b, comp=c: self.apply_completion(comp))
            self.suggestion_layout.add_widget(btn)

    def apply_completion(self, completion):
        # Simplistic insertion of the remaining characters
        self.editor.insert_text(completion.complete)

class PyEditorApp(App):
    def build(self):
        return IDEInterface()

if __name__ == '__main__':
    PyEditorApp().run()

