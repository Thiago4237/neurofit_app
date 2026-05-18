import sys, os
from src.core.app import NeuroFitApp

# Agrega la raíz del proyecto al path para que `from src...` funcione
sys.path.insert(0, os.path.abspath('.'))

if __name__ == '__main__':
    NeuroFitApp().run()