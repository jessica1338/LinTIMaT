# LinTIMaT
Lineage Tracing by Integrating Mutation and Transcriptomic data

This github repository provides the examples of running LinTIMaT (Lineage Tracing by Integrating Mutation and Transcriptomic data) for the paper "Single-cell Lineage Tracing by Integrating CRISPR-Cas9 Mutations with Transcriptomic Data". See the abstract below:
Recent studies combine two novel technologies, single-cell RNA-sequencing and CRISPR-Cas9 barcode editing for elucidating developmental lineages at the whole organism level. While these studies provided several insights regarding developmental lineages, they face several computational challenges. First, the trees are reconstructed based on noisy and often saturated random mutation data. Additionally, due to the randomness of the mutations, lineages from multiple experiments cannot be combined to reconstruct a consensus lineage. To address these issues, we developed a novel method, LinTIMaT, which reconstructs cell lineages in a maximum-likelihood framework by integrating mutation and expression data. Our analysis shows that expression data helps resolve the ambiguities arising in individual lineages when inferred based on mutations alone, while also enabling the integration of different individual lineages for the reconstruction of a consensus lineage. Lineages reconstructed by LinTIMaT provide better cell type coherence, improve the functional significance of gene sets and can provide new insights on progenitors and differentiation pathways.

![method_overview](images/method_overview.PNG)

