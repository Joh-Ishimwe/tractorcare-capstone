import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"

const faqs = [
  {
    question: "How does it detect a problem?",
    answer:
      "A recording is turned into 40 MFCC features and passed to a classifier that outputs an anomaly probability. The app can also compare the recording with that tractor's own healthy baseline.",
  },
  {
    question: "How accurate is it?",
    answer:
      "On our 295-clip tractor dataset, with recordings kept apart between training and test sets, the ResNet-like CNN reached about 94% accuracy and the best classical model about 81%. A baseline SVM missed all six held-out phone recordings, so field performance on new microphones is unproven. Treat results as a prototype signal, not a diagnosis.",
  },
  {
    question: "Does it replace a mechanic?",
    answer:
      "No. It is an early-warning aid and a reminder system. \"Abnormal\" means the sound differs from healthy examples, not that a specific part has failed.",
  },
  {
    question: "Does it work offline?",
    answer:
      "The Android app is designed offline-first: you can record and log usage without a connection and sync later. The web demo needs internet because it calls our hosted API.",
  },
  {
    question: "Which tractors are supported?",
    answer:
      "Maintenance rules come from the Massey Ferguson MF 240 and MF 375 operator manuals. Sound analysis is not yet validated per model.",
  },
  {
    question: "What happens to my recordings?",
    answer:
      "The web demo sends the clip to the hosted API to compute a score. This is a university project, so please do not upload anything sensitive.",
  },
]

export function FAQSection() {
  return (
    <section id="faq" className="py-24 px-4 bg-muted/60">
      <div className="container mx-auto max-w-3xl">
        <p className="eyebrow mb-4">FAQ</p>
        <h2 className="text-3xl md:text-4xl font-bold tracking-tight mb-10">Questions, answered plainly.</h2>
        <Accordion type="single" collapsible className="space-y-3">
          {faqs.map((faq, i) => (
            <AccordionItem key={i} value={`item-${i}`} className="border border-border rounded-xl px-5 bg-card">
              <AccordionTrigger className="text-left hover:no-underline py-4 font-semibold">{faq.question}</AccordionTrigger>
              <AccordionContent className="text-muted-foreground pb-4 leading-relaxed">{faq.answer}</AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </div>
    </section>
  )
}
