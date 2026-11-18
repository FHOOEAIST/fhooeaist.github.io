---
lang: en
page_id: pub:seeing-the-unseen-single-and-multi-view-wildlife-detection-in-aerial-image-and-embedding-spaces
permalink: /publications/seeing-the-unseen-single-and-multi-view-wildlife-detection-in-aerial-image-and-embedding-spaces/
date: 2027-02-28
early: true  # accepted for VISAPP 2027, not published yet; remove once the date has passed
title: "Seeing the Unseen: Single- and Multi-View Wildlife Detection in Aerial Image and Embedding Spaces"
reference: 'Praschl C., Schedl D. “Seeing the Unseen: Single- and Multi-View Wildlife
  Detection in Aerial Image and Embedding Spaces“, International Conference on Computer
  Vision Theory and Applications (VISAPP) 2027. Accepted (not published yet).'
categories: [cv, ml, geo]
projects: [projects:thumper]
---

Wildlife detection from uncrewed aerial vehicles in forested environments is strongly limited by vegetation occlusion, yet video recordings provide repeated observations from nearby viewpoints that may reveal complementary evidence. We study this redundancy along two explicit axes: single view versus multi view, and image space versus embedding space. Using 72 georeferenced aerial RGB–thermal recordings, we construct 31-view synthetic apertures and evaluate frozen DINOv3 and V-JEPA 2.1 features under scene-level five-fold cross-validation with three seeds. With a trained image-space detector (YOLO26x), multi-view integration increases recall on animals hidden in the central view by 1.70× on RGB and 2.04× on thermal, while recall on centrally visible (non-occluded) animals remains unchanged. In embedding space, the multi-view gain is consistently 1.50–1.68× across both encoders (DINOv3, V-JEPA 2.1) and both modalities. Frozen DINOv3 embeddings provide a further, largely independent improvement over the same detector head on image pixels: at fixed view count they raise hidden-animal recall by 1.66–1.69× on thermal and 3.04–3.89× on RGB, so that the multi-view DINOv3 condition is strongest overall, with 2.49× (thermal) and 4.77× (RGB) the hidden-animal recall of the single-view image baseline.