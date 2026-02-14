// removeEmbeddings.ts
import fs from "fs";

const products = JSON.parse(fs.readFileSync("server/products.json", "utf-8"));

const cleaned = products.map((p: any) => {
  delete p.embedding;
  return p;
});

fs.writeFileSync("server/products.json", JSON.stringify(cleaned, null, 2));

console.log("✅ Demo embeddings removed.");
