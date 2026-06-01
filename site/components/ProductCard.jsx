import { Award, ShoppingCart } from 'lucide-react'

const brl = (n) => n.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })

export default function ProductCard({ product, isBest }) {
  const p = product
  return (
    <div className={'card' + (isBest ? ' best' : '')}>
      {isBest && (
        <div className="best-tag">
          <Award size={11} /> Melhor custo-benefício
        </div>
      )}
      <div className="thumb">
        <span className={'plat-pill abs ' + (p.platform === 'ML' ? 'pill-ml' : 'pill-amazon')}>
          {p.platform === 'ML' ? 'Mercado Livre' : 'Amazon'}
        </span>
        <div style={{ textAlign: 'center' }}>
          <div className="mono-prot">{p.protein_g}g</div>
          <small>proteína / dose</small>
        </div>
      </div>
      <div className="cbody">
        <div className="brand">{p.brand}</div>
        <div className="pname">{p.name}</div>
        <div className="tags">
          <span className="tag">{p.flavor}</span>
          <span className="tag">{p.weight_g}g</span>
          <span className="tag">{p.servings} doses</span>
        </div>
        <div className="metrics">
          <div className="metric">
            <div className="k">Custo / dose</div>
            <div className="v">{brl(p.cost_per_dose)}</div>
          </div>
          <div className="metric hl">
            <div className="k">Custo / 30g proteína</div>
            <div className="v">{brl(p.cost_per_30g_protein)}</div>
          </div>
        </div>
        <div className="price-row">
          <span className="price">{brl(p.price)}</span>
        </div>
        <a className="buy" href={p.affiliate_url} target="_blank" rel="nofollow noopener noreferrer sponsored">
          <ShoppingCart size={16} />
          Comprar no {p.platform === 'ML' ? 'Mercado Livre' : 'Amazon'}
        </a>
      </div>
    </div>
  )
}
