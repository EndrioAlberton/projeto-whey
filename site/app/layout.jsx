import './globals.css'
import Footer from '../components/Footer'

export const metadata = {
  title: 'WheyMais — Compare whey protein pelo custo por proteína',
  description: 'Compare os melhores wheys do Brasil pelo custo por 30g de proteína. Filtros por marca, sabor e proteína mínima. Preços atualizados.',
  openGraph: {
    title: 'WheyMais — Compare whey protein pelo custo por proteína',
    description: 'Compare os melhores wheys do Brasil pelo custo por 30g de proteína.',
    locale: 'pt_BR',
    type: 'website',
  },
}

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body>
        {children}
        <Footer />
      </body>
    </html>
  )
}
