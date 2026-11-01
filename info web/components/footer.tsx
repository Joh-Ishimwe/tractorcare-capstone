import Link from "next/link"
import Image from "next/image"
import { REPO_URL } from "./site-config"

export function Footer() {
  return (
    <footer className="border-t border-border py-10 px-4">
      <div className="container mx-auto max-w-6xl flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2 font-bold">
          <Image src="/Logo.png" alt="TractorCare" width={81} height={32} className="h-8 w-auto rounded-md" />
        </div>
        <p className="text-sm text-muted-foreground text-center">
          Capstone project by Josiane Ishimwe. A research prototype, not a certified diagnostic tool.
        </p>
        <Link href={REPO_URL} className="text-sm text-muted-foreground hover:text-foreground transition-colors">
          GitHub
        </Link>
      </div>
    </footer>
  )
}
