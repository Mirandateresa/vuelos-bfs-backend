class Nodo:
    def __init__(self, datos, padre=None):
        self.datos = datos
        self.padre = padre
        self.hijos = []
    
    def set_hijos(self, hijos):
        self.hijos = hijos
    
    def get_datos(self):
        return self.datos
    
    def get_padre(self):
        return self.padre
    
    def en_lista(self, lista_nodos):
        for nodo in lista_nodos:
            if nodo.get_datos() == self.datos:
                return True
        return False