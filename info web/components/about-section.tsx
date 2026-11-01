import { CalendarClock, AudioWaveform, WifiOff } from "lucide-react"

const features = [
  {
    icon: CalendarClock,
    title: "Rule-based servicing",
    description:
      "Oil, filter and belt intervals taken from the Massey Ferguson MF 240 and MF 375 operator manuals, triggered by engine hours or calendar time, whichever comes first.",
  },
  {
    icon: AudioWaveform,
    title: "Sound-based anomaly detection",
    description:
      "A short engine recording is converted to MFCC features and scored by a classifier, then compared with that tractor's own healthy baseline.",
  },
  {
    icon: WifiOff,
    title: "Built for weak connectivity",
    description:
      "The Flutter app is designed offline-first: record and log usage in the field, sync when a connection is available.",
  },
]

export function AboutSection() {
  return (
    <section id="problem" className="py-24 px-4">
      <div className="container mx-auto max-w-6xl">
        <div className="grid lg:grid-cols-[0.8fr_1.2fr] gap-12">
          <div>
            <p className="eyebrow mb-4">The problem</p>
            <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-balance">
              Tractors fail in the field, far from a workshop.
            </h2>
            <p className="mt-5 text-muted-foreground leading-relaxed">
              Many smallholder farmers in Rwanda rely on older, shared tractors. Faults are usually noticed only after
              a breakdown, and a skilled mechanic can be hours away. An engine often sounds different before it fails,
              which makes sound a cheap early signal.
            </p>
          </div>

          <ul className="space-y-4">
            {features.map((f) => (
              <li key={f.title} className="flex gap-5 rounded-2xl border border-border bg-card p-6">
                <div className="shrink-0 w-12 h-12 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                  <f.icon className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">{f.title}</h3>
                  <p className="mt-1.5 text-muted-foreground leading-relaxed">{f.description}</p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  )
}
