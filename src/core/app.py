import os
import json

from datetime import datetime

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.resources import resource_find
from kivy.uix.screenmanager import ScreenManager

from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from kivy.metrics import dp

from src.core.screens import (
    WelcomeScreen,
    FormScreen,
    DashboardScreen
)

from src.ai.engine import NeuroFitEngine

# -----------------------------
# RUTAS
# -----------------------------

DATA_DIR = resource_find("data")

USER_DATA_FILE = (
    os.path.join(DATA_DIR, "user_data.json")
    if DATA_DIR else None
)

print("DATA_DIR:", DATA_DIR)
print("USER_DATA_FILE:", USER_DATA_FILE)

# -----------------------------
# APP
# -----------------------------
class NeuroFitApp(MDApp):

    edit_mode = False

    def build(self):

        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "700"

        self.user_data = {}

        # -----------------------------
        # Engine IA
        # -----------------------------
        self.engine = NeuroFitEngine()

        # -----------------------------
        # Cargar KV files
        # -----------------------------
        kv_files = [
            "src/kvs/welcome.kv",
            "src/kvs/form.kv",
            "src/kvs/dashboard.kv"
        ]

        for kv in kv_files:
            kv_path = resource_find(kv)
            print("KV:", kv)
            print("KV_PATH:", kv_path)
            if kv_path:
                Builder.load_file(kv_path)
            else:
                print(f"ERROR: No se encontró {kv}")

        # -----------------------------
        # ScreenManager
        # -----------------------------
        self.sm = ScreenManager()
        self.sm.add_widget(WelcomeScreen(name='welcome'))
        self.sm.add_widget(FormScreen(name='form'))
        self.sm.add_widget(DashboardScreen(name='dashboard'))

        # -----------------------------
        # Cargar datos previos
        # -----------------------------
        if self.cargar_datos():
            Clock.schedule_once(lambda dt: self.actualizar_dashboard(), 0.1)
            self.sm.current = 'dashboard'
        else:
            self.sm.current = 'welcome'

        return self.sm

    # =====================================================
    # PERSISTENCIA
    # =====================================================
    def cargar_datos(self):

        if not USER_DATA_FILE:
            print("ERROR: USER_DATA_FILE es None")
            return False

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

        if not DATA_DIR:
            print("ERROR: DATA_DIR no encontrado")
            return False

        os.makedirs(DATA_DIR, exist_ok=True)
        self.user_data['last_modified'] = datetime.now().isoformat()

        try:
            with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.user_data, f, indent=4)
            return True

        except Exception as e:
            print(f"Error guardando datos: {e}")
            return False

    # =====================================================
    # FORMULARIO
    # =====================================================
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

            if altura_str in ("Selecciona tu altura", ""):
                raise ValueError("Selecciona tu altura")

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
            toast(f"{str(e)}")

    # =====================================================
    # DASHBOARD
    # =====================================================
    def actualizar_dashboard(self):

        dash = self.sm.get_screen('dashboard')

        if not dash or not hasattr(dash, 'ids'):
            return

        u = self.user_data

        if not u:
            return

        # Actualizar info del drawer lateral
        if 'drawer_info_label' in dash.ids:

            objetivo_texto = u.get('objetivo') or 'No seleccionado'
            animo_texto = u.get('animo') or 'No seleccionado'

            dash.ids.drawer_info_label.text = (
                f"[b]Edad:[/b] {u['edad']} años\n"
                f"[b]Peso:[/b] {u['peso']} kg\n"
                f"[b]Altura:[/b] {u['altura']} cm\n"
                f"[b]Horas/sem:[/b] {u['horas']}\n"
                f"[b]Objetivo:[/b] {objetivo_texto}\n"
                f"[b]Ánimo:[/b] {animo_texto}\n\n"
                f"[i]Modificado: {u.get('last_modified', 'Nunca')[:16]}[/i]"
            )

        # Restaurar botones de selección (ahora son MDLabel dentro de MDCard)
        obj = u.get('objetivo')
        if 'btn_objetivo' in dash.ids:
            dash.ids.btn_objetivo.text = obj if obj else 'Seleccionar'

        anim = u.get('animo')
        if 'btn_animo' in dash.ids:
            dash.ids.btn_animo.text = anim if anim else 'Seleccionar'

        # Resetear zona de rutina
        if 'box_nivel_intensidad' in dash.ids:
            dash.ids.box_nivel_intensidad.height = 0
            dash.ids.box_nivel_intensidad.opacity = 0

        if 'rutina_container' in dash.ids:
            dash.ids.rutina_container.clear_widgets()
            placeholder = MDLabel(
                text="Selecciona tu objetivo y ánimo,\nluego pulsa [b]Generar rutina[/b]",
                halign="center",
                adaptive_height=True,
                theme_text_color="Hint",
                markup=True,
                size_hint_y=None,
                height=dp(80),
            )
            dash.ids.rutina_container.add_widget(placeholder)

    # =====================================================
    # SELECTORES DASHBOARD
    # =====================================================
    def abrir_selector_objetivo_dashboard(self):

        opciones = [
            "Perder peso",
            "Ganar músculo",
            "Resistencia",
            "Tonificación"
        ]

        # Usamos el card como caller para que el menú se posicione bien
        dash = self.sm.get_screen('dashboard')
        caller = dash.ids.btn_objetivo  # MDLabel dentro del card

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": opt,
                "height": dp(52),
                "on_release": lambda x=opt: self._seleccionar_objetivo(x)
            }
            for opt in opciones
        ]

        self.menu_obj = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
            max_height=dp(220),
            position="auto",
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

        dash = self.sm.get_screen('dashboard')
        caller = dash.ids.btn_animo

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": opt,
                "height": dp(52),
                "on_release": lambda x=opt: self._seleccionar_animo(x)
            }
            for opt in opciones
        ]

        self.menu_animo = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
            max_height=dp(260),
            position="auto",
        )

        self.menu_animo.open()

    def _seleccionar_animo(self, opcion):
        self.user_data['animo'] = opcion
        self.guardar_datos()
        self.actualizar_dashboard()
        self.menu_animo.dismiss()
        toast(f"Ánimo: {opcion}")

    # =====================================================
    # GENERAR RUTINA
    # =====================================================
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
        box.height = dp(56)
        box.opacity = 1

        dash.ids.lbl_nivel.text = f"Nivel: {resultado['nivel']}"
        dash.ids.lbl_intensidad.text = f"Intensidad: {resultado['intensidad'].capitalize()}"

        # Limpiar y rellenar tarjetas
        container = dash.ids.rutina_container
        container.clear_widgets()

        for ejercicio in resultado["rutina"]:
            card = self.crear_card_ejercicio(ejercicio)
            container.add_widget(card)

        toast("Rutina generada")

    # =====================================================
    # FORMULARIO — helpers
    # =====================================================
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

        # Ahora altura es un MDLabel, no MDTextField
        form.ids.altura.text = altura_str
        form.ids.horas.text = str(u.get('horas', ''))

    def nuevo_registro(self):
        self.edit_mode = False
        form = self.sm.get_screen('form')
        form.ids.edad.text = ''
        form.ids.peso.text = ''
        form.ids.altura.text = 'Selecciona tu altura'
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

    # =====================================================
    # ELIMINAR DATOS
    # =====================================================
    def eliminar_datos(self):
        try:
            self.user_data = {}

            if USER_DATA_FILE and os.path.exists(USER_DATA_FILE):
                os.remove(USER_DATA_FILE)

            dash = self.sm.get_screen('dashboard')
            if 'nav_drawer' in dash.ids:
                dash.ids.nav_drawer.set_state("close")

            self.sm.current = 'welcome'
            toast("Información eliminada")

        except Exception as e:
            toast(f"Error: {str(e)}")

    # =====================================================
    # SELECTOR ALTURA — FIX: usa MDLabel + MDDropdownMenu
    # sin depender de on_focus (que causa el bug fantasma)
    # =====================================================
    def abrir_selector_altura(self, caller_widget):
        """
        caller_widget es el Widget anchor invisible dentro del card de altura.
        Esto evita el bug de foco-fantasma que ocurría con MDTextField readonly.
        """
        opciones = ["< 50 cm"] + [f"{h} cm" for h in range(50, 211)] + ["> 210 cm"]

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": opt,
                "height": dp(52),
                "on_release": lambda x=opt: self._seleccionar_altura(x)
            }
            for opt in opciones
        ]

        self._altura_menu = MDDropdownMenu(
            caller=caller_widget,
            items=menu_items,
            width_mult=4,
            max_height=dp(260),
            position="auto",
        )

        self._altura_menu.open()

    def _seleccionar_altura(self, opcion):
        form = self.sm.get_screen('form')
        # Actualizar el MDLabel que muestra la altura seleccionada
        lbl = form.ids.altura
        lbl.text = opcion
        lbl.theme_text_color = "Custom"
        lbl.text_color = (0.18, 0.36, 0.43, 1)

        if hasattr(self, '_altura_menu'):
            self._altura_menu.dismiss()

    # =====================================================
    # TARJETAS DE EJERCICIO
    # =====================================================
    def crear_card_ejercicio(self, ejercicio):

        card = MDCard(
            orientation="vertical",
            padding=[dp(14), dp(10), dp(14), dp(10)],
            spacing=dp(0),
            size_hint_y=None,
            height=dp(88),
            radius=[dp(16)],
            elevation=0,
            md_bg_color=(1, 1, 1, 1),
        )

        # Línea de acento izquierda (decorativa)
        outer = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12),
        )

        acento = MDBoxLayout(
            size_hint_x=None,
            width=dp(4),
            md_bg_color=(0.18, 0.36, 0.43, 1),
            radius=[dp(4)],
        )

        contenido = MDBoxLayout(
            orientation="vertical",
            spacing=dp(6),
        )

        titulo = MDLabel(
            text=ejercicio["ejercicio"],
            bold=True,
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=(0.18, 0.36, 0.43, 1),
            size_hint_y=None,
            height=dp(26),
            valign="middle",
        )

        detalle = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(0),
            size_hint_y=None,
            height=dp(22),
        )

        datos = [
            ("Series",      str(ejercicio['series'])),
            ("Reps",        str(ejercicio['repeticiones'])),
            ("Descanso",    ejercicio['descanso']),
        ]

        for i, (prefijo, valor) in enumerate(datos):
            # Separador visual entre chips (excepto el primero)
            if i > 0:
                sep = MDLabel(
                    text="|",
                    size_hint_x=None,
                    width=dp(16),
                    halign="center",
                    font_style="Caption",
                    theme_text_color="Custom",
                    text_color=(0.75, 0.80, 0.82, 1),
                )
                detalle.add_widget(sep)

            chip = MDLabel(
                text=f"[b]{prefijo}:[/b] {valor}",
                markup=True,
                font_style="Caption",
                theme_text_color="Custom",
                text_color=(0.35, 0.55, 0.60, 1),
                halign="left",
                valign="middle",
            )
            detalle.add_widget(chip)

        contenido.add_widget(titulo)
        contenido.add_widget(detalle)

        outer.add_widget(acento)
        outer.add_widget(contenido)
        card.add_widget(outer)

        return card