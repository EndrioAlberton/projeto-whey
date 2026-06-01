import Link from 'next/link'

const BRANDS  = ['Growth', 'Max Titanium', 'Dux', 'Integralmédica', 'Probiótica', 'Black Skull', 'New Millen', 'Atlhetica']
const FLAVORS = ['Chocolate', 'Baunilha', 'Morango', 'Cookies']
const SIZES   = [{ label: '900g', value: '900' }, { label: '1kg', value: '1000' }, { label: '2kg', value: '2000' }]

export default function Footer() {
  const year = new Date().getFullYear()

  return (
    <footer className="site-footer">
      <div className="wrap">

        <div className="affiliate-notice">
          <strong>Aviso de afiliado:</strong> Este site contém links de afiliado. Podemos receber uma comissão quando você compra por eles, sem custo adicional para você. Isso nos ajuda a manter o site gratuito e os preços atualizados.
        </div>

        <div className="footer-grid">

          <div className="footer-col">
            <h3>Por marca</h3>
            <ul>
              {BRANDS.map((b) => (
                <li key={b}><Link href={`/?brand=${encodeURIComponent(b)}`}>{b}</Link></li>
              ))}
            </ul>
          </div>

          <div className="footer-col">
            <h3>Por sabor</h3>
            <ul>
              {FLAVORS.map((f) => (
                <li key={f}><Link href={`/?flavor=${encodeURIComponent(f)}`}>{f}</Link></li>
              ))}
            </ul>
            <h3 style={{ marginTop: 20 }}>Por tamanho</h3>
            <ul>
              {SIZES.map((s) => (
                <li key={s.value}><Link href={`/?size=${s.value}`}>{s.label}</Link></li>
              ))}
            </ul>
          </div>

          <div className="footer-col footer-col--wide">
            <h3>Como calculamos o custo por proteína</h3>
            <p>
              Dividimos o preço total do produto pelo total de gramas de proteína que ele entrega.
              O resultado é normalizado para 30g — uma dose padrão — permitindo comparar potes de
              tamanhos e doses diferentes em igualdade de condições. Quanto menor o valor, mais
              barato sai cada dose de proteína.
            </p>
            <p style={{ marginTop: 10 }}>
              <strong>Preços atualizados diariamente</strong> via API oficial do Mercado Livre e Amazon.
              A proteína por dose é cadastrada manualmente, pois as APIs não fornecem esse dado.
            </p>
          </div>

        </div>

        <div className="footer-bottom">
          <div className="footer-legal">
            <Link href="/politica-de-privacidade">Política de Privacidade</Link>
            <Link href="/termos-de-uso">Termos de Uso</Link>
            <Link href="/?sort=p30">Melhor custo-benefício</Link>
          </div>
          <span className="footer-copy">© {year} WheyMais — Todos os direitos reservados</span>
        </div>

      </div>
    </footer>
  )
}
