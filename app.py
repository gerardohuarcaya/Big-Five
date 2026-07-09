from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

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
            Eres un psicólogo experto en psicometría y el modelo Big Five.
            Tu tarea es transformar el siguiente informe en un análisis profesional,
            claro, humano y motivador.
            No cambies el significado, solo mejora la redacción.
            
            INFORME:
            {informe}
            """
        )
            
        informe = respuesta_ia.output_text
            
        return render_template(
            'resultados.html',
                
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
                
            informe=informe
                
        )


if __name__ == '__main__':
    app.run(debug=True)
