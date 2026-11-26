---
lang: en
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

Business process modeling in BPMN 2.0 is a manual, expertise-intensive activity. While Large Language Models (LLMs) can generate structured XML, applying them to BPMN generation introduces uncontrolled fabrication of process elements, structural invalidity, and divergent repair loops. This paper presents VIPA, a modular pipeline architecture that combines LLM-based BPMN generation with deterministic guardrails to produce structurally valid process diagrams from natural language requirements. The approach maximizes template reuse through a matching and verbatim extraction policy while allowing controlled generation of new elements when required by the process logic. Output is validated through a three-phase system combining traceability checks, LLM structural analysis, and rule-based linting. Deterministic post-generation sanitization prevents repair loop divergence. Evaluation across 12 enterprise workflow prompts over three independent runs shows that the pipeline achieves an average template reuse rate of 80%, with 83% of prompts converging to zero structural errors within two repair iterations and an overall average of 1.2 iterations. All generated processes reach full structural validity, with newly generated tasks explicitly tracked through a synthetic attribution flag.
