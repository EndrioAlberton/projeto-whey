import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'
import SiteHeader from './SiteHeader'

export default function Institucional({ titulo, children }) {
  return (
    <main className="wrap">
      <SiteHeader />
      <Link href="/" className="voltar"><ArrowLeft size={14} aria-hidden="true" /> Voltar à página principal</Link>
      <article className="prose">
        <h1>{titulo}</h1>
        {children}
      </article>
    </main>
  )
}
