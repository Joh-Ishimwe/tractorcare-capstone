import { Github, MessageSquare } from "lucide-react"
import { REPO_URL } from "./site-config"

export function ContactSection() {
  return (
    <section id="contact" className="py-24 px-4">
      <div className="container mx-auto max-w-6xl">
        <div className="rounded-[2rem] border border-border bg-card p-8 md:p-12 grid md:grid-cols-[1.2fr_0.8fr] gap-8 items-center">
          <div>
            <p className="eyebrow mb-4">Get involved</p>
            <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-balance">
              Own a tractor, or work on them? Help us test it.
            </h2>
            <p className="mt-4 text-muted-foreground leading-relaxed max-w-xl">
              The biggest gap is real recordings from Massey Ferguson tractors with a mechanic&apos;s verdict. If you can
              contribute recordings or feedback, or want to build on the code, open an issue on GitHub.
            </p>
          </div>
          <div className="flex flex-col gap-3">
            <a
              href={`${REPO_URL}/issues/new`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-2 rounded-full bg-primary text-primary-foreground h-12 px-6 font-medium hover:bg-primary/90 transition-colors"
            >
              <MessageSquare className="w-4 h-4" /> Share feedback
            </a>
            <a
              href={REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-2 rounded-full border border-border h-12 px-6 font-medium hover:bg-muted transition-colors"
            >
              <Github className="w-4 h-4" /> View the code
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
