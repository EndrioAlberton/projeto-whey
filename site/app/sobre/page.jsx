import Link from 'next/link'
import { Calculator, Database, Scale, Heart } from 'lucide-react'
import Institucional from '../../components/Institucional'

export const metadata = {
  title: 'Sobre o WheyMais',
  description: 'Como o WheyMais compara whey protein pelo custo por 30g de proteína e como o site é mantido.',
  alternates: { canonical: '/sobre' },
}

const PASSOS = [
  { icon: Database, titulo: 'Dados', texto: 'Preço, nome e imagem vêm da API do Mercado Livre, atualizados todos os dias. A proteína por dose é conferida à mão.' },
  { icon: Calculator, titulo: 'Conta', texto: 'Dividimos o preço total pelo total de gramas de proteína do pote e normalizamos para 30g, uma dose padrão.' },
  { icon: Scale, titulo: 'Ranking', texto: 'Os produtos são ordenados só pelo custo da proteína. Quanto menor o valor, mais barata é cada dose.' },
]

export default function Sobre() {
  return (
    <Institucional titulo="Sobre o WheyMais">
      <p className="lead">Um pote barato nem sempre tem a proteína mais barata. O WheyMais faz essa conta por você e ordena os wheys pelo <strong>custo por 30g de proteína</strong>, e não pelo preço da embalagem.</p>

      <h2>Como funciona</h2>
      <div className="steps">
        {PASSOS.map(({ icon: Icon, titulo, texto }, i) => (
          <div className="step" key={titulo}>
            <Icon size={20} aria-hidden="true" />
            <h3>{i + 1}. {titulo}</h3>
            <p>{texto}</p>
          </div>
        ))}
      </div>

      <h2>Por que isso importa</h2>
      <p>Exemplo ilustrativo, com doses de 30g e 24g de proteína em cada uma:</p>
      <div className="exemplo">
        <div>
          <span>Pote de 900g</span>
          <strong>R$ 150</strong>
          <em>R$ 6,25 por 30g de proteína</em>
        </div>
        <div className="venceu">
          <span>Pote de 1,8kg</span>
          <strong>R$ 200</strong>
          <em>R$ 4,17 por 30g de proteína</em>
        </div>
      </div>
      <p>O pote mais caro é o que entrega a proteína mais barata, e o preço da etiqueta sozinho esconderia isso.</p>

      <h2>Limitações</h2>
      <p>O preço mostrado é o menor listado pelos vendedores no catálogo. Cupons, promoções relâmpago e cashback não entram na conta, então o valor final pode ser menor.</p>

      <h2>Como o site se mantém</h2>
      <p>Os links "Comprar" são de afiliado: recebemos uma comissão quando você compra por eles, sem custo adicional para você. Isso não muda a ordem dos produtos, que segue só o custo por proteína.</p>

      <h2>Quem faz</h2>
      <div className="autor">
        <Heart size={18} aria-hidden="true" />
        <p>O WheyMais é um projeto pessoal, desenvolvido e mantido por <strong>Endrio Alberton</strong>. Achou algo errado ou tem uma sugestão? Fale pela página de <Link href="/contato">contato</Link>.</p>
      </div>
    </Institucional>
  )
}
