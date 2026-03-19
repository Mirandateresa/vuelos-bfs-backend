from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Nodo:
    def __init__(self, datos, padre=None):
        self.datos = datos
        self.padre = padre
    
    def get_datos(self):
        return self.datos
    
    def get_padre(self):
        return self.padre

def buscar_solucion_BFS(conexiones, estado_inicial, solucion):
    print(f"Buscando de {estado_inicial} a {solucion}")
    
    # Lista de nodos visitados
    visitados = []
    # Cola de nodos por visitar (frontera)
    frontera = [Nodo(estado_inicial)]
    
    while frontera:
        # Sacar el primer nodo de la cola
        nodo_actual = frontera.pop(0)
        print(f"Visitando: {nodo_actual.get_datos()}")
        
        # Agregar a visitados
        visitados.append(nodo_actual)
        
        # Verificar si es la solución
        if nodo_actual.get_datos() == solucion:
            print("¡Solución encontrada!")
            return nodo_actual
        
        # Expandir nodos hijos
        ciudad_actual = nodo_actual.get_datos()
        ciudades_conectadas = conexiones.get(ciudad_actual, [])
        
        for ciudad_hija in ciudades_conectadas:
            # Crear nuevo nodo
            nodo_hijo = Nodo(ciudad_hija, nodo_actual)
            
            # Verificar si ya fue visitado o está en frontera
            visitado = False
            for v in visitados:
                if v.get_datos() == ciudad_hija:
                    visitado = True
                    break
            
            en_frontera = False
            for f in frontera:
                if f.get_datos() == ciudad_hija:
                    en_frontera = True
                    break
            
            if not visitado and not en_frontera:
                frontera.append(nodo_hijo)
                print(f"  - Agregado a frontera: {ciudad_hija}")
    
    print("No se encontró solución")
    return None

@app.route('/buscar_ruta', methods=['POST'])
def buscar_ruta():
    try:
        data = request.get_json()
        print("Datos recibidos:", data)
        
        origen = data.get('origen', 'JILOYORK')
        destino = data.get('destino', 'ZACATECAS')
        
        print(f"Buscando ruta de {origen} a {destino}")
        
        # Conexiones entre ciudades (GRAFO DIRIGIDO)
        conexiones = {
            'JILOYORK': ['CELAYA', 'CDMX', 'QUERÉTARO'],
            'CELAYA': ['JILOYORK', 'SINALOA'],
            'CDMX': ['JILOYORK'],
            'QUERÉTARO': ['MONTERREY', 'TAMAULIPAS', 'ZACATECAS', 'SINALOA','JILOYORK', 'OAXACA'],
            'SONORA': ['ZACATECAS', 'SINALOA'],
            'SINALOA': ['CELAYA', 'SONORA', 'JILOYORK'],
            'ZACATECAS': ['SONORA', 'MONTERREY', 'QUERÉTARO'],
            'MONTERREY': ['ZACATECAS'],
            'TAMAULIPAS': ['QUERÉTARO'],
            'OAXACA': ['QUERÉTARO'],
            'GUANAJUATO': ['AGUASCALIENTES'],
            'AGUASCALIENTES': ['GUANAJUATO']
        }
        
        # Ejecutar BFS
        nodo_solucion = buscar_solucion_BFS(conexiones, origen, destino)
        
        if nodo_solucion:
            # Reconstruir la ruta
            ruta = []
            nodo = nodo_solucion
            while nodo:
                ruta.insert(0, nodo.get_datos())
                nodo = nodo.get_padre()
            
            print("Ruta encontrada:", ruta)
            
            return jsonify({
                'encontrada': True,
                'ruta': ruta,
                'mensaje': f'Ruta encontrada con {len(ruta)} ciudades'
            })
        else:
            print("No se encontró ruta")
            return jsonify({
                'encontrada': False,
                'ruta': [],
                'mensaje': 'No hay ruta disponible'
            })
            
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            'error': str(e),
            'encontrada': False,
            'ruta': []
        }), 500

@app.route('/ciudades', methods=['GET'])
def obtener_ciudades():
    conexiones = {
        'JILOYORK': ['CELAYA', 'CDMX', 'QUERÉTARO'],
        'CELAYA': ['JILOYORK', 'SINALOA'],
        'CDMX': ['JILOYORK'],
        'QUERÉTARO': ['MONTERREY', 'TAMAULIPAS', 'ZACATECAS', 'SINALOA','QUERETARO', 'OAXACA'],
        'SONORA': ['ZACATECAS', 'SINALOA'],
        'SINALOA': ['CELAYA', 'SONORA', 'JILOYORK'],
        'ZACATECAS': ['SONORA', 'MONTERREY', 'QUERÉTARO'],
        'MONTERREY': ['ZACATECAS'],
        'TAMAULIPAS': ['QUERÉTARO'],
        'OAXACA': ['QUERÉTARO'],
        'GUANAJUATO': ['AGUASCALIENTES'],
        'AGUASCALIENTES': ['GUANAJUATO']
    }
    ciudades = list(conexiones.keys())
    ciudades.sort()
    print("Ciudades disponibles:", ciudades)
    return jsonify({'ciudades': ciudades})

if __name__ == '__main__':
    print("=== SERVIDOR INICIADO ===")
    print("Puerto: 5000")
    print("Endpoint ciudades: http://localhost:5000/ciudades")
    print("Endpoint buscar: http://localhost:5000/buscar_ruta")
    print("========================")
    app.run(debug=True, port=5000, host='0.0.0.0')
