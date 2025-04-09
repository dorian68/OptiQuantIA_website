# website/views.py
from django.shortcuts import render
#from .models import CaseStudy
from django.http import JsonResponse
from django.http import HttpResponse
from .models import UploadedFile
from django.shortcuts import redirect
from .forms import UploadedFileForm, RiskSimlatorfielsForm
from .models import UploadedFile
from django.core.files.storage import default_storage
import pandas as pd
import numpy as np
import json
import os
from website.utils.cls_ExcelToHTML import ExcelToHTML
import requests
from django.views.decorators.csrf import csrf_exempt


# Remplace par l'URL de ton webhook n8n
#N8N_WEBHOOK_URL = "https://dorian68.app.n8n.cloud/webhook/b093723a-24b8-429a-a39e-406dfd7f82f7/chat"
#N8N_WEBHOOK_URL = "https://dorian68.app.n8n.cloud/webhook/2c789570-fd97-4855-9cd1-3b0487af00d9/chat"
N8N_WEBHOOK_URL = "https://dorian68.app.n8n.cloud/webhook/ed35d1bb-ca5c-4bf0-adb5-08b62f756f05"


@csrf_exempt  # Désactive temporairement la protection CSRF (utile si API externe)
def chatbot_view(request):
    if request.method != "POST":
        print(request.body)
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()

        if not user_message:
            return JsonResponse({"error": "Message vide"}, status=400)

        print(f"[LOG] Message reçu: {user_message}")

        # Envoyer la requête à n8n
        response = requests.post(N8N_WEBHOOK_URL, json={"message": user_message})

        if response.status_code == 200:
            chatbot_reply = response.json().get("reply", "Réponse vide de l'IA")
            print(f"[LOG] Réponse de n8n: {chatbot_reply}")
            return JsonResponse({"reply": chatbot_reply})
        else:
            print(f"[ERROR] n8n a retourné une erreur: {response.status_code} - {response.text}")
            return JsonResponse({"error": f"Erreur avec n8n (status: {response.status_code})"}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Requête invalide (JSON mal formé)"}, status=400)
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Problème de connexion à n8n : {e}")
        return JsonResponse({"error": "Impossible de contacter n8n"}, status=500)


def upload_file(request):
    data = None  # Pour stocker les données traitées
    print("Uploaded_file called")
    try:
        if request.method == 'POST':
            form = UploadedFileForm(request.POST, request.FILES)

            if 'csv_file' in request.FILES:
                if form.is_valid():
                    uploaded_file = form.save()  # Enregistre le fichier en base
                    file_path = uploaded_file.file.path  # Récupère le chemin du fichier
                            # Charger le fichier dans un DataFrame pandas
                
                    if file_path.endswith('.csv'):
                        data = pd.read_csv(file_path)
                    elif file_path.endswith(('.xls', '.xlsx')):
                        data = pd.read_excel(file_path)

                    # Convertir en HTML pour affichage
                    data_html = data.head(10).to_html(classes="table table-striped")

                    # Extraire les colonnes pour les charger dans un combobox
                    columns = data.columns.tolist()  

                    # Enregistrer les données CSV temporairement pour la session ou base de données
                    uploaded_csv = UploadedFile.objects.create(file=file_path)

                    return render(request, 'report.html', {'data': data_html,"columns": columns, "df_json": data.to_json(orient="records")})
            elif 'column_choices' in request.POST:
                # formule avec les colonnes choisies
                formSelect = RiskSimlatorfielsForm(request.POST)
                if formSelect.valid():
                    selected_columns = formSelect.cleaned_data
                    return render(request, 'upload.html', {'form': form})

    except Exception as e:
        return render(request, 'upload.html', {'form': form, 'error': str(e)})

def home2(request):
    return render(request, 'home2.html')

def about(request):
    return render(request, 'aPropos.html')

def articles(request):
    return render(request,'articles.html')

def services(request):
    return render(request, 'services.html')

def service_analysis(request):
    return render(request, 'service_analysis.html')

def service_dev_tool(request):
    return render(request, 'service_dev_tool.html')

def service_data_management(request):
    return render(request, 'service_data_management.html')

def corpoFinance(request):
    return render(request, 'corpoFinance.html')

def contact(request):
    return render(request, 'contact.html')

def rates_analysis(request):
    return render(request, 'ratesAnalysis.html')

def meanReversion(request):
    return render(request, 'meanReversion.html')

from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadedFileForm
from .models import UploadedFile
import pandas as pd
from django.conf import settings

def tool_risk_calculator(request):
    form = UploadedFileForm()
    report_list = ["Reporting de performances", "Simulateur de risques", "Prévision de trésorie"]
    
    if request.method == "POST":  
        file = request.FILES.get("file")
        allowed_types = ['text/csv', 'text/plain', 'application/vnd.ms-excel'] 

        #if file.content_type in allowed_types:
        if not file is None:
            form = UploadedFileForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = form.save()
                print("------------------------------------------------------")
                print(f"uploaded_file type is {type(uploaded_file)}")
                print(f"uploaded_file is {uploaded_file}")
                print("------------------------------------------------------")
                file_path = uploaded_file.file.path  # Récupère le chemin du fichier
                # Charger le fichier dans un DataFrame pandas
                if file_path.endswith('.csv'):
                    data = pd.read_csv(file_path)
                elif file_path.endswith(('.xls', '.xlsx')):
                    data = pd.read_excel(file_path)
                
                # Sauvegarde le fichier en session
                request.session['csv_file_path'] = file_path

                # Sauvegarde le fichier en session
                request.session['file_id'] = uploaded_file.id

                # Convertir en HTML pour affichage
                data_html = data.head(10).to_html(classes="table table-striped")

                # Extraire les colonnes pour les charger dans un combobox
                columns = data.columns.tolist()  
                return render(request, "riskCalculator.html", {"form": form, "columns": columns,"df_json": data.to_json(orient="records")})
        elif file is None:
            file_path = request.session.get('csv_file_path', None)
            file_id = request.session.get('file_id')

            # Get fields choosen by the user
            context = {
                "column_labels" : request.POST.get("column_labels"),
                "index_labels" : request.POST.get("index_labels"),
                "value_labels" : request.POST.get("value_labels"),
            }

            context = request.POST.dict()  # Convertit les données POST en dictionnaire
            request.session["context"] = context  # Stocker en session
              
            print("------------------------------------------------------")
            print(f"file_path type is {type(file_path)}")
            print(f"file_id is {file_id}")
            print("------------------------------------------------------")
            return redirect("process_file", file_id=file_id)  # Redirection après upload
    return render(request, "riskCalculator.html", {"form": form, "report_list": report_list})

def process_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    file_path = uploaded_file.file.path
    context = request.session.get("context", {})  # Récupère le contexte stocké en session
    # Détection automatique du format
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        else:
            return render(request, "error.html", {"message": "Format de fichier non pris en charge."})

        # Vérification si le DataFrame est vide
        if df.empty:
            print("df is empty")
            return render(request, "error.html", {"message": "Le fichier est vide ou mal formaté."})
        
        html_table_perso = ""
        dev = True

        # Supposons que df existe déjà
        n,mu,sigma,dt  = len(df),150,1,1 

        # Génération du mouvement brownien
        brownian_motion = np.cumsum(np.random.normal(mu * dt, sigma * np.sqrt(dt), n))

        # Ajout au DataFrame sous une nouvelle colonne
        df["values"] = brownian_motion

        # Shrink our dataframe
        df = df.head(7)

        df_input = ExcelToHTML(df,style={"border": "2px solid skyblue","width":"auto","white-space": "nowrap"})

        # work on user inputs then transforms to html
        #html_table_perso = df_input.to_html()

        # Convertir le DataFrame en HTML
        #table_html = df.to_html(classes="table table-striped", index=False)
        

        # Choisir une colonne à afficher (ex: la première colonne comme labels)
        labels = df.iloc[:, 0].astype(str).tolist()
        values = df["values"].tolist() # Deuxième colonne pour les valeurs

        # Convertir les données en JSON pour JavaScript
        index_labels = [context["index_labels"]]
        column_labels=[context["column_labels"]]
        value_labels =[context["value_labels"]]

        context = {
            "table_html": df_input.generate_pivot_html(index_labels, column_labels, value_labels),
            "labels_json": json.dumps(labels),  # Convertir en JSON
            "values_json": json.dumps(values),  # Convertir en JSON
        }
        default_storage.delete(file_path)
        return render(request, "report.html", context)

    except Exception as e:
        return render(request, "error.html", {"message": f"Erreur lors du traitement du fichier : {e}"})

def riskCalculator_report(request):
    file_path = os.path.join(settings.BASE_DIR, 'media', 'uploads/orders_trainTEMP.csv')
    df_data = pd.read_csv(file_path, sep=',')
    df_data = df_data.head()
    columns = list(df_data.columns)
    print(columns)
    # Conversion du DataFrame en JSON
    data = df_data.to_dict(orient='records')
    data_json = json.dumps(data)

    return render(request, "riskCalculator_report.html", { "data_json" : data_json, "col" : columns }) 

def article_automation_for_small_business(request):
    return render(request, 'article_automation_for_small_business.html')

def article_ml_for_small_business(request):
    return render(request, 'article_ml_for_small_business.html')

def article_risk_management(request):
    return render(request, 'article_risk_management.html')

def article_automation_email_sending(request):
    return render(request, 'article_automation_email_sending.html')

def riskCalculator_frontPage(request):
    return render(request, 'riskCalculator_frontPage.html')

def chart_data(request):
    # Exemple de données pour la courbe
    data = {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "datasets": [
            {
                "label": "Ventes",
                "data": [12, 19, 3, 5, 2, 3],
                "borderColor": "rgba(75, 192, 192, 1)",
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "fill": True
            }
        ]
    }
    return JsonResponse(data)

def chart_view(request):
    return render(request, "chart.html")



