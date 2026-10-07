import Link from 'next/link'

// [rótulo, slug de /whey-barato/[slug]]
const BRANDS  = [['Growth', 'growth-supplements'], ['Max Titanium', 'max-titanium'], ['Dux', 'dux-nutrition'], ['Integralmédica', 'integralmedica'], ['Probiótica', 'probiotica'], ['Black Skull', 'black-skull'], ['New Millen', 'new-millen'], ['Atlhetica', 'atlhetica']]
const FLAVORS = [['Chocolate', 'chocolate'], ['Baunilha', 'baunilha'], ['Morango', 'morango'], ['Cookies', 'cookies-and-cream']]
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
              {BRANDS.map(([nome, slug]) => (
                <li key={slug}><Link href={`/whey-barato/${slug}`}>{nome}</Link></li>
              ))}
            </ul>
          </div>

          <div className="footer-col">
            <h3>Por sabor</h3>
            <ul>
              {FLAVORS.map(([nome, slug]) => (
                <li key={slug}><Link href={`/whey-barato/${slug}`}>{nome}</Link></li>
              ))}
            </ul>
            <h3 style={{ marginTop: 20 }}>Por tamanho</h3>
            <ul>
              {SIZES.map((s) => (
                <li key={s.value}><Link href={`/?tamanho=${s.value}`}>{s.label}</Link></li>
              ))}
            </ul>
          </div>

          <div className="footer-col footer-col--wide">
            <h3>Como calculamos o custo por proteína</h3>
            <p>
              Dividimos o preço total do produto pelo total de gramas de proteína que ele entrega.
              O resultado é normalizado para 30g (uma dose padrão) permitindo comparar potes de
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
            <Link href="/?sort=p30">Melhor custo-benefício</Link>
          </div>
          <span className="footer-copy">
            © {year} WheyMais — Desenvolvido por{' '}
            <a href="mailto:endrio.alberton@gmail.com">endrio.alberton@gmail.com</a>
          </span>
        </div>

      </div>
    </footer>
  )
}
