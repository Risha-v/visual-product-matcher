import { Product } from "../types";
import ProductCard from "./ProductCard";

export default function ProductGrid({ products }: { products: Product[] }) {
  return (
    <div>
      {/* Grid Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">
          Similar Products
        </h2>
        <p className="text-gray-600 mt-1">
          Showing {products.length} {products.length === 1 ? "product" : "products"} sorted by similarity
        </p>
      </div>

      {/* Product Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}