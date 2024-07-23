import cv2
import numpy as np
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
from FairMOT_ROOT.src.lib.models.networks.vit import ViT_BACKBONE as vit

def preprocess_image(image):
    # Preprocess the image as required by the model (resize, normalize, etc.)
    image = cv2.resize(image, (1088, 608))
    image = image.astype(np.float32) / 255.0
    image = torch.from_numpy(image).permute(2, 0, 1).unsqueeze(0)  # Convert to NCHW format
    return image

def overlay_heatmap(img, heatmap):
    # Resize heatmap to match image dimensions
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    # Normalize the heatmap to a range of 0 to 255
    heatmap = np.uint8(255 * heatmap)
    # Apply the colormap
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    # Overlay the heatmap on the image
    overlay = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)
    return overlay

def find_peaks(heatmap, threshold=0.4):
    # Apply Gaussian filter to the heatmap
    heatmap = cv2.GaussianBlur(heatmap, (3, 3), 0)
    
    # Apply max pooling to find local maxima
    heatmap_tensor = torch.from_numpy(heatmap).unsqueeze(0).unsqueeze(0)
    pooled_heatmap = F.max_pool2d(heatmap_tensor, kernel_size=3, stride=1, padding=1)
    
    # Elementwise comparison
    peaks = (heatmap_tensor == pooled_heatmap).float()
    
    # Elementwise multiplication to get peak confidence scores
    peak_heatmap = peaks * heatmap_tensor
    
    # Thresholding
    peak_heatmap = peak_heatmap * (peak_heatmap > threshold).float()
    
    return peak_heatmap.squeeze().numpy()

# Load your custom model (assuming it's already defined and loaded)
model = vit(
        width=1088,
        height=608,
        patch_size=16,
        dim=256,
        depth=6,
        heads=8,
        mlp_dim=1024,
        channels=3,
        dim_head=64,
        dropout=0.1,
        emb_dropout=0.1
    )

checkpoint = torch.load('FairMOT_ROOT/exp/mot/default/vit16x16E15_2024-07-19-12-13/model_15.pth')
pretrained_dict = checkpoint['state_dict']
model_dict = model.state_dict()
filtered_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict and model_dict[k].shape == v.shape}
model_dict.update(filtered_dict)
# Load the filtered state dictionary into your model
model.load_state_dict(model_dict)
model.eval()

# Read and preprocess the input image
image = cv2.imread('vif_frames/236_1/frame_0200.jpeg')
input_tensor = preprocess_image(image)

# Get the model prediction
with torch.no_grad():
    output = model(input_tensor)[0]  # Assuming the output is a dictionary

# Extract the heatmap from the model output
heatmap = output['hm'].squeeze().cpu().numpy()  # Assuming the heatmap is under 'hm' key and in NCHW format

# Normalize the heatmap for visualization
heatmap = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min())

# Find peaks in the heatmap
peak_heatmap = find_peaks(heatmap, threshold=0.4)

# Convert the original image to RGB format (from BGR)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Overlay the heatmap peaks on the image
overlayed_peaks = overlay_heatmap(image, peak_heatmap)

# Display the image with peaks overlay
plt.imshow(overlayed_peaks)
plt.axis('off')
plt.show()
