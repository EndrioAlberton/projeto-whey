import { Mail, Tag, Link2, Lightbulb } from 'lucide-react'
import Institucional from '../../components/Institucional'

export const metadata = {
  title: 'Contato | WheyMais',
  description: 'Fale com o WheyMais: dúvidas, correções de preço ou dose e sugestões.',
  alternates: { canonical: '/contato' },
}

const EMAIL = 'endrio.alberton@gmail.com'

const MOTIVOS = [
  { icon: Tag, titulo: 'Preço ou dose errados', texto: 'Mande o link da página e o valor que você viu no Mercado Livre.' },
  { icon: Link2, titulo: 'Link quebrado', texto: 'Se o botão "Comprar" abriu uma página vazia ou outro produto, avise.' },
  { icon: Lightbulb, titulo: 'Sugestão', texto: 'Uma marca que falta, um filtro útil ou uma ideia para o site.' },
]

export default function Contato() {
  return (
    <Institucional titulo="Contato">
      <p className="lead">O WheyMais é mantido por uma pessoa só, e o seu aviso ajuda a manter os dados certos. Escolha o assunto e escreva.</p>

      <div className="steps">
        {MOTIVOS.map(({ icon: Icon, titulo, texto }) => (
          <div className="step" key={titulo}>
            <Icon size={20} aria-hidden="true" />
            <h3>{titulo}</h3>
            <p>{texto}</p>
          </div>
        ))}
      </div>

      <div className="autor" style={{ marginTop: 24 }}>
        <Mail size={18} aria-hidden="true" />
        <p>Prefere escrever direto? <a href={`mailto:${EMAIL}`}>{EMAIL}</a></p>
      </div>

      <p style={{ marginTop: 24 }}>
        <a className="cta" href={`mailto:${EMAIL}?subject=${encodeURIComponent('Contato WheyMais')}`}>
          <Mail size={16} aria-hidden="true" /> Enviar e-mail
        </a>
      </p>
    </Institucional>
  )
}
