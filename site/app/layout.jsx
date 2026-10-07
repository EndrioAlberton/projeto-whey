import './globals.css'
import Footer from '../components/Footer'

import { SITE_URL } from '../lib/slug'

export const metadata = {
  metadataBase: new URL(SITE_URL),
  title: 'WheyMais — Compare whey protein pelo custo por proteína',
  description: 'Compare os melhores wheys do Brasil pelo custo por 30g de proteína. Filtros por marca, sabor e proteína mínima. Preços atualizados.',
  verification: { google: '9aDvQDm412ZkAO0p34GothTAF9wtklABn0Q3hAG8RiE' },
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
      <head>
        <script dangerouslySetInnerHTML={{ __html: `try{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t)}catch(e){}` }} />
      </head>
      <body>
        {children}
        <Footer />
      </body>
    </html>
  )
}
