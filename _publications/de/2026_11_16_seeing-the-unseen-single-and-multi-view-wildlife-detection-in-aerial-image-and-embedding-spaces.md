---
lang: de
page_id: pub:seeing-the-unseen-single-and-multi-view-wildlife-detection-in-aerial-image-and-embedding-spaces
permalink: /publications/seeing-the-unseen-single-and-multi-view-wildlife-detection-in-aerial-image-and-embedding-spaces/
date: 2026-11-16  # accepted for VISAPP 2027, not published yet; dated today because future-dated entries are not rendered
title: "Seeing the Unseen: Single- and Multi-View Wildlife Detection in Aerial Image and Embedding Spaces"
reference: 'Praschl C., Schedl D. “Seeing the Unseen: Single- and Multi-View Wildlife
  Detection in Aerial Image and Embedding Spaces“, International Conference on Computer
  Vision Theory and Applications (VISAPP) 2027. Angenommen (noch nicht erschienen).'
categories: [cv, ml, geo]
---

Die Wildtierdetektion mit unbemannten Luftfahrzeugen in bewaldeten Gebieten wird stark durch die Verdeckung durch Vegetation eingeschränkt. Videoaufnahmen liefern jedoch wiederholte Beobachtungen aus benachbarten Blickwinkeln, die komplementäre Evidenz sichtbar machen können. Wir untersuchen diese Redundanz entlang zweier expliziter Achsen: Single-View gegenüber Multi-View sowie Bildraum gegenüber Embedding-Raum. Anhand von 72 georeferenzierten RGB-Thermal-Luftaufnahmen konstruieren wir synthetische Aperturen aus 31 Ansichten und evaluieren eingefrorene DINOv3- und V-JEPA-2.1-Features mittels fünffacher Kreuzvalidierung auf Szenenebene mit drei Seeds. Mit einem trainierten Detektor im Bildraum (YOLO26x) erhöht die Multi-View-Integration den Recall für Tiere, die in der zentralen Ansicht verdeckt sind, um das 1,70-Fache bei RGB und das 2,04-Fache bei Thermal, während der Recall für zentral sichtbare (nicht verdeckte) Tiere unverändert bleibt. Im Embedding-Raum liegt der Multi-View-Gewinn über beide Encoder (DINOv3, V-JEPA 2.1) und beide Modalitäten hinweg konsistent beim 1,50- bis 1,68-Fachen. Eingefrorene DINOv3-Embeddings bringen eine weitere, weitgehend unabhängige Verbesserung gegenüber demselben Detektor-Head auf Bildpixeln: Bei gleicher Anzahl an Ansichten steigern sie den Recall verdeckter Tiere um das 1,66- bis 1,69-Fache bei Thermal und das 3,04- bis 3,89-Fache bei RGB, sodass die Multi-View-DINOv3-Konfiguration insgesamt am stärksten ist und das 2,49-Fache (Thermal) bzw. 4,77-Fache (RGB) des Recalls verdeckter Tiere der Single-View-Bild-Baseline erreicht.