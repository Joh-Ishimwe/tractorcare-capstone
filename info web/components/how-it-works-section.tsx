import { Mic, AudioLines, GitCompare, Bell } from "lucide-react"

const steps = [
  { icon: Mic, title: "Record", text: "Capture about ten seconds of the running engine with the phone." },
  { icon: AudioLines, title: "Extract features", text: "High-pass filter at 100 Hz, then 40 MFCCs over 100 frames at 16 kHz." },
  {
    icon: GitCompare,
    title: "Score twice",
    text: "A global classifier gives an anomaly probability; a baseline check measures drift from this tractor's healthy sound.",
  },
  { icon: Bell, title: "Act", text: "Anomalies map to suggested maintenance tasks, alongside the manual-based schedule." },
]

export function HowItWorksSection() {
  return (
    <section id="how-it-works" className="py-24 px-4 bg-muted/60">
      <div className="container mx-auto max-w-6xl">
        <p className="eyebrow mb-4">How it works</p>
        <h2 className="text-3xl md:text-4xl font-bold tracking-tight max-w-2xl text-balance">
          From a phone recording to a maintenance decision.
        </h2>

        <ol className="mt-12 grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {steps.map((s, i) => (
            <li key={s.title} className="relative rounded-2xl bg-card border border-border p-6">
              <span className="absolute top-5 right-5 text-4xl font-bold text-primary/15 leading-none">{i + 1}</span>
              <div className="w-11 h-11 rounded-xl bg-primary text-primary-foreground flex items-center justify-center">
                <s.icon className="w-5 h-5" />
              </div>
              <h3 className="mt-5 font-semibold text-lg">{s.title}</h3>
              <p className="mt-2 text-sm text-muted-foreground leading-relaxed">{s.text}</p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  )
}
