import { Award, ShoppingCart } from 'lucide-react'

const brl = (n) => n.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })

export default function ProductCard({ produto: p, isMelhor }) {
  return (
    <div className={'card' + (isMelhor ? ' best' : '')}>
      {isMelhor && (
        <div className="best-tag">
          <Award size={11} /> Melhor custo-benefício
        </div>
      )}
      <div className="thumb">
        <span className={'plat-pill abs ' + (p.plataforma === 'ML' ? 'pill-ml' : 'pill-amazon')}>
          {p.plataforma === 'ML' ? 'Mercado Livre' : 'Amazon'}
        </span>
        <div style={{ textAlign: 'center' }}>
          <div className="mono-prot">{p.proteina_g}g</div>
          <small>proteína / dose</small>
        </div>
      </div>
      <div className="cbody">
        <div className="brand">{p.marca}</div>
        <div className="pname">{p.nome}</div>
        <div className="tags">
          <span className="tag">{p.sabor}</span>
          <span className="tag">{p.peso_g}g</span>
          <span className="tag">{p.doses} doses</span>
        </div>
        <div className="metrics">
          <div className="metric">
            <div className="k">Custo / dose</div>
            <div className="v">{brl(p.custo_por_dose)}</div>
          </div>
          <div className="metric hl">
            <div className="k">Custo / 30g proteína</div>
            <div className="v">{brl(p.custo_por_30g_proteina)}</div>
          </div>
        </div>
        <div className="price-row">
          <span className="price">{brl(p.preco)}</span>
        </div>
        <a className="buy" href={p.url_afiliado} target="_blank" rel="nofollow noopener noreferrer sponsored">
          <ShoppingCart size={16} />
          Comprar no {p.plataforma === 'ML' ? 'Mercado Livre' : 'Amazon'}
        </a>
      </div>
    </div>
  )
}
