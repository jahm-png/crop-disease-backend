# download_model.py
from huggingface_hub import hf_hub_download

# Replace with your model's repository ID and filename
repo_id = "premo625/Plant_disease_detection_cnn_model"
filename = "plant_disease_model.pth"  # Update with the correct filename

# Download the model
model_path = hf_hub_download(repo_id=repo_id, filename=filename)

print(f"Model downloaded to: {model_path}")
