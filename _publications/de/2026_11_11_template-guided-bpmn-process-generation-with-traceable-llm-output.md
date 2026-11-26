---
lang: de
page_id: pub:template-guided-bpmn-process-generation-with-traceable-llm-output
permalink: /publications/template-guided-bpmn-process-generation-with-traceable-llm-output/
date: 2026-11-11  # ISM 2026 conference start date (Nov 11–13); exact day unknown
title: Template-Guided BPMN Process Generation with Traceable LLM Output and Deterministic
  Guardrails
reference: Dalkilic M., Pointner A., Zwettler G.A. “Template-Guided BPMN Process Generation
  with Traceable LLM Output and Deterministic Guardrails“, ISM 2026, Procedia Computer Science.
categories: [ml, pm]
projects: [projects:viper]
---

Die Geschäftsprozessmodellierung in BPMN 2.0 ist eine manuelle, expertiseintensive Tätigkeit. Große Sprachmodelle (LLMs) können zwar strukturiertes XML erzeugen, ihr Einsatz für die BPMN-Generierung bringt jedoch unkontrolliert erfundene Prozesselemente, strukturell ungültige Modelle und divergierende Reparaturschleifen mit sich. Diese Arbeit stellt VIPA vor, eine modulare Pipeline-Architektur, die LLM-basierte BPMN-Generierung mit deterministischen Leitplanken kombiniert, um aus natürlichsprachlichen Anforderungen strukturell gültige Prozessdiagramme zu erzeugen. Der Ansatz maximiert die Wiederverwendung bestehender Vorlagen durch eine Matching- und wortgetreue Übernahmestrategie und erlaubt zugleich die kontrollierte Erzeugung neuer Elemente, wo die Prozesslogik dies erfordert. Die Ausgabe wird in einem dreistufigen Verfahren aus Rückverfolgbarkeitsprüfung, LLM-basierter Strukturanalyse und regelbasiertem Linting validiert. Eine deterministische Bereinigung nach der Generierung verhindert divergierende Reparaturschleifen. Die Evaluierung mit 12 Prompts aus Unternehmensabläufen in je drei unabhängigen Durchläufen zeigt, dass die Pipeline im Schnitt 80 % der Aufgaben aus Vorlagen übernimmt; 83 % der Prompts erreichen innerhalb von zwei Reparaturschritten null strukturelle Fehler, im Mittel sind 1,2 Schritte nötig. Alle erzeugten Prozesse sind vollständig strukturell gültig, neu generierte Aufgaben werden über ein Synthetic-Attribut explizit gekennzeichnet.
