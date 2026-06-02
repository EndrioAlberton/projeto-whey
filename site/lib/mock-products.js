export const produtos = [
  { id: 1, marca: "Growth",        nome: "Whey Protein Concentrado", plataforma: "ML",  preco: 89.90,  peso_g: 1000, dose_g: 30, proteina_g: 22, sabor: "Baunilha",  url_afiliado: "#", url_imagem: "" },
  { id: 2, marca: "Max Titanium",  nome: "Top Whey 3W",              plataforma: "AMZ", preco: 129.90, peso_g: 900,  dose_g: 30, proteina_g: 23, sabor: "Chocolate", url_afiliado: "#", url_imagem: "" },
  { id: 3, marca: "Integralmédica",nome: "Nutri Whey Isolado",       plataforma: "ML",  preco: 159.90, peso_g: 907,  dose_g: 30, proteina_g: 25, sabor: "Morango",   url_afiliado: "#", url_imagem: "" },
  { id: 4, marca: "Dux",           nome: "Whey 100%",                plataforma: "AMZ", preco: 99.90,  peso_g: 900,  dose_g: 30, proteina_g: 24, sabor: "Cookies",   url_afiliado: "#", url_imagem: "" },
  { id: 5, marca: "Probiótica",    nome: "100% Pure Whey",           plataforma: "ML",  preco: 119.90, peso_g: 900,  dose_g: 35, proteina_g: 24, sabor: "Baunilha",  url_afiliado: "#", url_imagem: "" },
  { id: 6, marca: "Black Skull",   nome: "Whey 80% Concentrado",     plataforma: "AMZ", preco: 94.90,  peso_g: 900,  dose_g: 30, proteina_g: 21, sabor: "Chocolate", url_afiliado: "#", url_imagem: "" },
  { id: 7, marca: "New Millen",    nome: "100% Pure Whey",           plataforma: "ML",  preco: 109.90, peso_g: 900,  dose_g: 30, proteina_g: 24, sabor: "Baunilha",  url_afiliado: "#", url_imagem: "" },
  { id: 8, marca: "Atlhetica",     nome: "Nutrition Whey",           plataforma: "AMZ", preco: 134.90, peso_g: 850,  dose_g: 32, proteina_g: 25, sabor: "Cookies",   url_afiliado: "#", url_imagem: "" },
]

export function calcProduto(p) {
  const doses               = Math.floor(p.peso_g / p.dose_g) || 1
  const custo_por_dose      = p.preco / doses
  const proteina_total      = p.proteina_g * doses
  const custo_por_30g_proteina = (p.preco / proteina_total) * 30
  return { ...p, doses, custo_por_dose, proteina_total, custo_por_30g_proteina }
}

export function slugify(p) {
  return `${p.marca}-${p.nome}-${p.peso_g}g-${p.sabor}`
    .toLowerCase()
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
}

export function getProdutos() {
  return produtos.map((p) => ({ ...calcProduto(p), slug: slugify(p) }))
}
