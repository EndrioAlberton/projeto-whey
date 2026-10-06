import { notFound } from 'next/navigation'
import Link from 'next/link'
import { getProdutos, getOpcoesFiltros } from '../../../lib/api'
import { resolverSlug, SITE_URL } from '../../../lib/slug'
import ProductCard from '../../../components/ProductCard'

export const revalidate = 3600

const titulo = ({ tipo, nome }) =>
  tipo === 'marca' ? `Whey ${nome} barato: ranking por custo de proteína` : `Whey sabor ${nome}: os mais baratos por proteína`

export async function generateMetadata({ params }) {
  const alvo = await resolverSlug(params.slug, getOpcoesFiltros)
  if (!alvo) return {}
  const t = titulo(alvo)
  return {
    title: `${t} | WheyMais`,
    description: `Compare os wheys ${alvo.tipo === 'marca' ? 'da ' : 'sabor '}${alvo.nome} pelo custo por 30g de proteína. Preços atualizados.`,
    alternates: { canonical: `${SITE_URL}/whey-barato/${params.slug}` },
  }
}

export default async function Page({ params }) {
  const alvo = await resolverSlug(params.slug, getOpcoesFiltros)
  if (!alvo) notFound()

  const todos = await getProdutos()
  const lista = todos
    .filter((p) => p[alvo.tipo] === alvo.nome && p.custo_por_30g_proteina != null)
    .sort((a, b) => a.custo_por_30g_proteina - b.custo_por_30g_proteina)

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: titulo(alvo),
    itemListElement: lista.map((p, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      item: {
        '@type': 'Product',
        name: p.nome,
        brand: { '@type': 'Brand', name: p.marca },
        offers: { '@type': 'Offer', price: p.preco, priceCurrency: 'BRL', url: p.url_afiliado || p.url_produto },
      },
    })),
  }

  return (
    <main className="wrap">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <p style={{ fontSize: 12, marginBottom: 12 }}><Link href="/">← WheyMais</Link></p>
      <h1 style={{ fontSize: 22, marginBottom: 6 }}>{titulo(alvo)}</h1>
      <p style={{ fontSize: 14, color: 'var(--mut)', marginBottom: 18 }}>
        {lista.length} produtos ordenados do menor para o maior custo por 30g de proteína.
      </p>
      <div className="grid">
        {lista.map((p, i) => <ProductCard key={p.id} produto={p} isMelhor={i === 0} />)}
        {!lista.length && <div className="empty">Nenhum produto encontrado.</div>}
      </div>
    </main>
  )
}
