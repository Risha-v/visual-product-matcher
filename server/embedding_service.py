from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
from PIL import Image
import requests
import json
import numpy as np
import io
import base64
import os
import re

app = Flask(__name__)
CORS(app)

# -----------------------------
# CONFIGURATION
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "assets", "product")
PRODUCTS_PATH = os.path.join(BASE_DIR, "products.json")

model = SentenceTransformer("sentence-transformers/clip-ViT-B-32")

# Load products
with open(PRODUCTS_PATH, "r", encoding="utf-8") as f:
    products = json.load(f)


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def load_image_from_base64(data_string):
    image_bytes = base64.b64decode(data_string.split(",")[-1])
    return Image.open(io.BytesIO(image_bytes)).convert("RGB")


def extract_unsplash_direct_url(page_url):
    try:
        html = requests.get(page_url, timeout=10).text
        match = re.search(r'https://images\.unsplash\.com[^"]+', html)
        if match:
            return match.group(0)
        return None
    except:
        return None


def load_image_from_url(url):
    # Handle base64 mistakenly passed in URL field
    if url.startswith("data:image"):
        return load_image_from_base64(url)

    # Handle Unsplash page links
    if "unsplash.com/photos" in url:
        direct_url = extract_unsplash_direct_url(url)
        if direct_url:
            url = direct_url

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return Image.open(io.BytesIO(response.content)).convert("RGB")


# -----------------------------
# ROUTES
# -----------------------------

@app.route("/images/<path:filename>")
def serve_image(filename):
    try:
        return send_from_directory(IMAGE_FOLDER, filename)
    except Exception:
        return jsonify({"error": f"Image not found: {filename}"}), 404


@app.route("/match", methods=["POST"])
def match():
    try:
        data = request.json

        image_data = data.get("image")
        image_url = data.get("imageUrl")

        if not image_data and not image_url:
            return jsonify({"error": "No image provided"}), 400

        # Load query image
        if image_data:
            image = load_image_from_base64(image_data)
        else:
            image = load_image_from_url(image_url)

        query_embedding = model.encode(image)

        results = []

        for product in products:
            if "embedding" not in product:
                continue

            score = cosine_similarity(query_embedding, product["embedding"])

            results.append({
                **product,
                "image": f"http://localhost:5000/images/{product['image']}",
                "similarity": score
            })

        results.sort(key=lambda x: x["similarity"], reverse=True)

        return jsonify(results[:20])

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
