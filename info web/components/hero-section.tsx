import { Button } from "@/components/ui/button"
import { ArrowRight, Download } from "lucide-react"
import Link from "next/link"
import { APK_URL } from "./site-config"

const facts = [
  { value: "295", label: "labelled tractor sound clips" },
  { value: "6", label: "model families compared" },
  { value: "2-stage", label: "global model + personal baseline" },
  { value: "MF 240 / 375", label: "manual-based service rules" },
]

export function HeroSection() {
  return (
    <section className="relative pt-28 pb-16 px-4 overflow-hidden">
      <div className="absolute inset-x-0 top-0 h-[28rem] bg-gradient-to-b from-primary/10 to-transparent -z-10" />
      <div className="container mx-auto max-w-6xl">
        <div className="grid lg:grid-cols-[1.1fr_0.9fr] gap-12 items-center">
          <div>
            <p className="eyebrow mb-5">Capstone research project · Rwanda</p>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight leading-[1.05] text-balance">
              Listen to your tractor <span className="text-primary">before it breaks down.</span>
            </h1>
            <p className="mt-6 text-lg text-muted-foreground leading-relaxed max-w-xl text-pretty">
              TractorCare pairs a manufacturer-manual maintenance schedule with machine-learning analysis of engine
              sound, so a smallholder farmer can check a tractor with nothing more than a phone.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row gap-3">
              <Button asChild size="lg" className="rounded-full h-12 px-7 group">
                <Link href="#test-model">
                  Try the live demo
                  <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="rounded-full h-12 px-7 bg-transparent">
                <a href={APK_URL} target="_blank" rel="noopener noreferrer">
                  <Download className="mr-2 h-4 w-4" />
                  Android app (APK)
                </a>
              </Button>
            </div>
            <p className="mt-5 text-sm text-muted-foreground">
              A research prototype. Read the{" "}
              <Link href="#evidence" className="underline underline-offset-4 hover:text-foreground">
                honest evaluation
              </Link>
              .
            </p>
          </div>

          <div className="relative">
            <div className="absolute -inset-3 rounded-[2rem] bg-accent/30 rotate-2 -z-10" />
            <img
              src="/modern-tractor-in-field-rwanda-agriculture.png"
              alt="A tractor working in a field in Rwanda"
              className="w-full aspect-[4/3] object-cover rounded-[1.75rem] border border-border shadow-xl"
            />
          </div>
        </div>

        <dl className="mt-14 grid grid-cols-2 lg:grid-cols-4 gap-px bg-border rounded-2xl overflow-hidden border border-border">
          {facts.map((f) => (
            <div key={f.label} className="bg-card p-5">
              <dd className="text-2xl font-bold text-primary">{f.value}</dd>
              <dt className="text-sm text-muted-foreground mt-1">{f.label}</dt>
            </div>
          ))}
        </dl>
      </div>
    </section>
  )
}
