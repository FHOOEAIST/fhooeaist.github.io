---
lang: de
page_id: pub:seeing-the-unseen-single-and-multi-view-wildlife-detection-in-aerial-image-and-embedding-spaces
permalink: /publications/seeing-the-unseen-single-and-multi-view-wildlife-detection-in-aerial-image-and-embedding-spaces/
date: 2027-02-28
early: true  # accepted for VISAPP 2027, not published yet; remove once the date has passed
title: "Seeing the Unseen: Single- and Multi-View Wildlife Detection in Aerial Image and Embedding Spaces"
reference: 'Praschl C., Schedl D. “Seeing the Unseen: Single- and Multi-View Wildlife
  Detection in Aerial Image and Embedding Spaces“, International Conference on Computer
  Vision Theory and Applications (VISAPP) 2027. Angenommen (noch nicht erschienen).'
categories: [cv, ml, geo]
projects: [projects:thumper]
---

Die Detektion von Wildtieren mittels Drohnen in bewaldeten Gebieten wird durch Vegetationsverdeckungen stark eingeschränkt. Videoaufnahmen ermöglichen jedoch wiederholte Beobachtungen aus benachbarten Blickwinkeln, die ergänzende Informationen liefern können. Wir untersuchen diese Redundanz entlang zweier Dimensionen: Einzelansicht gegenüber Mehrfachansicht sowie Bildraum gegenüber Embeddingraum. Anhand von 72 georeferenzierten RGB- und Thermal-Luftbildaufnahmen konstruieren wir synthetische Aufnahmen mit 31 Ansichten und evaluieren frozen DINOv3- und V-JEPA-2.1-Merkmale mittels fünffacher Kreuzvalidierung auf Szenenebene mit drei Seeds. Mit einem trainierten Bilddetektor (YOLO26x) erhöht die Integration mehrerer Ansichten den Recall für in der zentralen Ansicht verdeckte Tiere um den Faktor 1,70 bei RGB und 2,04 bei Thermalaufnahmen, während der Recall für zentral sichtbare (nicht verdeckte) Tiere unverändert bleibt. Im Einbettungsraum liegt der Mehrfachansichtgewinn über beide Encoder (DINOv3, V-JEPA 2.1) und Modalitäten hinweg konstant beim Faktor 1,50–1,68. Frozen DINOv3-Embeddings erzielen zudem eine weitgehend unabhängige Verbesserung gegenüber demselben Detektionskopf auf Bildpixeln: Bei gleicher Ansichtsanzahl steigern sie den Recall für verdeckte Tiere um den Faktor 1,66–1,69 bei Thermalaufnahmen und 3,04–3,89 bei RGB. Insgesamt erzielt die Mehrfachansicht mit DINOv3 die besten Ergebnisse, mit einem 2,49-fachen (Thermal) beziehungsweise 4,77-fachen (RGB) Recall für verdeckte Tiere gegenüber der Einzelansicht-Baseline im Bildraum.
