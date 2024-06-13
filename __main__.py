import sys
from src.vista.InterfazEnForma import App_EnForma
from src.logica.LogicaEnForma import LogicaEnForma

if __name__ == '__main__':
    # Punto inicial de la aplicación

    logica = LogicaEnForma()

    app = App_EnForma(sys.argv, logica)
    sys.exit(app.exec_())