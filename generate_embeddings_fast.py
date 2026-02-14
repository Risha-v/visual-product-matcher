import json
import os
from sentence_transformers import SentenceTransformer
from PIL import Image
from tqdm import tqdm

# ✅ Load CLIP model
model = SentenceTransformer("sentence-transformers/clip-ViT-B-32")

# ✅ JSON file
PRODUCTS_PATH = "more_products.json"

# ✅ Base directory where images are stored
IMAGE_BASE_PATH = r"D:\visual_product_matcher\assets\product"

with open(PRODUCTS_PATH, "r", encoding="utf-8") as f:
    products = json.load(f)

print("🔄 Generating CLIP image embeddings...")

for product in tqdm(products):
    try:
        # Image filename from JSON (example: "air-fryer.jpg")
        image_filename = product["image"]

        # Construct full absolute path
        image_path = os.path.join(IMAGE_BASE_PATH, image_filename)

        if not os.path.exists(image_path):
            print(f"⚠️ Image not found: {image_path}")
            continue

        # Load and encode image
        image = Image.open(image_path).convert("RGB")
        embedding = model.encode(image)

        # Store embedding
        product["embedding"] = embedding.tolist()

    except Exception as e:
        print(f"❌ Error processing {product.get('name')}: {e}")

# Save updated JSON
with open(PRODUCTS_PATH, "w", encoding="utf-8") as f:
    json.dump(products, f, indent=2)

print("✅ CLIP image embeddings generated successfully!")