# src/utils/toast.py
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.animation import Animation

class Toast:
    """Toast cross-platform compatible con Kivy puro"""
    
    _instance = None
    _label = None
    _clock_event = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def show(self, text: str, duration: float = 2.0):
        """Muestra un toast tipo Android en cualquier plataforma"""
        from kivymd.app import MDApp
        
        # Cancelar toast anterior si existe
        if self._clock_event:
            self._clock_event.cancel()
        if self._label and self._label.parent:
            self._label.parent.remove_widget(self._label)
        
        # Crear label estilizado
        self._label = Label(
            text=text,
            size_hint=(None, None),
            size=('220dp', '40dp'),
            color=(1, 1, 1, 1),
            font_size='14sp',
            bold=True,
            halign='center',
            valign='middle',
            opacity=0
        )
        # Fondo semitransparente con canvas
        with self._label.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(0, 0, 0, 0.85)
            RoundedRectangle(pos=self._label.pos, size=self._label.size, radius=[10])
        
        # Posicionar en parte inferior central
        app = MDApp.get_running_app()
        if app and app.root:
            self._label.pos = (
                (app.root.width - self._label.width) / 2,
                50  # 50px desde el fondo
            )
            app.root.add_widget(self._label)
            
            # Animación fade-in + fade-out
            anim_in = Animation(opacity=1, duration=0.2)
            anim_out = Animation(opacity=0, duration=0.3)
            anim_in.start(self._label)
            
            def remove_label(*args):
                anim_out.start(self._label)
                Clock.schedule_once(lambda dt: self._label.parent.remove_widget(self._label) if self._label.parent else None, 0.35)
            
            self._clock_event = Clock.schedule_once(remove_label, duration)

# Instancia global para usar como función
toast = Toast().show