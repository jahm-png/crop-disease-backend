from PIL import Image
import requests
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Disease
from .serializers import DiseaseSerializer

# Optional: Add treatment suggestions per disease
TREATMENT_DICT = {
    "Pepper__bell___Bacterial_spot": "Use copper-based bactericides and avoid overhead watering.",
    "Pepper__bell___healthy": "No treatment needed. Your crop is healthy.",
    "Potato___Early_blight": "Apply fungicides containing chlorothalonil or copper. Practice crop rotation.",
    "Potato___Late_blight": "Use fungicides like mancozeb or metalaxyl. Remove infected plants immediately.",
    "Potato___healthy": "No treatment needed. Your crop is healthy.",
    "Tomato_Bacterial_spot": "Remove infected leaves and apply copper-based fungicides.",
    "Tomato_Early_blight": "Use fungicides such as chlorothalonil. Avoid water splashing on leaves.",
    "Tomato_Late_blight": "Apply fungicides like mancozeb or chlorothalonil. Remove infected plants.",
    "Tomato_Leaf_Mold": "Ensure good air circulation. Use fungicides if necessary.",
    "Tomato_Septoria_leaf_spot": "Remove infected leaves and apply fungicides containing chlorothalonil.",
    "Tomato_Spider_mites_Two_spotted_spider_mite": "Spray with insecticidal soap or neem oil.",
    "Tomato__Target_Spot": "Apply fungicides like chlorothalonil or copper sprays.",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "Remove infected plants. Control whitefly populations with insecticides.",
    "Tomato__Tomato_mosaic_virus": "Remove infected plants and disinfect tools regularly.",
    "Tomato_healthy": "No treatment needed. Your crop is healthy."
}

# ---------- Weather API ---------- #
@api_view(['GET'])
def get_weather(request):
    city = request.GET.get('city', 'Nairobi')
    try:
        api_key = '3d508b4e5dbb45330a53e393e26cfc2d'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            weather = data['weather'][0]['description']
            return Response({
                'temperature': temperature,
                'humidity': humidity,
                'description': weather
            })
        return Response({'error': 'Unable to fetch weather info.'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# ---------- Symptom-Based Diagnosis (Function-based) ---------- #
@api_view(['POST'])
def diagnose(request):
    crop = request.data.get('crop_name')
    symptoms = request.data.get('symptoms')

    disease = Disease.objects.filter(crop_name__iexact=crop, symptoms__icontains=symptoms).first()
    
    if disease:
        return Response({
            'diagnosis': disease.disease_name,
            'treatment': disease.treatment
        })

    return Response({
        'diagnosis': 'No matching disease found.',
        'treatment': 'N/A'
    })

# ---------- Disease List ---------- #
class DiseaseList(APIView):
    def get(self, request):
        diseases = Disease.objects.all()
        serializer = DiseaseSerializer(diseases, many=True)
        return Response(serializer.data)

# ---------- Symptom-Based Diagnosis (Class-based) ---------- #
class SymptomDiagnosis(APIView):
    def post(self, request):
        crop = request.data.get('crop_name')
        symptoms = request.data.get('symptoms')

        disease = Disease.objects.filter(crop_name__iexact=crop, symptoms__icontains=symptoms).first()

        if disease:
            return Response({
                'diagnosis': disease.disease_name,
                'treatment': disease.treatment
            })

        return Response({
            'diagnosis': 'No matching disease found.',
            'treatment': 'N/A'
        })

# ---------- Add New Disease ---------- #
class AddDisease(APIView):
    def post(self, request):
        serializer = DiseaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Disease entry added successfully.',
                'disease': serializer.data
            }, status=201)
        return Response(serializer.errors, status=400)

# ---------- Image-Based Diagnosis (Lazy Model Load) ---------- #
class ImageDiagnosisView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES:
            return Response({'error': 'No image uploaded'}, status=400)

        try:
            from .model_loader import load_model  # Load only when needed
            model = load_model()

            image = Image.open(request.FILES['image']).convert('RGB')
            disease, confidence = model.predict(image)

            return Response({
                'diagnosis': disease.replace('_', ' '),
                'confidence': f"{confidence * 100:.2f}%",
                'treatment': TREATMENT_DICT.get(disease, 'Treatment information coming soon...'),
            })

        except Exception as e:
            return Response({'error': str(e)}, status=500)
