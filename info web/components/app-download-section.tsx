import { Button } from "@/components/ui/button"
import { Download, WifiOff, Mic, History, CalendarCheck } from "lucide-react"
import { APK_URL } from "./site-config"

const features = [
  { icon: Mic, title: "Record and compare", text: "Capture a healthy baseline, then test later recordings against it." },
  { icon: WifiOff, title: "Offline-first", text: "Log usage and record in the field; data syncs when you are back online." },
  { icon: CalendarCheck, title: "Service calendar", text: "Hour- and date-based reminders from the operator manuals." },
  { icon: History, title: "Prediction history", text: "Every test is stored with its score and timestamp." },
]

export function AppDownloadSection() {
  return (
    <section id="app" className="py-24 px-4">
      <div className="container mx-auto max-w-6xl">
        <div className="rounded-[2rem] bg-primary text-primary-foreground overflow-hidden grid lg:grid-cols-[1.1fr_0.9fr]">
          <div className="p-8 md:p-12">
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-accent">Mobile app</p>
            <h2 className="mt-4 text-3xl md:text-4xl font-bold tracking-tight text-balance">
              The full system lives in the Android app.
            </h2>
            <p className="mt-4 text-primary-foreground/80 leading-relaxed max-w-lg">
              The web demo scores a single clip. The app adds tractor profiles, personal baselines, usage tracking and
              maintenance scheduling.
            </p>

            <ul className="mt-8 grid sm:grid-cols-2 gap-5">
              {features.map((f) => (
                <li key={f.title} className="flex gap-3">
                  <f.icon className="w-5 h-5 mt-0.5 shrink-0 text-accent" />
                  <div>
                    <p className="font-semibold">{f.title}</p>
                    <p className="text-sm text-primary-foreground/75 leading-relaxed">{f.text}</p>
                  </div>
                </li>
              ))}
            </ul>

            <Button asChild size="lg" variant="secondary" className="mt-9 rounded-full h-12 px-7 bg-accent text-accent-foreground hover:bg-accent/90">
              <a href={APK_URL} target="_blank" rel="noopener noreferrer">
                <Download className="w-4 h-4 mr-2" />
                Download Android APK
              </a>
            </Button>
            <p className="mt-3 text-xs text-primary-foreground/70">
              Prototype build, installed outside the Play Store. Enable &ldquo;install unknown apps&rdquo; to sideload.
            </p>
          </div>

          <div className="relative bg-black/15 flex items-center justify-center p-8">
            <img
              src="/mobile-app-interface-tractor-maintenance-dashboard.jpg"
              alt="TractorCare mobile app dashboard"
              className="w-full max-w-[18rem] rounded-[1.75rem] border-4 border-primary-foreground/20 shadow-2xl"
            />
          </div>
        </div>
      </div>
    </section>
  )
}
