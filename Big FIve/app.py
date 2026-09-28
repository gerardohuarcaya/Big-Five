from flask import Flask, render_template, request
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

usuarios = []

class Pila:

    def __init__(self):
        self.items=[]

    def apilar(self,item):
        self.items.append(item)

    def desapilar(self):
        if self.items:
            return self.items.pop()

    def mostrar(self):
        return self.items

class Cola:

    def __init__(self):
        self.items=[]

    def encolar(self,item):
        self.items.append(item)

    def desencolar(self):
        if self.items:
            return self.items.pop(0)

    def mostrar(self):
        return self.items
    
class Nodo:

    def __init__(self,dato):
        self.dato=dato
        self.siguiente=None


class ListaEnlazada:

    def __init__(self):
        self.cabeza=None

    def agregar(self,dato):

        nuevo=Nodo(dato)

        if self.cabeza is None:
            self.cabeza=nuevo
            return

        actual=self.cabeza

        while actual.siguiente:
            actual=actual.siguiente

        actual.siguiente=nuevo

    def mostrar(self):

        datos=[]

        actual=self.cabeza

        while actual:

            datos.append(actual.dato)

            actual=actual.siguiente

        return datos

def clasificar_perfil(apertura,responsabilidad,extroversion,neuroticismo):

    if responsabilidad>=4:

        if extroversion>=4:
            return "Líder"

        elif apertura>=4:
            return "Innovador"

        else:
            return "Organizado"

    else:

        if apertura>=4:
            return "Creativo"

        elif neuroticismo>=4:
            return "Emocional"

        else:
            return "Equilibrado"

def interpretar(valor):
    niveles = {
        1: "Muy bajo",
        2: "Bajo",
        3: "Medio",
        4: "Alto",
        5: "Muy alto"
    }
    return niveles.get(valor, "Desconocido")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultados', methods=['POST'])

def resultados():

        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        
        apertura = int(request.form.get('p1', 3))
        responsabilidad = int(request.form.get('p2', 3))
        extroversion = int(request.form.get('p3', 3))
        amabilidad = int(request.form.get('p4', 3))
        neuroticismo = int(request.form.get('p5', 3))

        respuestas = [
            apertura,
            responsabilidad,
            extroversion,
            amabilidad,
            neuroticismo
        ]
            
        promedio = round(sum(respuestas) / len(respuestas), 2)
        mayor = max(respuestas)
        menor = min(respuestas)
        
        rasgos = {
            "Apertura": apertura,
            "Responsabilidad": responsabilidad,
            "Extroversión": extroversion,
            "Amabilidad": amabilidad,
            "Neuroticismo": neuroticismo
        }
        
        ranking = sorted(
            rasgos.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        pila=Pila()
        
        for dato in ranking:
            pila.apilar(dato)
            
        ultimo_rasgo=pila.desapilar()

        cola=Cola()
        
        cola.encolar(nombre)
        cola.encolar(correo)
        
        cola_actual=cola.mostrar()

        historial=ListaEnlazada()
        
        for respuesta in respuestas:
            historial.agregar(respuesta)
            
        historial_respuestas=historial.mostrar()

        perfil = clasificar_perfil(
            apertura,
            responsabilidad,
            extroversion,
            neuroticismo
            
        )

        rasgo_dominante = ranking[0][0]
        puntaje_dominante = ranking[0][1]

        informe = ""


        # Apertura

        if apertura >= 4:
            informe += "• Presentas una alta apertura a la experiencia. Disfrutas aprender cosas nuevas y explorar diferentes ideas.\n\n"
        elif apertura == 3:
            informe += "• Presentas una apertura media. Combinas la curiosidad por aprender con la preferencia por actividades conocidas.\n\n"
        else:
            informe += "• Prefieres la estabilidad y las actividades que ya conoces. Tiendes a sentirte cómodo con las rutinas.\n\n"

        # Responsabilidad

        if responsabilidad >= 4:
            informe += "• Eres una persona organizada y responsable. Sueles cumplir tus tareas y planificar tus actividades.\n\n"
        elif responsabilidad == 3:
            informe += "• Presentas un nivel medio de responsabilidad. Puedes organizarte cuando es necesario, aunque también eres flexible.\n\n"
        else:
            informe += "• Tiendes a actuar de forma espontánea y en ocasiones puedes dejar tareas para después.\n\n"

        # Extroversión

        if extroversion >= 4:
            informe += "• Disfrutas interactuar con otras personas y participar en actividades sociales.\n\n"
        elif extroversion == 3:
            informe += "• Te adaptas tanto a reuniones sociales como a momentos de tranquilidad.\n\n"
        else:
            informe += "• Prefieres ambientes tranquilos y grupos pequeños. Disfrutas dedicar tiempo a actividades individuales.\n\n"

        # Amabilidad

        if amabilidad >= 4:
            informe += "• Sueles actuar con empatía, cooperación y consideración hacia los demás.\n\n"
        elif amabilidad == 3:
            informe += "• Mantienes un equilibrio entre defender tus ideas y comprender a las demás personas.\n\n"
        else:
            informe += "• Tiendes a expresar tus opiniones con firmeza y priorizar tus propios criterios cuando tomas decisiones.\n\n"

        # Neuroticismo

        if neuroticismo >= 4:
            informe += "• Puedes experimentar el estrés o la preocupación con mayor intensidad ante situaciones difíciles.\n\n"
        elif neuroticismo == 3:
            informe += "• Tu estabilidad emocional es intermedia. Dependiendo de la situación puedes sentirte tranquilo o preocupado.\n\n"
        else:   
            informe += "• Generalmente mantienes la calma y afrontas las dificultades con estabilidad emocional.\n\n"
            
        
        respuesta_ia = client.responses.create(
            model="gpt-5.4-mini",
            input=f"""
        Eres un psicólogo experto en el modelo Big Five.
        
        Analiza los siguientes resultados y redacta un informe profesional.
        
        Nombre: {nombre}
        
        Resultados:
        - Apertura: {apertura}/5
        - Responsabilidad: {responsabilidad}/5
        - Extroversión: {extroversion}/5
        - Amabilidad: {amabilidad}/5
        - Neuroticismo: {neuroticismo}/5
        
        Rasgo dominante:
        {rasgo_dominante} ({puntaje_dominante}/5)
        
        Perfil calculado por el sistema:
        {perfil}
        
        Promedio:
        {promedio}
        
        Informe base:
        {informe}
        
        Genera un informe motivador de aproximadamente 250 palabras.
        """
        )
            
        informe = respuesta_ia.output_text

        nuevo_usuario = {
            "nombre": nombre,
            "correo": correo,
            "apertura": apertura,
            "responsabilidad": responsabilidad,
            "extroversion": extroversion,
            "amabilidad": amabilidad,
            "neuroticismo": neuroticismo,
            "perfil": perfil,
            "promedio": promedio,
            "rasgo_dominante": rasgo_dominante,
            "puntaje_dominante": puntaje_dominante,
            "informe": informe
        }
        
        try:
            with open("usuarios.json", "r", encoding="utf-8") as archivo:
                usuarios = json.load(archivo)
        except:
            usuarios = []
            
        usuarios.append(nuevo_usuario)
        
        with open("usuarios.json", "w", encoding="utf-8") as archivo:
            json.dump(
                usuarios,
                archivo,
                indent=4,
                ensure_ascii=False
            ) 
        
        return render_template(
            
            "resultados.html",
            
            nombre=nombre,
            correo=correo,
            
            apertura=apertura,
            responsabilidad=responsabilidad,
            extroversion=extroversion,
            amabilidad=amabilidad,
            neuroticismo=neuroticismo,
            
            apertura_txt=interpretar(apertura),
            responsabilidad_txt=interpretar(responsabilidad),
            extroversion_txt=interpretar(extroversion),
            amabilidad_txt=interpretar(amabilidad),
            neuroticismo_txt=interpretar(neuroticismo),
            
            informe=informe,
            promedio=promedio,
            mayor=mayor,
            menor=menor,
            
            perfil=perfil,
            
            rasgo_dominante=rasgo_dominante,
            puntaje_dominante=puntaje_dominante,
            
            ranking=ranking,
            
            ultimo_rasgo=ultimo_rasgo,
            cola_actual=cola_actual,
            historial_respuestas=historial_respuestas
            
        )
        
@app.route('/usuarios')
def ver_usuarios():
    
    try:
        with open("usuarios.json", "r", encoding="utf-8") as archivo:
            usuarios = json.load(archivo)
                    
    except:
        usuarios = []
            
    return render_template(
        "usuarios.html",
        usuarios=usuarios
    )

if __name__ == '__main__':
    app.run(debug=True)
