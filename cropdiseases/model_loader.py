import torch
from torchvision import models, transforms
from PIL import Image

class PlantDiseaseModel:
    def __init__(self, model_path):
        self.class_names = [
            "Pepper__bell___Bacterial_spot",
            "Pepper__bell___healthy",
            "Potato___Early_blight",
            "Potato___Late_blight",
            "Potato___healthy",
            "Tomato_Bacterial_spot",
            "Tomato_Early_blight",
            "Tomato_Late_blight",
            "Tomato_Leaf_Mold",
            "Tomato_Septoria_leaf_spot",
            "Tomato_Spider_mites_Two_spotted_spider_mite",
            "Tomato__Target_Spot",
            "Tomato__Tomato_YellowLeaf__Curl_Virus",
            "Tomato__Tomato_mosaic_virus",
            "Tomato_healthy"
        ]

        self.model = models.mobilenet_v2(pretrained=False)
        self.model.classifier[1] = torch.nn.Linear(self.model.last_channel, 15)

        state_dict = torch.load(model_path, map_location='cpu')
        self.model.load_state_dict(state_dict)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def predict(self, image: Image.Image):
        image = self.transform(image).unsqueeze(0)

        with torch.no_grad():
            outputs = self.model(image)
            probs = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probs, 1)

        return self.class_names[predicted.item()], confidence.item()

def load_model():
    return PlantDiseaseModel('cropdiseases/plant_disease_model.pth')
