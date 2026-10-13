import { getProdutos } from '../lib/api'
import { slugify, SITE_URL } from '../lib/slug'

export const revalidate = 3600

export default async function sitemap() {
  const produtos = await getProdutos()
  const slugs = [...new Set(produtos.flatMap((p) => [p.marca, p.sabor]).map(slugify))]
  return [
    { url: SITE_URL },
    ...['sobre', 'contato', 'privacidade'].map((s) => ({ url: `${SITE_URL}/${s}` })),
    ...slugs.map((s) => ({ url: `${SITE_URL}/whey-barato/${s}` })),
  ]
}
