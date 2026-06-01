export const products = [
  { id: 1, brand: "Growth", name: "Whey Protein Concentrado", platform: "ML",     price: 89.90,  weight_g: 1000, dose_g: 30, protein_g: 22, flavor: "Baunilha",  affiliate_url: "#", image_url: "" },
  { id: 2, brand: "Max Titanium", name: "Top Whey 3W",          platform: "AMZ",   price: 129.90, weight_g: 900,  dose_g: 30, protein_g: 23, flavor: "Chocolate", affiliate_url: "#", image_url: "" },
  { id: 3, brand: "Integralmédica", name: "Nutri Whey Isolado", platform: "ML",    price: 159.90, weight_g: 907,  dose_g: 30, protein_g: 25, flavor: "Morango",   affiliate_url: "#", image_url: "" },
  { id: 4, brand: "Dux", name: "Whey 100%",                     platform: "AMZ",   price: 99.90,  weight_g: 900,  dose_g: 30, protein_g: 24, flavor: "Cookies",   affiliate_url: "#", image_url: "" },
  { id: 5, brand: "Probiótica", name: "100% Pure Whey",         platform: "ML",    price: 119.90, weight_g: 900,  dose_g: 35, protein_g: 24, flavor: "Baunilha",  affiliate_url: "#", image_url: "" },
  { id: 6, brand: "Black Skull", name: "Whey 80% Concentrado",  platform: "AMZ",   price: 94.90,  weight_g: 900,  dose_g: 30, protein_g: 21, flavor: "Chocolate", affiliate_url: "#", image_url: "" },
  { id: 7, brand: "New Millen", name: "100% Pure Whey",         platform: "ML",    price: 109.90, weight_g: 900,  dose_g: 30, protein_g: 24, flavor: "Baunilha",  affiliate_url: "#", image_url: "" },
  { id: 8, brand: "Atlhetica", name: "Nutrition Whey",          platform: "AMZ",   price: 134.90, weight_g: 850,  dose_g: 32, protein_g: 25, flavor: "Cookies",   affiliate_url: "#", image_url: "" },
]

export function calcProduct(p) {
  const servings = Math.floor(p.weight_g / p.dose_g) || 1
  const cost_per_dose = p.price / servings
  const total_protein = p.protein_g * servings
  const cost_per_30g_protein = (p.price / total_protein) * 30
  return { ...p, servings, cost_per_dose, total_protein, cost_per_30g_protein }
}

export function slugify(p) {
  return `${p.brand}-${p.name}-${p.weight_g}g-${p.flavor}`
    .toLowerCase()
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
}

export function getProducts() {
  return products.map((p) => ({ ...calcProduct(p), slug: slugify(p) }))
}
