import Institucional from '../../components/Institucional'

export const metadata = {
  title: 'Política de privacidade | WheyMais',
  description: 'Quais dados o WheyMais coleta, para quê e como falar com a gente sobre eles.',
  alternates: { canonical: '/privacidade' },
}

export default function Privacidade() {
  return (
    <Institucional titulo="Política de privacidade">
      <p>Atualizada em 7 de outubro de 2026.</p>
      <h2>O que coletamos</h2>
      <p>O WheyMais não tem cadastro, login nem formulários, e não pede dados pessoais. O servidor registra os acessos em logs técnicos (endereço IP, página, data e horário), usados para segurança e para diagnosticar falhas.</p>
      <h2>Armazenamento no navegador</h2>
      <p>O site guarda no seu navegador apenas a preferência de tema (claro ou escuro). Esse dado fica no seu aparelho e não é enviado para nós.</p>
      <h2>Links de afiliado</h2>
      <p>Ao clicar em "Comprar", você sai do WheyMais e vai para o Mercado Livre, que tem a sua própria política de privacidade e pode usar cookies para identificar que a compra veio do nosso link.</p>
      <h2>Seus direitos</h2>
      <p>Pela LGPD, você pode pedir informações, correção ou exclusão dos dados que tivermos sobre você. Escreva para <a href="mailto:endrio.alberton@gmail.com">endrio.alberton@gmail.com</a>.</p>
    </Institucional>
  )
}
