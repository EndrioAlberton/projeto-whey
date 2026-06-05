const API_URL = process.env.API_URL || 'http://localhost:8000'

export async function getProdutos({ marca, sabor, tamanho, proteina_min, ordenar } = {}) {
  const params = new URLSearchParams()
  if (marca)        params.set('marca',       marca)
  if (sabor)        params.set('sabor',        sabor)
  if (tamanho)      params.set('peso_g',       tamanho)
  if (proteina_min) params.set('proteina_min', proteina_min)

  const url = `${API_URL}/api/produtos/?${params.toString()}`

  const res = await fetch(url, { cache: 'no-store' })
  if (!res.ok) return []

  const data = await res.json()
  return data.results ?? data
}

export async function getOpcoesFiltros() {
  const [marcas, sabores, tamanhos] = await Promise.all([
    fetch(`${API_URL}/api/marcas/`,    { cache: 'no-store' }).then(r => r.json()),
    fetch(`${API_URL}/api/sabores/`,   { cache: 'no-store' }).then(r => r.json()),
    fetch(`${API_URL}/api/tamanhos/`,  { cache: 'no-store' }).then(r => r.json()),
  ])
  return {
    marcas:   (marcas.results   ?? marcas).map(m => m.nome),
    sabores:  (sabores.results  ?? sabores).map(s => s.nome),
    tamanhos: (tamanhos.results ?? tamanhos).map(t => ({ peso_g: t.peso_g, rotulo: t.rotulo })),
  }
}
