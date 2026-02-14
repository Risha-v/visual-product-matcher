import { Product } from "../types";
import { useState } from "react";

export default function ProductCard({ product }: { product: Product }) {
  const [imageError, setImageError] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(false);

  const getSimilarityColor = (similarity: number) => {
    if (similarity >= 0.8) return "bg-green-100 text-green-800 border-green-200";
    if (similarity >= 0.6) return "bg-blue-100 text-blue-800 border-blue-200";
    if (similarity >= 0.4) return "bg-yellow-100 text-yellow-800 border-yellow-200";
    return "bg-gray-100 text-gray-800 border-gray-200";
  };

  return (
    <div className="group bg-white rounded-xl shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-200 hover:border-blue-300 flex flex-col h-full">

      {/* Image */}
      <div className="relative w-full h-56 bg-gray-100 overflow-hidden">

        {!imageLoaded && !imageError && (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-8 h-8 border-4 border-gray-300 border-t-blue-600 rounded-full animate-spin"></div>
          </div>
        )}

        {!imageError ? (
          <img
            src={product.image}
            alt={product.name}
            onLoad={() => setImageLoaded(true)}
            onError={() => setImageError(true)}
            className={`w-full h-full object-cover transition-all duration-300 group-hover:scale-110 ${
              imageLoaded ? "opacity-100" : "opacity-0"
            }`}
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-100">
            <div className="text-center">
              <p className="text-sm text-gray-500">Image unavailable</p>
            </div>
          </div>
        )}

        {/* Similarity Badge */}
        <div className="absolute top-3 right-3">
          <div className={`px-3 py-1.5 rounded-full text-xs font-semibold border backdrop-blur-sm ${getSimilarityColor(product.similarity)}`}>
            {(product.similarity * 100).toFixed(0)}%
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4 flex-1 flex flex-col">
        <h3 className="font-semibold text-gray-900 text-base mb-1 line-clamp-2">
          {product.name}
        </h3>

        <div className="text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded-full inline-block mb-2 w-fit">
          {product.category}
        </div>

        <p className="text-sm text-gray-600 line-clamp-2 mb-3 flex-1">
          {product.description}
        </p>

        <div className="mt-auto pt-3 border-t border-gray-100">
          <div className="w-full bg-gray-200 rounded-full h-1.5 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all duration-500 rounded-full"
              style={{ width: `${product.similarity * 100}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}