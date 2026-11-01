import { AlertTriangle } from "lucide-react"
import { REPO_URL } from "./site-config"

// Results of evaluation/run_evaluation.py (5-fold CV, 289 clips, 40 pseudo-recording groups).
const rows = [
  { model: "KNN (k = 5)", random: 90.9, grouped: 68.0 },
  { model: "SVM (RBF)", random: 93.5, grouped: 80.7 },
  { model: "Simple CNN", random: 92.4, grouped: 83.2 },
  { model: "ResNet-like CNN", random: 94.5, grouped: 93.9 },
]

export function EvidenceSection() {
  return (
    <section id="evidence" className="py-24 px-4 bg-muted/60">
      <div className="container mx-auto max-w-6xl">
        <p className="eyebrow mb-4">Evidence</p>
        <h2 className="text-3xl md:text-4xl font-bold tracking-tight max-w-3xl text-balance">
          We tested it honestly. Only one model held up.
        </h2>
        <p className="mt-5 max-w-3xl text-muted-foreground leading-relaxed">
          The tractor clips are short segments cut from longer recordings, so neighbouring segments are almost
          identical. A random train/test split lets near-duplicates land on both sides and inflates accuracy. We
          re-ran the comparison keeping each recording group on one side only. The classical models lost 13 to 23 points;
          the ResNet-like CNN, the architecture used in the app, kept 93.9%.
        </p>

        <div className="mt-10 grid lg:grid-cols-[1.2fr_0.8fr] gap-6">
          <figure className="rounded-2xl border border-border bg-card p-6 md:p-8">
            <figcaption className="font-semibold">Accuracy by evaluation protocol</figcaption>
            <div className="mt-6 space-y-7">
              {rows.map((r) => (
                <div key={r.model}>
                  <p className="text-sm font-medium mb-2">{r.model}</p>
                  {[
                    { label: "Random split (leaky)", v: r.random, cls: "bg-muted-foreground/35" },
                    { label: "Grouped split (honest)", v: r.grouped, cls: "bg-primary" },
                  ].map((b) => (
                    <div key={b.label} className="flex items-center gap-3 mb-1.5">
                      <span className="w-40 shrink-0 text-xs text-muted-foreground">{b.label}</span>
                      <div className="relative flex-1 h-6 rounded-md bg-muted overflow-hidden">
                        <div className={`h-full rounded-md ${b.cls}`} style={{ width: `${b.v}%` }} />
                      </div>
                      <span className="w-12 text-right text-sm font-semibold tabular-nums">{b.v}%</span>
                    </div>
                  ))}
                </div>
              ))}
            </div>
            <p className="mt-6 text-xs text-muted-foreground">
              5-fold cross-validation on 289 clips in 40 inferred recording groups. ResNet-like CNN grouped F1 0.92
              (95% CI 0.90 to 0.96). Fold-to-fold spread is large for the other models (SVM ±11.7 points), so small
              gaps between them are not significant.
            </p>
          </figure>

          <div className="space-y-6">
            <div className="rounded-2xl border border-accent/60 bg-accent/15 p-6">
              <div className="flex items-center gap-2 font-semibold">
                <AlertTriangle className="w-5 h-5 text-accent-foreground" />
                Phone recordings: 0 of 6 caught
              </div>
              <p className="mt-2 text-sm leading-relaxed">
                Trained on every other clip, the SVM missed all six held-out faulty-engine recordings made with a
                phone (the CNNs were not tested on them). Six clips is a small sample, but it is the closest thing
                to a field test, and it shows performance on a new microphone is unproven.
              </p>
            </div>
            <div className="rounded-2xl border border-border bg-card p-6 text-sm leading-relaxed text-muted-foreground">
              <p className="font-semibold text-foreground">Known limitations</p>
              <ul className="mt-2 list-disc pl-5 space-y-1.5">
                <li>Training clips come from public sound libraries, not labelled Rwandan MF 240/375 faults.</li>
                <li>&ldquo;Abnormal&rdquo; does not identify a specific failure.</li>
                <li>Recording groups are inferred by clustering, not recorded.</li>
                <li>The benefit of pump pre-training (MIMII) has not been isolated yet.</li>
              </ul>
              <a href={REPO_URL} target="_blank" rel="noopener noreferrer" className="mt-4 inline-block font-medium text-primary underline underline-offset-4">
                Reproduce it from the repository
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
