# LinTIMaT: Lineage Tracing by Integrating Mutation and Transcriptomic data

This github repository provides the examples of running LinTIMaT (Lineage Tracing by Integrating Mutation and Transcriptomic data) for the paper "Single-cell Lineage Tracing by Integrating CRISPR-Cas9 Mutations with Transcriptomic Data". See the abstract below:
Recent studies combine two novel technologies, single-cell RNA-sequencing and CRISPR-Cas9 barcode editing for elucidating developmental lineages at the whole organism level. While these studies provided several insights regarding developmental lineages, they face several computational challenges. First, the trees are reconstructed based on noisy and often saturated random mutation data. Additionally, due to the randomness of the mutations, lineages from multiple experiments cannot be combined to reconstruct a consensus lineage. To address these issues, we developed a novel method, LinTIMaT, which reconstructs cell lineages in a maximum-likelihood framework by integrating mutation and expression data. Our analysis shows that expression data helps resolve the ambiguities arising in individual lineages when inferred based on mutations alone, while also enabling the integration of different individual lineages for the reconstruction of a consensus lineage. Lineages reconstructed by LinTIMaT provide better cell type coherence, improve the functional significance of gene sets and can provide new insights on progenitors and differentiation pathways.

![method_overview](images/method_overview.PNG)

In this github repository, we provide the example code to reconstruct similar zebrafish lineage tree listed in the paper.   We also provide the code for visualizing the trees in the paper.  

The raw dataset is take from https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE105010.  

The processed input files for ZF1 and ZF3 is here https://drive.google.com/file/d/1DI4N7eG7Rn4hopVYGV6iILHilvz8LbQA/view?usp=sharing  

## Tree visualization website
You can see the tree visualization for individual fish ZF1, ZF3 and consensus tree for these two fish in the following website: https://jessica1338.github.io/LinTIMaT/  
If you click any node on each tree you can see additional information such as proportion of different cell types or mutations associated with the node.  
The source code for visualizing the json files for each tree is in docs folder of this repository.  
We also provide the code (in visualization folder of this repository) to reproduce the json files for these trees from LinTIMaT output. 

See http://htmlpreview.github.io/?https://github.com/jessica1338/LinTIMaT/blob/master/visualization/reproducing_LinTIMaT_tree_json.html for the codes in the html output of jupyter notebook
or you can change directory into LinTIMaT/visualization and execute "python reproducing_LinTIMaT_tree_json.py" then you will get the same json files in the LinTIMaT/docs/tree_data folder.

## Example of running LinTIMaT on zebrafish data
Download this repository, and download the the processed input file from https://drive.google.com/file/d/1DI4N7eG7Rn4hopVYGV6iILHilvz8LbQA/view?usp=sharing, unzip the file data.zip and move the file "ZF1_F3_DrImpute.txt" and "ZF3_F6_DrImpute.txt" to the data/ folder of this repository.

### TODO: Hamim write the part for reproducing similar tree here


## INPUT of LinTIMaT
LinTIMaT runs on single cell RNA-Seq data where each cell has mutated barcodes. If the RNA-Seq data is raw reads, the instruction about how to calculate continuous expression based on RNA-Seq raw reads can be found in many other studies, e.g (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4728800/). 

Once we get the continuous RNA-Seq gene expression, the expression data should be transformed to log space for example by log2(x+1) where x could represent the gene expression in terms of RPKM, FPKM or TPM depending.   
For the mutated barcode for each cell, it should be given as a single string with mutation events on different sites separated by "-" character. Mutation events can be NONE when no mutation is observed on this site, or conprise with deletion/insertion length and the position. For example, assumes that there are 4 possible sites for mutation, one possible mutation sring can be NONE-10D+113-NONE-5I+256+ATCGA. This means that for site 1 and site 3, there is no mutation, for site 2, there is a deletion of 10 basepairs happend at position 113, for site 4, there is a insertion of 5 base pairs (ATCGA) at position 256.

The input file for LinTIMaT has the following formatting requirements:  
* __Header Row__   
	First 3 columns are "Cells","ClusterIdent","HMID" and the remaining columns are gene names.  
* __Data Rows__   
	* __1st column__: Cell ID, String, represents the ID for the cell. (should be unique)  
	* __2nd column__: Cell label, Integer, represents  the label of the cell (e.g cell type if known). In most cases, we don't have any prior knowledge of the cell type. In this case, use 0 instead. Or, you can use any name you want to label each cell. We don't use this information in building the lineage tree and it's only used to mark the cells in visualization and calculate ARI.  
	* __3rd column__: Cell mutation barcode, String, mutation events on different sites separated by "-" character.  
	* __4th- columns__: Gene expression values.    
    
    Note that each entry of the data is separated by "\t" character.  
	Example processed input file can be downloaded from here:  
    https://drive.google.com/file/d/1DI4N7eG7Rn4hopVYGV6iILHilvz8LbQA/view?usp=sharing

## Hyper parameters of LinTIMaT
### TODO: Hamim write the part for explaning hyper parameters for running tree search here

## OUTPUT of LinTIMaT
### TODO: Hamim write the part for specifying output format and how to generate output files (newick and matching files) for visualizing individual and consensus trees.

