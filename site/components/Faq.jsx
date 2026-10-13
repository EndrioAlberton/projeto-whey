const PERGUNTAS = [
  ['Como escolher um whey pelo orçamento?',
   'Compare pelo custo por 30g de proteína, não pelo preço do pote. Potes de tamanhos, doses e teores de proteína diferentes só ficam comparáveis nessa conta. Quanto menor o valor, mais barata é a proteína.'],
  ['Qual a diferença entre concentrado, isolado e hidrolisado?',
   'O concentrado é o mais comum e o mais barato, e costuma ter um pouco mais de lactose e gordura. O isolado passa por mais filtragem, tem mais proteína por dose e menos lactose, e custa mais. O hidrolisado é pré-digerido e o mais caro, e para a maioria das pessoas a vantagem prática é pequena.'],
  ['Quanta proteína eu preciso por dia?',
   'Para quem treina, as faixas mais citadas ficam entre 1,6 e 2,2 g por kg de peso corporal ao dia, somando toda a alimentação. O whey é um complemento, não um substituto da comida. Para uma recomendação para o seu caso, procure um nutricionista.'],
  ['O preço no site é o mesmo do Mercado Livre?',
   'É o menor preço listado pelos vendedores no catálogo, e atualizamos todos os dias. Cupons, promoções relâmpago e cashback não entram na conta, então o preço que você paga pode ser menor.'],
  ['O site ganha comissão?',
   'Sim. Os links "Comprar" são de afiliado, e recebemos uma comissão se você comprar por eles, sem custo adicional para você. Isso não muda a ordem dos produtos, que segue só o custo por proteína.'],
]

export default function Faq() {
  return (
    <section className="faq">
      <h2>Perguntas frequentes</h2>
      {PERGUNTAS.map(([p, r]) => (
        <details key={p}>
          <summary>{p}</summary>
          <p>{r}</p>
        </details>
      ))}
    </section>
  )
}
