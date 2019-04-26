
# coding: utf-8

# In[1]:


from visualization_utility import *
import json


# In[2]:


label_type_dictionary, label_color_dictionary=load_color_annotation_dictionary("../data/ClusterColors.txt")


# In[3]:


# label_type_dictionary


# In[4]:


# label_color_dictionary


# In[5]:


data_files=[]
data_files+=["../data/ZF1_F3.txt_label_HMID.txt"]
data_files+=["../data/ZF3_F6.txt_label_HMID.txt"]


# In[6]:


cell_label_dictionary, cell_HMID_dictionary=load_label_mutation_annotation_dictionary(data_files)


# In[7]:


# cell_label_dictionary


# In[8]:


# cell_HMID_dictionary


# In[9]:


small_event_location_map=load_mutation_event_loaction_dictionary(cell_HMID_dictionary)


# In[10]:


# small_event_location_map


# # producing json file for visualizing consensus tree

# In[11]:


# matching_file_name contains the matching information of how individual tree clusters are mapped to consensus clusters
matching_file_name = '../data/ZF1_ZF3_consensus_matching_file.txt'
matched_cluster,node_leaf_dictionary_list,matched_tree_newicks = get_matched_cluster_node_leaf_dictionary(matching_file_name)


# In[12]:


# matched_cluster


# In[13]:


# matched_tree_newicks


# In[14]:


# consensus_newick_file_name is the newick tree string for consensus tree, each leaf node corresponds to a consensus cluster
consensus_newick_file_name="../data/ZF1_ZF3_consLineage_nonBinary.newick"
cons_newick_string = open(consensus_newick_file_name,"r").readlines()[0][:-1]
cons_tree = loads(cons_newick_string)
tree_root = cons_tree[0]
out_file_name = "ZF1_ZF3_consLineage_nonBinary.json"
json_dict=write_consensus_tree_json_dict(tree_root,fish_index=-1,matched_cluster=matched_cluster, node_leaf_dictionary_list=node_leaf_dictionary_list,label_type_dictionary=label_type_dictionary,label_color_dictionary=label_color_dictionary,cell_HMID_dictionary=cell_HMID_dictionary,cell_label_dictionary=cell_label_dictionary)
out_str= json.dumps(json_dict, sort_keys=False,indent=4, separators=(',', ': '))
fp = open(out_file_name,"w")
fp.write("["+out_str+"]")
fp.close()


# # producing json file for visualizing individual tree ZF3

# In[15]:


# ZF3_non_binary_tree_file is the file for visualizing individual tree ZF3, it contains the newick tree string and information of mutation nodes and cluster nodes 
ZF3_non_binary_tree_file="../data/ZF3_F6_nonbinary_tree_newick_for_visualization.txt"
tree_root, mutation_node,cluster_node,mutation_node_event_dict=load_individual_tree_visualization_file(ZF3_non_binary_tree_file)
json_dict=write_individual_tree_non_binary(tree_root,mutation_node,cluster_node,mutation_node_event_dict,cell_label_dictionary,label_color_dictionary,label_type_dictionary,cell_HMID_dictionary,small_event_location_map)
out_file_name="individual_non_binary_ZF3_final.json"
out_str= json.dumps(json_dict, sort_keys=False,indent=4, separators=(',', ': '))
fp = open(out_file_name,"w")
fp.write("["+out_str+"]")
fp.close()


# # producing json file for visualizing individual tree ZF1

# In[16]:


# ZF1_non_binary_tree_file is the file for visualizing individual tree ZF1, it contains the newick tree string and information of mutation nodes and cluster nodes 
ZF1_non_binary_tree_file="../data/ZF1_F3_nonbinary_tree_newick_for_visualization.txt"
tree_root, mutation_node,cluster_node,mutation_node_event_dict=load_individual_tree_visualization_file(ZF1_non_binary_tree_file)
json_dict=write_individual_tree_non_binary(tree_root,mutation_node,cluster_node,mutation_node_event_dict,cell_label_dictionary,label_color_dictionary,label_type_dictionary,cell_HMID_dictionary,small_event_location_map)
out_file_name="individual_non_binary_ZF1_final.json"
out_str= json.dumps(json_dict, sort_keys=False,indent=4, separators=(',', ': '))
fp = open(out_file_name,"w")
fp.write("["+out_str+"]")
fp.close()

