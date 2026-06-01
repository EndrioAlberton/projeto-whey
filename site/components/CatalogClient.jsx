'use client'

import { useState, useMemo, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import { SlidersHorizontal } from 'lucide-react'
import ProductCard from './ProductCard'

const SORT_OPTIONS = [
  { value: 'p30',   label: 'Melhor custo por proteína' },
  { value: 'dose',  label: 'Menor custo por dose' },
  { value: 'price', label: 'Menor preço' },
  { value: 'prot',  label: 'Mais proteína por dose' },
]

const sorters = {
  p30:   (a, b) => a.cost_per_30g_protein - b.cost_per_30g_protein,
  dose:  (a, b) => a.cost_per_dose - b.cost_per_dose,
  price: (a, b) => a.price - b.price,
  prot:  (a, b) => b.protein_g - a.protein_g,
}

// Agrupa peso em baldes legíveis: ~900g, ~1kg, ~2kg
function sizeBucket(weight_g) {
  if (weight_g >= 1800) return '2000'
  if (weight_g >= 950)  return '1000'
  return '900'
}

export default function CatalogClient({ products }) {
  const params = useSearchParams()

  const [fBrand,   setFBrand]   = useState('')
  const [fFlavor,  setFFlavor]  = useState('')
  const [fSize,    setFSize]    = useState('')
  const [fMinProt, setFMinProt] = useState(0)
  const [sort,     setSort]     = useState('p30')

  // Inicializa filtros a partir dos query params
  useEffect(() => {
    if (params.get('brand'))  setFBrand(params.get('brand'))
    if (params.get('flavor')) setFFlavor(params.get('flavor'))
    if (params.get('size'))   setFSize(params.get('size'))
    if (params.get('sort'))   setSort(params.get('sort'))
  }, [params])

  const brands  = [...new Set(products.map((p) => p.brand))]
  const flavors = [...new Set(products.map((p) => p.flavor))]

  const view = useMemo(() => {
    return [...products]
      .filter((p) =>
        (!fBrand  || p.brand  === fBrand)  &&
        (!fFlavor || p.flavor === fFlavor) &&
        (!fSize   || sizeBucket(p.weight_g) === fSize) &&
        p.protein_g >= fMinProt
      )
      .sort(sorters[sort])
  }, [products, fBrand, fFlavor, fSize, fMinProt, sort])

  const bestId = useMemo(() =>
    view.length ? [...view].sort(sorters.p30)[0].id : null,
  [view])

  return (
    <>
      <div className="filters">
        <SlidersHorizontal size={18} color="var(--mut)" />
        <div className="fgroup">
          <label>Marca</label>
          <select value={fBrand} onChange={(e) => setFBrand(e.target.value)}>
            <option value="">Todas</option>
            {brands.map((b) => <option key={b} value={b}>{b}</option>)}
          </select>
        </div>
        <div className="fgroup">
          <label>Sabor</label>
          <select value={fFlavor} onChange={(e) => setFFlavor(e.target.value)}>
            <option value="">Todos</option>
            {flavors.map((f) => <option key={f} value={f}>{f}</option>)}
          </select>
        </div>
        <div className="fgroup">
          <label>Tamanho</label>
          <select value={fSize} onChange={(e) => setFSize(e.target.value)}>
            <option value="">Todos</option>
            <option value="900">~900g</option>
            <option value="1000">~1kg</option>
            <option value="2000">~2kg</option>
          </select>
        </div>
        <div className="fgroup">
          <label>Proteína mín / dose: {fMinProt}g</label>
          <input type="range" min="0" max="30" value={fMinProt} onChange={(e) => setFMinProt(+e.target.value)} />
        </div>
        <div className="fgroup" style={{ marginLeft: 'auto' }}>
          <label>Ordenar por</label>
          <select value={sort} onChange={(e) => setSort(e.target.value)}>
            {SORT_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
        </div>
      </div>

      <div className="grid">
        {view.map((p) => (
          <ProductCard key={p.id} product={p} isBest={p.id === bestId} />
        ))}
        {!view.length && <div className="empty">Nenhum produto com esses filtros.</div>}
      </div>
    </>
  )
}
