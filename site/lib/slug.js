export const SITE_URL = process.env.SITE_URL || 'https://whey.endrioalberton.com.br'

export const slugify = (s) =>
  s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')

// Uma rota só serve marca e sabor. Marca tem prioridade se o slug colidir.
export async function resolverSlug(slug, getOpcoes) {
  const { marcas, sabores } = await getOpcoes()
  const marca = marcas.find((m) => slugify(m) === slug)
  if (marca) return { tipo: 'marca', nome: marca }
  const sabor = sabores.find((s) => slugify(s) === slug)
  if (sabor) return { tipo: 'sabor', nome: sabor }
  return null
}
