import torch
import torch.onnx
import torch.nn as nn
from torchvision.models import resnet101
from arcface_onnx import ArcFaceONNX

# Load the model (assuming the model architecture is defined)
model = ArcFaceONNX()  # Replace with your actual model class
model.load_state_dict(torch.load("arcface_final_1.pth"))
model.eval()

# Dummy input for export (match the model's expected input size)
dummy_input = torch.randn(1, 3, 112, 112)  # Example for a 224x224 image with 3 channels

# Export the model
torch.onnx.export(
    model,                    # Model to export
    dummy_input,               # Dummy input to trace the model
    "model.onnx",              # Path to save the ONNX model
    export_params=True,        # Store model weights inside the ONNX file
    opset_version=11,          # ONNX opset version (adjust if needed)
    input_names=['input'],     # Input layer name
    output_names=['output']    # Output layer name
)

print("Model successfully exported to ONNX format.")
