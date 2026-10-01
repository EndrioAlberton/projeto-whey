import { Award, ShoppingCart } from 'lucide-react'

const brl = (n) => n == null ? '—' : Number(n).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })

export default function ProductCard({ produto: p, isMelhor }) {
  // Sem link de afiliado ainda (produto recém-importado)? usa o link real
  // do produto como fallback, senão o botão fica quebrado.
  const link = p.url_afiliado || p.url_produto

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
          <small>proteína / dose de {p.dose_g}g</small>
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
        {link ? (
          <a className="buy" href={link} target="_blank" rel="nofollow noopener noreferrer sponsored">
            <ShoppingCart size={16} />
            Comprar no {p.plataforma === 'ML' ? 'Mercado Livre' : 'Amazon'}
          </a>
        ) : (
          <span className="buy" style={{ opacity: .5, cursor: 'not-allowed' }}>
            <ShoppingCart size={16} />
            Link indisponível
          </span>
        )}
      </div>
    </div>
  )
}
