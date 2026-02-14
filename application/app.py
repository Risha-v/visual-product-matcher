from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import torch
import clip
import numpy as np
import json
import io
import base64
import requests
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Load CLIP model for visual similarity
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Load products database
products_path = Path(__file__).parent / "products.json"
with open(products_path, "r", encoding="utf-8") as f:
    products = json.load(f)

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def get_image_embedding(image):
    """Generate CLIP embedding for an image"""
    try:
        image_input = preprocess(image).unsqueeze(0).to(device)
        with torch.no_grad():
            image_features = model.encode_image(image_input)
            image_features /= image_features.norm(dim=-1, keepdim=True)
        return image_features.cpu().numpy().flatten()
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def get_text_embedding(text):
    """Generate CLIP embedding for text"""
    try:
        text_input = clip.tokenize([text]).to(device)
        with torch.no_grad():
            text_features = model.encode_text(text_input)
            text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features.cpu().numpy().flatten()
    except Exception as e:
        print(f"Error generating text embedding: {e}")
        return None

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "model": "CLIP ViT-B/32"})

@app.route("/match", methods=["POST"])
def match_products():
    """Match products based on uploaded image or URL"""
    try:
        data = request.json
        image = None
        query_embedding = None

        # Handle base64 image upload
        if "image" in data and data["image"]:
            try:
                # Remove data URL prefix if present
                image_data = data["image"]
                if "base64," in image_data:
                    image_data = image_data.split("base64,")[1]
                
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                query_embedding = get_image_embedding(image)
            except Exception as e:
                return jsonify({"error": f"Invalid image data: {str(e)}"}), 400

        # Handle image URL
        elif "imageUrl" in data and data["imageUrl"]:
            try:
                response = requests.get(data["imageUrl"], timeout=10)
                response.raise_for_status()
                image = Image.open(io.BytesIO(response.content)).convert("RGB")
                query_embedding = get_image_embedding(image)
            except Exception as e:
                return jsonify({"error": f"Failed to fetch image from URL: {str(e)}"}), 400

        # Handle text query (fallback)
        elif "query" in data and data["query"]:
            query_embedding = get_text_embedding(data["query"])

        if query_embedding is None:
            return jsonify({"error": "No valid input provided"}), 400

        # Calculate similarity with all products
        results = []
        for product in products:
            if "embedding" in product:
                similarity = cosine_similarity(query_embedding, product["embedding"])
                results.append({
                    "id": product["id"],
                    "name": product["name"],
                    "category": product["category"],
                    "description": product["description"],
                    "image": product["image"],
                    "similarity": float(similarity)
                })

        # Sort by similarity and return top 50
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return jsonify(results[:50])

    except Exception as e:
        print(f"Error in match_products: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/products", methods=["GET"])
def get_products():
    """Get all products"""
    return jsonify(products[:50])

if __name__ == "__main__":
    print(f"🚀 Server starting on http://localhost:5000")
    print(f"📊 Loaded {len(products)} products")
    print(f"🎨 Using device: {device}")
    app.run(host="0.0.0.0", port=5000, debug=True)