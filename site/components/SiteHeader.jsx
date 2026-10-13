import Link from 'next/link'
import { Zap } from 'lucide-react'
import ThemeToggle from './ThemeToggle'

export default function SiteHeader() {
  return (
    <header>
      <Link href="/" className="logo" aria-label="WheyMais, página inicial" style={{ textDecoration: 'none', color: 'inherit' }}>
        <Zap aria-hidden="true" size={26} color="var(--lime)" fill="var(--lime)" />
        <b>Whey<span className="x">Mais</span></b>
        <span className="badge-lab">custo por proteína</span>
      </Link>
      <ThemeToggle />
    </header>
  )
}
