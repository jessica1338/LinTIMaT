import pandas as pd
from newick import loads,read
from collections import defaultdict

def load_color_annotation_dictionary(color_annotation_file):
#     color_annotation_file = "ClusterColors.txt"
    label_type_dictionary={}
    label_color_dictionary={}
    color_df = pd.read_csv(color_annotation_file,sep="\t")
    labels=color_df[color_df.columns[0]]
    label_types=color_df[color_df.columns[1]]
    label_type_dictionary.update(dict(zip(labels, label_types)))
    label_colors=color_df[color_df.columns[2]]
    label_color_dictionary.update(dict(zip(labels, label_colors)))
    return label_type_dictionary, label_color_dictionary
def load_label_mutation_annotation_dictionary(data_files):
    cell_label_dictionary={}
    cell_HMID_dictionary={}
    for data_file in data_files:
        df=pd.read_csv(data_file,sep="\t")
#         dfs+=[df]
        cell_names=df[df.columns[0]]
        cell_labels=df[df.columns[1]]
        cell_label_dictionary.update(dict(zip(cell_names, cell_labels)))
        cell_HMIDs=df[df.columns[2]]
        cell_HMID_dictionary.update(dict(zip(cell_names, cell_HMIDs)))
#         print len(cell_label_dictionary.items())
#         print len(cell_HMID_dictionary.items())
    return cell_label_dictionary, cell_HMID_dictionary
def load_mutation_event_loaction_dictionary(cell_HMID_dictionary):
    small_event_location_map=defaultdict(set)
    for key,value in cell_HMID_dictionary.items():
        splits=value.split("-")
        for i,sp in enumerate(splits):
            small_event_location_map[sp].add(i)
    return small_event_location_map
def load_individual_tree_visualization_file(non_binary_tree_file):
    lines=open(non_binary_tree_file,'r').readlines()
    tree_newick=lines[1].split("\n")[0]
    tree_root = loads(tree_newick)[0]
    # print tree_newick
    mutation_node=[]
    cluster_node=[]
    mutation_node_event_dict=defaultdict(list)
    ln=0
    for i in range(3,len(lines)):
        if lines[i].startswith("Cluster Nodes"):
            ln=i
            break
        line = lines[i].split("\n")[0]
    #     print line
        splits=line.split(" ")
        mutation_node_name = splits[0]
        mutation_node+=[mutation_node_name]
        for sp in splits[1:]:
            if sp.startswith("["):
                sp=sp[1:]
            if sp.endswith("]") or sp.endswith(",") :
                sp=sp[:-1]
            mutation_node_event_dict[mutation_node_name]+=[sp]
    for i in range(ln+1,len(lines)):
        cluster_node+=[lines[i].split("\n")[0]]
    return tree_root, mutation_node,cluster_node,mutation_node_event_dict

def write_individual_tree_non_binary(node,mutation_node,cluster_node,mutation_node_event_dict,cell_label_dictionary,label_color_dictionary,label_type_dictionary,cell_HMID_dictionary,small_event_location_map, level=0, parent=None,mutation_set=set(),group=[]):
    node_dict={}
    node_dict["name"]=node.name
    node_dict["parent"]="null"
    node_dict["event"]="NONE_NONE_NONE_NONE_NONE_NONE_NONE_NONE_NONE_NONE"
#     node_dict["commonEvent"]="*_*_*_*_*_*_*_*_*_*"
    node_dict["rootDist"]=level+1
    node_dict["organProportions"]={"ALL": 1.0}
    node_dict["nodecolor"]="black"
    if node.name in mutation_node:
        node_dict["nodecolor"]="blue"
        mutation_set|=set(mutation_node_event_dict[node.name])
        node_dict["mutation"]="_".join(mutation_node_event_dict[node.name])
    else:
        node_dict["mutation"]="NONE"
    if node.name in cluster_node:
        node_dict["nodecolor"]="red"
    if parent != None:
        node_dict["parent"] = parent.name
#     print mutation_set
    events=["*"]*10
    for event in mutation_set:
        event_locs=small_event_location_map[event]
        for event_loc in event_locs:
            events[event_loc]=event
    node_dict["commonEvent"] = "_".join(events)
#     print node_dict["commonEvent"]
    children=[]
    if len(node.descendants) == 0:
        #leaf
        cl=cell_label_dictionary[node.name]
        lc = label_color_dictionary[cl]
        node_dict["nodecolor"]="white"
        node_dict["cladeColor"]="#"+lc
        node_dict["cellType"]=label_type_dictionary[cl]
        node_dict["event"] = "_".join(cell_HMID_dictionary[node.name].split("-"))
        node_dict["organProportions"]={label_type_dictionary[cl]: 1.0}
        node_dict["num_cell_under_this_node"]=1
    else:
        node_dict["organProportions"]=defaultdict(lambda:0)
        cell_count=0
        for child in node.descendants:
            if child.name =="normal":
                continue
            if child.name not in group and len(group)>0 and level==1:
                print child.name
                print group
                continue
            children += [write_individual_tree_non_binary(child,mutation_node,cluster_node,mutation_node_event_dict,cell_label_dictionary,label_color_dictionary,label_type_dictionary,cell_HMID_dictionary,small_event_location_map, level = level+1, parent = node, mutation_set=mutation_set,group=group)]
#             print children[-1]
            ops=children[-1]["organProportions"]
            cc=children[-1]["num_cell_under_this_node"]
            for key,val in ops.items():
                node_dict["organProportions"][key]+=val*cc
            cell_count+=cc
        node_dict["num_cell_under_this_node"]=cell_count

        total=sum(node_dict["organProportions"].values())
        for key in node_dict["organProportions"].keys():
            node_dict["organProportions"][key]/=float(total)
#         print node_dict["organProportions"]
    node_dict["children"]=children
    mutation_set-=set(mutation_node_event_dict[node.name])
    return node_dict

def update_node_leaf_dictionary(root,node_leaf_dictionary,level=0):
    #print level
    node_leaf_dictionary[root.name]=root.get_leaf_names()
    #print root, root.descendants
    for node in root.descendants:
        update_node_leaf_dictionary(node,node_leaf_dictionary,level+1)
def get_matched_cluster_node_leaf_dictionary(matching_file_name):
    matched_tree_file_lines=open(matching_file_name,"r").readlines()
    ln=0
    original_tree_newicks=[]
    matched_tree_newicks=[]
    matched_cluster={}
    while(ln<len(matched_tree_file_lines)):
        line=matched_tree_file_lines[ln]
        if line=="Original tree newick\n":
            original_tree_newicks+=[matched_tree_file_lines[ln+1][:-1]]
            matched_tree_newicks+=[matched_tree_file_lines[ln+3][:-1]]
            ln+=4
        else:
            ln+=2
            break  
    while(ln<len(matched_tree_file_lines)):
        line=matched_tree_file_lines[ln]
        line2=matched_tree_file_lines[ln+1]
        key=line[:-1]
        values=line2.split("\n")[0].split(" ")[:-1]
        matched_cluster[key]=values
#         print key, values
        ln+=2
    node_leaf_dictionary_list=[]
    for newick_string in original_tree_newicks:
        tree = loads(newick_string)
        node_leaf_dictionary={}
        update_node_leaf_dictionary(tree[0],node_leaf_dictionary,0)
#         print node_leaf_dictionary
        node_leaf_dictionary_list+=[node_leaf_dictionary]
    return matched_cluster,node_leaf_dictionary_list,matched_tree_newicks
def write_consensus_tree_json_dict(node,matched_cluster, node_leaf_dictionary_list,label_type_dictionary,label_color_dictionary,cell_HMID_dictionary,cell_label_dictionary, level=0, parent=None, fish_index = -1, calc_distance_by_cell_pairs=False,group=[]):
    node_dict={}
    node_dict["name"]=node.name

    node_dict["parent"]="null"
    node_dict["event"]="NONE_NONE_NONE_NONE_NONE_NONE_NONE_NONE_NONE_NONE"
    node_dict["commonEvent"]="*_*_*_*_*_*_*_*_*_*"
    node_dict["rootDist"]=level+1
    node_dict["organProportions"]=defaultdict(lambda:0)
    node_dict["num_cell_under_this_node"]=0
    if parent != None:
        node_dict["parent"] = parent.name
    children=[]
    if len(node.descendants) == 0:
        node_dict["nodecolor"]="red"
        for i,cluster in enumerate(matched_cluster[node.name]):
            fish_cell_type_count_dict=defaultdict(lambda:0)
            if fish_index!= -1 and i != fish_index:
                continue
            fish_node_dict={}
            fish_node_dict["name"]="f"+str(i)
            fish_node_dict["parent"]=node.name
            fish_node_dict["commonEvent"]="*_*_*_*_*_*_*_*_*_*"
            fish_node_dict["event"]="NONE_NONE_NONE_NONE_NONE_NONE_NONE_NONE_NONE_NONE"
            fish_node_dict["rootDist"]=level+2
            fish_node_dict["organProportions"]=defaultdict(lambda:0)
            fish_node_dict["nodecolor"]="blue"
            fish_node_dict["num_cell_under_this_node"]=0
            fish_children=[]
            cluster_mean=[]
            for cell in node_leaf_dictionary_list[i][cluster]:
                cell_dict={}
                cl=cell_label_dictionary[cell]
                lc = label_color_dictionary[cl]
#                 exp = cell_exp_dictionary[cell]
#                 cluster_mean+=[exp]
                cell_dict["name"]=cell
                if fish_index == -1:
                    cell_dict["parent"]="f"+str(i)
                    cell_dict["rootDist"]=level+3
                else:
                    cell_dict["parent"]=node.name
                    cell_dict["rootDist"]=level+2
                cell_dict["commonEvent"]="*_*_*_*_*_*_*_*_*_*"
#                 cell_dict["organProportions"]={"ALL": 1.0}
                
                cell_dict["nodecolor"]="white"
                cell_dict["cladeColor"]="#"+lc
                cell_dict["cellType"]=label_type_dictionary[cl]
                cell_dict["organProportions"]={label_type_dictionary[cl]: 1.0}
                cell_dict["num_cell_under_this_node"]=1
                fish_node_dict["num_cell_under_this_node"]+=1
                node_dict["num_cell_under_this_node"]+=1
                cell_dict["event"] = "_".join(cell_HMID_dictionary[cell].split("-"))
                fish_node_dict["organProportions"][label_type_dictionary[cl]]+=1
                node_dict["organProportions"][label_type_dictionary[cl]]+=1
#                 print cell_dict["event"]
                fish_children+=[cell_dict]
            factor=1.0/sum(fish_node_dict["organProportions"].itervalues())
            for k in fish_node_dict["organProportions"]:
                fish_node_dict["organProportions"][k] = fish_node_dict["organProportions"][k]*factor
            if fish_index ==-1:
                fish_node_dict["children"]=fish_children
                children+=[fish_node_dict]
            else:
                children=fish_children
        factor=1.0/sum(node_dict["organProportions"].itervalues())
        for k in node_dict["organProportions"]:
            node_dict["organProportions"][k] = node_dict["organProportions"][k]*factor
    else:
        cell_count=0
        for child in node.descendants:
            if child.name =="normal":
                continue
            if child.name not in group and len(group)>0 and level==1:
                continue
            children += [write_consensus_tree_json_dict(child,matched_cluster, node_leaf_dictionary_list,label_type_dictionary,label_color_dictionary,cell_HMID_dictionary,cell_label_dictionary, level = level+1, parent = node,fish_index=fish_index,calc_distance_by_cell_pairs=calc_distance_by_cell_pairs,group=group)]
#             print children[-1]["name"]
            ops=children[-1]["organProportions"]
            cc=children[-1]["num_cell_under_this_node"]
            for key,val in ops.items():
                node_dict["organProportions"][key]+=val*cc
            cell_count+=cc
        node_dict["num_cell_under_this_node"]=cell_count
        total=sum(node_dict["organProportions"].values())
        for key in node_dict["organProportions"].keys():
            node_dict["organProportions"][key]/=float(total)
#         print node_dict["organProportions"]
    node_dict["children"]=children
    return node_dict