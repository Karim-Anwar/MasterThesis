import torch
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np
from .networks.vit import ViT_BACKBONE as vit

def create_model(arch, heads, head_conv):
  if arch != 'vit':
    num_layers = int(arch[arch.find('_') + 1:]) if '_' in arch else 0
    arch = arch[:arch.find('_')] if '_' in arch else arch
    get_model = _model_factory[arch]
    model = get_model(num_layers=num_layers, heads=heads, head_conv=head_conv)
  elif arch =='vit':
    model = vit(
            width=1088,
            height=608,
            patch_size=32,
            dim=256,
            depth=6,
            heads=8,
            mlp_dim=1024,
            channels=3,
            dim_head=64,
            dropout=0.1,
            emb_dropout=0.1
        )
  return model


# Define the transformation for the input image
transform = transforms.Compose([
    transforms.Resize((608, 1088)),  # Resize to model's input size
    transforms.ToTensor(),  # Convert to tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize
])

# Load the trained model
def load_model(model_path):
    model = create_model('vit', None, None)  # Adjust parameters as per your model's create_model function
    checkpoint = torch.load(model_path, map_location='cpu')
    model.load_state_dict(checkpoint['state_dict'])
    model.eval()
    return model

# Preprocess the image
def preprocess_image(image_path):
    image = Image.open(image_path).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)  # Add batch dimension
    return image

# Postprocess the model's output (example for bounding boxes)
def postprocess_output(output):
    # Assuming output is a list of dictionaries as defined in the model's forward function
    output = output[0]
    hm = output['hm'].squeeze().sigmoid().detach().cpu().numpy()
    wh = output['wh'].squeeze().detach().cpu().numpy()
    reg = output['reg'].squeeze().detach().cpu().numpy()

    # Example: visualize the heatmap
    plt.imshow(hm[0], cmap='hot', interpolation='nearest')
    plt.show()

    # Example: extract bounding boxes from heatmap (for illustration only, needs proper implementation)
    threshold = 0.5
    bbox_indices = np.where(hm[0] > threshold)
    bboxes = []
    for y, x in zip(*bbox_indices):
        w, h = wh[:, y, x]
        center_x, center_y = x + reg[0, y, x], y + reg[1, y, x]
        bboxes.append([center_x - w / 2, center_y - h / 2, center_x + w / 2, center_y + h / 2])
    return bboxes

# Visualize bounding boxes on the image
def visualize_bboxes(image_path, bboxes):
    image = cv2.imread(image_path)
    for bbox in bboxes:
        x1, y1, x2, y2 = [int(coord) for coord in bbox]
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()

# Main function to evaluate the model
def evaluate_image(model_path, image_path):
    model = load_model(model_path)
    image = preprocess_image(image_path)
    with torch.no_grad():
        output = model(image)
    bboxes = postprocess_output(output)
    visualize_bboxes(image_path, bboxes)

# Example usage
model_path = 'FairMOT_ROOT/models/model_5.pth'
image_path = 'sanity/val/217_1_5.jpg'
evaluate_image(model_path, image_path)