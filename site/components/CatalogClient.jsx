'use client'

import { useState, useMemo, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import { SlidersHorizontal } from 'lucide-react'
import ProductCard from './ProductCard'

const OPCOES_ORDENACAO = [
  { value: 'p30',    label: 'Melhor custo por proteína' },
  { value: 'dose',   label: 'Menor custo por dose' },
  { value: 'preco',  label: 'Menor preço' },
  { value: 'prot',   label: 'Mais proteína por dose' },
]

const ordenadores = {
  p30:   (a, b) => a.custo_por_30g_proteina - b.custo_por_30g_proteina,
  dose:  (a, b) => a.custo_por_dose - b.custo_por_dose,
  preco: (a, b) => a.preco - b.preco,
  prot:  (a, b) => b.proteina_g - a.proteina_g,
}

function faixaPeso(peso_g) {
  if (peso_g >= 1800) return '2000'
  if (peso_g >= 950)  return '1000'
  return '900'
}

export default function CatalogClient({ produtos, opcoes = {} }) {
  const params = useSearchParams()

  const [fMarca,      setFMarca]      = useState('')
  const [fSabor,      setFSabor]      = useState('')
  const [fTamanho,    setFTamanho]    = useState('')
  const [fProtMin,    setFProtMin]    = useState(0)
  const [ordenar,     setOrdenar]     = useState('p30')

  useEffect(() => {
    if (params.get('marca'))   setFMarca(params.get('marca'))
    if (params.get('sabor'))   setFSabor(params.get('sabor'))
    if (params.get('tamanho')) setFTamanho(params.get('tamanho'))
    if (params.get('ordenar')) setOrdenar(params.get('ordenar'))
  }, [params])

  const marcas  = opcoes.marcas  || [...new Set(produtos.map((p) => p.marca))]
  const sabores = opcoes.sabores || [...new Set(produtos.map((p) => p.sabor))]
  const tamanhos = opcoes.tamanhos || []

  const lista = useMemo(() => {
    return [...produtos]
      .filter((p) =>
        (!fMarca   || p.marca  === fMarca)  &&
        (!fSabor   || p.sabor  === fSabor)  &&
        (!fTamanho || faixaPeso(p.peso_g) === fTamanho) &&
        p.proteina_g >= fProtMin
      )
      .sort(ordenadores[ordenar])
  }, [produtos, fMarca, fSabor, fTamanho, fProtMin, ordenar])

  const melhorId = useMemo(() =>
    lista.length ? [...lista].sort(ordenadores.p30)[0].id : null,
  [lista])

  return (
    <>
      <div className="filters">
        <SlidersHorizontal size={18} color="var(--mut)" />
        <div className="fgroup">
          <label>Marca</label>
          <select value={fMarca} onChange={(e) => setFMarca(e.target.value)}>
            <option value="">Todas</option>
            {marcas.map((m) => <option key={m} value={m}>{m}</option>)}
          </select>
        </div>
        <div className="fgroup">
          <label>Sabor</label>
          <select value={fSabor} onChange={(e) => setFSabor(e.target.value)}>
            <option value="">Todos</option>
            {sabores.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>
        <div className="fgroup">
          <label>Tamanho</label>
          <select value={fTamanho} onChange={(e) => setFTamanho(e.target.value)}>
            <option value="">Todos</option>
            {tamanhos.map((t) => (
              <option key={t.peso_g} value={t.peso_g}>{t.rotulo}</option>
            ))}
          </select>
        </div>
        <div className="fgroup">
          <label>Proteína mín / dose: {fProtMin}g</label>
          <input type="range" min="0" max="30" value={fProtMin} onChange={(e) => setFProtMin(+e.target.value)} />
        </div>
        <div className="fgroup" style={{ marginLeft: 'auto' }}>
          <label>Ordenar por</label>
          <select value={ordenar} onChange={(e) => setOrdenar(e.target.value)}>
            {OPCOES_ORDENACAO.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
        </div>
      </div>

      <div className="grid">
        {lista.map((p) => (
          <ProductCard key={p.id} produto={p} isMelhor={p.id === melhorId} />
        ))}
        {!lista.length && <div className="empty">Nenhum produto com esses filtros.</div>}
      </div>
    </>
  )
}
