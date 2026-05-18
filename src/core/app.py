import os
import json

from datetime import datetime
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from src.core.screens import WelcomeScreen, FormScreen, DashboardScreen
from src.ai.engine import NeuroFitEngine



# Rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
USER_DATA_FILE = os.path.join(DATA_DIR, 'user_data.json')
KVS_DIR = os.path.join(BASE_DIR, 'src', 'kvs')


class NeuroFitApp(MDApp):
    edit_mode = False

    def build(self):
        
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "500"
        # self.theme_cls.theme_style = "Dark"
        
        self.user_data = {}
        self.engine = NeuroFitEngine()

        # Cargar archivos KV
        if not os.path.exists(KVS_DIR):
            print(f"ERROR: No se encuentra {KVS_DIR}")
        else:
            for kv_file in os.listdir(KVS_DIR):
                if kv_file.endswith('.kv'):
                    Builder.load_file(os.path.join(KVS_DIR, kv_file))

        self.sm = ScreenManager()
        self.sm.add_widget(WelcomeScreen(name='welcome'))
        self.sm.add_widget(FormScreen(name='form'))
        self.sm.add_widget(DashboardScreen(name='dashboard'))

        # Cargar datos previos
        if self.cargar_datos():
            Clock.schedule_once(lambda dt: self.actualizar_dashboard(), 0.1)
            self.sm.current = 'dashboard'
        else:
            self.sm.current = 'welcome'

        return self.sm

    # ------------------- PERSISTENCIA -------------------
    def cargar_datos(self):
        if not os.path.exists(USER_DATA_FILE):
            return False

        try:
            with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            required_keys = ['edad', 'peso', 'altura', 'horas']

            if all(k in data for k in required_keys):
                self.user_data = data
                self.user_data.setdefault('objetivo', None)
                self.user_data.setdefault('animo', None)
                return True

            return False

        except Exception as e:
            print(f"Error cargando datos: {e}")
            return False

    def guardar_datos(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.user_data['last_modified'] = datetime.now().isoformat()

        try:
            with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.user_data, f, indent=4)
            return True

        except Exception as e:
            print(f"Error guardando datos: {e}")
            return False

    def guardar_datos_basicos(self):
        form = self.sm.get_screen('form')

        try:
            edad = int(form.ids.edad.text.strip())
            peso = float(form.ids.peso.text.strip())
            altura_str = form.ids.altura.text.strip()
            horas = int(form.ids.horas.text.strip())

            if not (15 <= edad <= 80):
                raise ValueError("Edad entre 15 y 80")

            if not (30 <= peso <= 200):
                raise ValueError("Peso entre 30 y 200 kg")

            if not (1 <= horas <= 20):
                raise ValueError("Horas entre 1 y 20")

            if altura_str == "< 50 cm":
                altura_val = 40
            elif altura_str == "> 210 cm":
                altura_val = 220
            else:
                altura_val = int(altura_str.replace(" cm", ""))

            self.user_data.update({
                "edad": edad,
                "peso": peso,
                "altura": altura_val,
                "horas": horas,
            })

            if self.guardar_datos():
                toast("Datos básicos guardados")
            else:
                toast("Error al guardar")

            self.actualizar_dashboard()
            self.sm.current = 'dashboard'

        except Exception as e:
            toast(f"⚠️ {str(e)}")

    # ------------------- DASHBOARD -------------------
    def actualizar_dashboard(self):
        dash = self.sm.get_screen('dashboard')

        if not dash or not hasattr(dash, 'ids'):
            return

        u = self.user_data

        if not u:
            return

        # Actualizar info del drawer lateral
        if 'drawer_info_label' in dash.ids:
            objetivo_texto = u.get('objetivo', 'No seleccionado')
            animo_texto = u.get('animo', 'No seleccionado')

            dash.ids.drawer_info_label.text = (
                f"[b]Edad:[/b] {u['edad']} años\n"
                f"[b]Peso:[/b] {u['peso']} kg\n"
                f"[b]Altura:[/b] {u['altura']} cm\n"
                f"[b]Horas/sem:[/b] {u['horas']}\n"
                f"[b]Objetivo:[/b] {objetivo_texto}\n"
                f"[b]Ánimo:[/b] {animo_texto}\n\n"
                f"[i]Modificado: {u.get('last_modified', 'Nunca')[:16]}[/i]"
            )

        # Restaurar botones de selección
        if hasattr(dash.ids, 'btn_objetivo'):
            obj = u.get('objetivo')
            dash.ids.btn_objetivo.text = obj if obj else 'Seleccionar objetivo'

        if hasattr(dash.ids, 'btn_animo'):
            anim = u.get('animo')
            dash.ids.btn_animo.text = anim if anim else 'Seleccionar ánimo'

        # Resetear zona de rutina: ocultar nivel/intensidad y mostrar placeholder
        if hasattr(dash.ids, 'box_nivel_intensidad'):
            dash.ids.box_nivel_intensidad.height = 0
            dash.ids.box_nivel_intensidad.opacity = 0

        if hasattr(dash.ids, 'rutina_container'):
            dash.ids.rutina_container.clear_widgets()
            from kivymd.uix.label import MDLabel
            placeholder = MDLabel(
                id='rutina_placeholder',
                text="Selecciona tu objetivo y ánimo,\nluego pulsa [b]Generar rutina[/b]",
                halign="center",
                adaptive_height=True,
                theme_text_color="Hint",
                markup=True,
            )
            dash.ids.rutina_container.add_widget(placeholder)

    # ------------------- SELECTORES -------------------
    def abrir_selector_objetivo_dashboard(self):
        opciones = [
            "Perder peso",
            "Ganar músculo",
            "Resistencia",
            "Tonificación"
        ]

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": opt,
                "height": dp(48),
                "on_release": lambda x=opt: self._seleccionar_objetivo(x)
            }
            for opt in opciones
        ]

        self.menu_obj = MDDropdownMenu(
            caller=self.sm.get_screen('dashboard').ids.btn_objetivo,
            items=menu_items,
            width_mult=3,
            max_height=dp(200)
        )

        self.menu_obj.open()

    def _seleccionar_objetivo(self, opcion):
        self.user_data['objetivo'] = opcion
        self.guardar_datos()
        self.actualizar_dashboard()
        self.menu_obj.dismiss()
        toast(f"Objetivo: {opcion}")

    def abrir_selector_animo(self):
        opciones = [
            "Excelente",
            "Bien",
            "Normal",
            "Cansado",
            "Desanimado"
        ]

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": opt,
                "height": dp(48),
                "on_release": lambda x=opt: self._seleccionar_animo(x)
            }
            for opt in opciones
        ]

        self.menu_animo = MDDropdownMenu(
            caller=self.sm.get_screen('dashboard').ids.btn_animo,
            items=menu_items,
            width_mult=3,
            max_height=dp(200)
        )

        self.menu_animo.open()

    def _seleccionar_animo(self, opcion):
        self.user_data['animo'] = opcion
        self.guardar_datos()
        self.actualizar_dashboard()
        self.menu_animo.dismiss()
        toast(f"Ánimo: {opcion}")

    # ------------------- GENERAR RUTINA -------------------
    def generar_rutina(self):
        u = self.user_data

        if not u.get('objetivo'):
            toast("Selecciona un objetivo")
            return

        if not u.get('animo'):
            toast("Selecciona tu estado de ánimo")
            return

        resultado = self.engine.generar_plan(
            edad=u['edad'],
            peso=u['peso'],
            altura=u['altura'],
            horas=u['horas'],
            objetivo=u['objetivo'],
            animo=u['animo']
        )

        dash = self.sm.get_screen('dashboard')

        # Mostrar bloque nivel/intensidad
        box = dash.ids.box_nivel_intensidad
        box.height = 70
        box.opacity = 1

        # Actualizar textos de nivel e intensidad
        dash.ids.lbl_nivel.text = f"Nivel: {resultado['nivel']}"
        dash.ids.lbl_intensidad.text = f"Intensidad: {resultado['intensidad'].capitalize()}"

        # Limpiar contenedor (quita placeholder y tarjetas anteriores)
        container = dash.ids.rutina_container
        container.clear_widgets()

        # Crear tarjetas para cada ejercicio
        for ejercicio in resultado["rutina"]:
            card = self.crear_card_ejercicio(ejercicio)
            container.add_widget(card)

        toast("Rutina generada")
    
    # ------------------- FORMULARIO -------------------
    def precargar_formulario(self):
        form = self.sm.get_screen('form')
        u = self.user_data

        form.ids.edad.text = str(u.get('edad', ''))
        form.ids.peso.text = str(u.get('peso', ''))

        altura_cm = u.get('altura', 0)

        if altura_cm == 40:
            altura_str = "< 50 cm"
        elif altura_cm == 220:
            altura_str = "> 210 cm"
        else:
            altura_str = f"{altura_cm} cm"

        form.ids.altura.text = altura_str
        form.ids.horas.text = str(u.get('horas', ''))

    def nuevo_registro(self):
        self.edit_mode = False

        form = self.sm.get_screen('form')
        form.ids.edad.text = ''
        form.ids.peso.text = ''
        form.ids.altura.text = ''
        form.ids.horas.text = ''

        self.sm.current = 'form'

    def abrir_formulario_editar(self):
        self.edit_mode = True
        self.precargar_formulario()
        self.sm.current = 'form'

        dash = self.sm.get_screen('dashboard')

        if hasattr(dash.ids, 'nav_drawer'):
            dash.ids.nav_drawer.set_state("close")

    def cancelar_edicion(self):
        self.sm.current = 'dashboard'

    # ------------------- ELIMINAR DATOS -------------------
    def eliminar_datos(self):
        try:
            self.user_data = {}

            if os.path.exists(USER_DATA_FILE):
                os.remove(USER_DATA_FILE)

            dash = self.sm.get_screen('dashboard')

            if hasattr(dash.ids, 'nav_drawer'):
                dash.ids.nav_drawer.set_state("close")

            self.sm.current = 'welcome'

            toast("Información eliminada")

        except Exception as e:
            toast(f"Error: {str(e)}")

    # ------------------- ALTURA -------------------
    def abrir_selector_altura(self, widget):
        opciones = ["< 50 cm"] + [f"{h} cm" for h in range(50, 211)] + ["> 210 cm"]

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": opt,
                "on_release": lambda x=opt: self._seleccionar_altura(x, widget)
            }
            for opt in opciones
        ]

        self._altura_menu = MDDropdownMenu(
            caller=widget,
            items=menu_items,
            width_mult=3,
            max_height=dp(200)
        )

        self._altura_menu.open()

    def _seleccionar_altura(self, opcion, widget):
        widget.text = opcion
        widget.helper_text = "Seleccionado"
        widget.focus = False

        if hasattr(self, '_altura_menu'):
            self._altura_menu.dismiss()
    
    # ------------------- TARJETAS -------------------
    def crear_card_ejercicio(self, ejercicio):

        card = MDCard(
            orientation="vertical",
            padding="15dp",
            spacing="10dp",
            size_hint_y=None,
            height="140dp",
            radius=[20],
            # elevation=8,
            # shadow_softness=12,
            # shadow_offset=(0, -2),
            elevation=0,
            md_bg_color=(1, 1, 1, 1)
        )

        contenido = MDBoxLayout(
            orientation="vertical",
            spacing="8dp"
        )

        titulo = MDLabel(
            text=ejercicio["ejercicio"],
            bold=True,
            font_style="H6"
        )

        series = MDLabel(
            text=f"Series: {ejercicio['series']}"
        )

        repeticiones = MDLabel(
            text=f"Repeticiones: {ejercicio['repeticiones']}"
        )

        descanso = MDLabel(
            text=f"Descanso: {ejercicio['descanso']}"
        )

        contenido.add_widget(titulo)
        contenido.add_widget(series)
        contenido.add_widget(repeticiones)
        contenido.add_widget(descanso)

        card.add_widget(contenido)

        return card