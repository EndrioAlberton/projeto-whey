import { getOpcoesFiltros } from '../lib/api'
import { slugify, SITE_URL } from '../lib/slug'

export const revalidate = 3600

export default async function sitemap() {
  const { marcas, sabores } = await getOpcoesFiltros()
  const slugs = [...new Set([...marcas, ...sabores].map(slugify))]
  return [
    { url: SITE_URL },
    ...slugs.map((s) => ({ url: `${SITE_URL}/whey-barato/${s}` })),
  ]
}
