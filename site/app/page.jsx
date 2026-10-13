import { Suspense } from 'react'
import { getProdutos, getOpcoesFiltros } from '../lib/api'
import CatalogClient from '../components/CatalogClient'
import SiteHeader from '../components/SiteHeader'
import { SITE_URL } from '../lib/slug'

export const metadata = {
  title: 'WheyMais — Melhores wheys do Brasil por custo de proteína',
  description: 'Compare os melhores wheys do Brasil pelo custo por 30g de proteína. Filtre por marca, sabor e tamanho.',
  alternates: { canonical: '/' },
}

export default async function Home() {
  const [produtos, opcoes] = await Promise.all([
    getProdutos(),
    getOpcoesFiltros(),
  ])

  return (
    <main className="wrap">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
        '@context': 'https://schema.org', '@type': 'WebSite', name: 'WheyMais', url: SITE_URL, inLanguage: 'pt-BR',
      }) }} />
      <SiteHeader />

      <h1 style={{ fontSize: 14, color: 'var(--mut)', fontWeight: 400, marginBottom: 18 }}>
        Compare {produtos.length} wheys pelo <strong style={{ color: 'var(--lime)' }}>custo por 30g de proteína</strong>
      </h1>

      <Suspense fallback={<div className="empty">Carregando...</div>}>
        <CatalogClient produtos={produtos} opcoes={opcoes} />
      </Suspense>

      <p style={{ marginTop: 40, fontSize: 11, color: 'var(--mut)', lineHeight: 1.6 }}>
        * Links marcados com "Comprar" são links de afiliado — recebemos uma comissão se você comprar pelo link, sem custo adicional para você.
      </p>
    </main>
  )
}
