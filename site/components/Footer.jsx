import Link from 'next/link'
import Faq from './Faq'

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
            <Faq />
          </div>

          <div className="footer-col footer-col--wide">
            <h2>Como calculamos o custo por proteína</h2>
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
            <Link href="/sobre">Sobre</Link>
            <Link href="/contato">Contato</Link>
            <Link href="/privacidade">Privacidade</Link>
          </div>
          <span className="footer-copy">
            © {year} WheyMais
          </span>
        </div>

      </div>
    </footer>
  )
}
