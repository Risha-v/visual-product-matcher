import { Product } from "../types";

const API_URL = import.meta.env.VITE_API_URL;

export const searchProducts = async (
  imageData: string,
  isUrl: boolean = false
): Promise<Product[]> => {
  try {
    const payload: any = {};

    if (isUrl) {
      payload.imageUrl = imageData;
    } else {
      payload.image = imageData;
    }

    const response = await fetch(`${API_URL}/match`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.error || `Server error: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    if (error instanceof TypeError && error.message.includes("fetch")) {
      throw new Error(
        "Cannot connect to server. Please make sure the backend is running on port 5000."
      );
    }
    throw error;
  }
};

export const healthCheck = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
};
