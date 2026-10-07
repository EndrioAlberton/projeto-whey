import './globals.css'
import Footer from '../components/Footer'

import { Anton, DM_Sans, JetBrains_Mono } from 'next/font/google'
import { SITE_URL } from '../lib/slug'

const anton = Anton({ subsets: ['latin'], weight: '400', variable: '--f-anton', display: 'swap' })
const dm    = DM_Sans({ subsets: ['latin'], weight: ['400', '500', '700'], variable: '--f-dm', display: 'swap' })
const mono  = JetBrains_Mono({ subsets: ['latin'], weight: ['500', '700'], variable: '--f-mono', display: 'swap' })

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
    <html lang="pt-BR" className={`${anton.variable} ${dm.variable} ${mono.variable}`}>
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
