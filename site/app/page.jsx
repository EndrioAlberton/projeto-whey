import { Suspense } from 'react'
import { Zap } from 'lucide-react'
import { getProducts } from '../lib/mock-products'
import CatalogClient from '../components/CatalogClient'
import ThemeToggle from '../components/ThemeToggle'

export const metadata = {
  title: 'WheyMais — Melhores wheys do Brasil por custo de proteína',
  description: 'Compare os melhores wheys do Brasil pelo custo por 30g de proteína. Filtros por marca, sabor e proteína mínima. Preços atualizados diariamente.',
}

export default function Home() {
  const products = getProducts()

  return (
    <main className="wrap">
      <header>
        <div className="logo">
          <Zap size={26} color="var(--lime)" fill="var(--lime)" />
          <b>Whey<span className="x">Mais</span></b>
          <span className="badge-lab">custo por proteína</span>
        </div>
        <ThemeToggle />
      </header>

      <h1 style={{ fontSize: 14, color: 'var(--mut)', fontWeight: 400, marginBottom: 18 }}>
        Compare {products.length} wheys pelo <strong style={{ color: 'var(--lime)' }}>custo por 30g de proteína</strong>
      </h1>

      <Suspense fallback={<div className="empty">Carregando...</div>}>
        <CatalogClient products={products} />
      </Suspense>

      <p style={{ marginTop: 40, fontSize: 11, color: 'var(--mut)', lineHeight: 1.6 }}>
        * Links marcados com "Comprar" são links de afiliado — recebemos uma comissão se você comprar pelo link, sem custo adicional para você.
      </p>
    </main>
  )
}
