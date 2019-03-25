"""

    #Last Edit : 21:03:19 02:35:21
    mini log:
            #added constraints for addition and deletion
            #imporved bug for bool has no attribute 

"""

import copy #for deepcopy
import math #for maths intensive operations
import time #for execution time computation
#from numba import jit

def deep_copy(adj2):    #auxilary module for copying the adjacency list
    var={}
    var=copy.deepcopy(adj2)
    return var

# its an ordered entry with {Node, Type, CT, Delay, Weight of Edge}
adj={} #dictionary for adjacency list
node_CT={} #stores computation time corresponding to each node

def initialize(raw_file):   #first function for parsing the input and getting all nodes
    data=open(raw_file,'r')
    if not data:
        print ("File doesn't exist")
    adj['GInput']=[]   #in adj list dic we created two lists
    adj['GOutput']=[]
    node_CT['GInput']=0   #same in node computation time dictionary
    node_CT['GOutput']=0
    for line in data :
        arr=line.split()
        a=line[line.find("(")+1:line.find(")")]
        if '#' not in line and line!='\n' and 'INPUT' not in line and 'OUTPUT' not in line:
            adj[arr[0]]=[] #we store all nodes provided on lhs
        if 'INPUT' in line or 'OUTPUT' in line :
            adj[a]=[] #and we mark input or output nodes

is_delete = False #for tracking if any node has come for deletion
is_add = False #for tracking addition  
Input=[]    #list for IP
Output=[]
Add = []    #for addition of extra registers
Del_1 = []  #for deletion of extra registers
Del_2 = []
DFF_list=[] #for storing the nodes associated with registeres
DFF_CT = INPUT_CT = OUTPUT_CT = 0   #computational delays
NOR_CT = NOT_CT = AND_CT = NAND_CT = OR_CT = 1
NodeTypes={}    #the dictionary stores the type of each node

def build_graph(raw_file): #Here all the operations are getting filtered
    data=open(raw_file,'r')
    for line in data :  #here parsing of the input file takes place
        var=[] 
        var2=[]
        arr=line.split()
        if '#' not in line: #we read if its not a comment 
            a=line[line.find("(")+1:line.find(")")]
            a1=a.split(',')
            if 'INPUT' in line: #we find the input nodes
                Input.append(a) #we append it in input list
                node_CT[a]=INPUT_CT
            elif 'OUTPUT' in line:  #we find the output nodes
                Output.append(a)
                node_CT[a]=OUTPUT_CT
            elif 'AND' in line and 'NAND' not in line:
                for i in range(0,len(a1)):
                    m=a1[i].split()
                    node_CT[arr[0]]=AND_CT
                    NodeTypes[arr[0]]='AND'
                    adj[m[0]].append([arr[0],'AND',AND_CT,0,0])
            elif 'OR' in line and 'NOR' not in line:
                for i in range(0,len(a1)):
                    m=a1[i].split()
                    node_CT[arr[0]]=OR_CT
                    NodeTypes[arr[0]]='OR'
                    adj[m[0]].append([arr[0],'OR',OR_CT,0,0])
            elif 'NAND' in line:
                for i in range(0,len(a1)):
                    m=a1[i].split()
                    node_CT[arr[0]]=NAND_CT
                    NodeTypes[arr[0]]='NAND'
                    adj[m[0]].append([arr[0],'NAND',NAND_CT,0,0])
            elif 'NOR' in line :
                for i in range(0,len(a1)):
                    m=a1[i].split()
                    node_CT[arr[0]]=NOR_CT
                    NodeTypes[arr[0]]='NOR'
                    adj[m[0]].append([arr[0],'NOR',NOR_CT,0,0])
            elif 'NOT' in line:
                for i in range(0,len(a1)):
                    m=a1[i].split()
                    node_CT[arr[0]]=NOT_CT
                    NodeTypes[arr[0]]='NOT'
                    adj[m[0]].append([arr[0],'NOT',NOT_CT,0,0])
            elif 'DFF' in line :
                for i in range(0,len(a1)):
                    m=a1[i].split()
                    node_CT[arr[0]]=DFF_CT
                    DFF_list.append(arr[0])
                    adj[m[0]].append([arr[0],'DFF',DFF_CT,0,0])

def create_retiming_model(adj): #Here we populate the adj list with edge weights wrt IP & OP
    for i in range(0,len(Input)):
        adj['GInput'].append([Input[i],'INPUT',0,0,0])

    for i in range(0,len(Output)):
        adj[Output[i]].append(['GOutput','OUTPUT',0,0,0])

    var = copy.deepcopy(adj)
    return var

def weight_builder_DFS(adj, entry, i, p):   #Now we populate weights for rest of the nodes
    varNode=adj[entry][i][0]
    if(adj[varNode][0][1]=='DFF'): #if its DFF we keep moving forward
        p = p+1 #since we need to create delay
        return weight_builder_DFS(adj,varNode,i,p)
    else :
        adj[varNode][0][4]=adj[varNode][0][4]+1 + p    #we update weights
        return adj[varNode][0]

def weighted_graph_population(adj):
    for entry in adj:   #for every node in our adj list
        for i in range(0, len(adj[entry])):
            #print entry, adj[entry]
            if(adj[entry][i][1]=='DFF'):  #if the node type is DFF
                varNode = weight_builder_DFS(adj,entry,i,0)
                #varNode is the address location of the node
                var =[varNode[0],varNode[1],varNode[2],varNode[3],varNode[4]]
                #print entry, adj[entry]
                #print var
                #storing in the value not the address of the var node
                adj[entry][i]=var

unit_time = 1   #can be changed based on needs
keys=[]
keys2=[]
values = []

def repopulate_weighted_graph(adj_reweighted):
    n=0  
    for entry in adj_reweighted:
        if entry not in DFF_list:
            n=n+1   #counting entries which are not DFF
    M = unit_time*n
    for entry in adj_reweighted:
        for i in range(0,len(adj_reweighted[entry])):
            if(node_CT[entry]!=0):
                adj_reweighted[entry][i][4]=(M*adj_reweighted[entry][i][4])-node_CT[entry]

def counter(adj, i, entry, dictn):
    if entry not in dictn:
        dictn.append(entry)
        if entry in DFF_list:
            values.append(i)
            for var in adj[entry]:
                if var[0] in Output:
                    values.append(1)
                else:
                    counter(adj, 1, var[0], dictn)
        else:
            for var in adj[entry]:
                if var[0] in Output:
                    values.append(i+1)
                else:
                    counter(adj, i+1, var[0], dictn)
                
            

def form_adj_mat(adj):
    mat=[[float('inf') for x in range(len(adj)-len(DFF_list))] for y in range(len(adj)-len(DFF_list))]
    for i in range(len(mat[0])):
        mat[i][i]=0
    for entry in adj :
        if entry not in DFF_list:
            keys.append(entry)
    for entry in adj:
        if entry not in DFF_list:
            l=keys.index(entry)
            for i in range(len(adj[entry])):
                entry2=adj[entry][i][0]
                if entry2 not in DFF_list:
                    m=keys.index(entry2)
                    mat[l][m]=adj[entry][i][4]
    return mat

#   _______________________ Execution flow ___________________________
raw_file = input("Enter the file name : ")
c = 10
print(raw_file)
#c = int(raw_input('Enter the value of the c : '))
print("Processing " + raw_file + " . . . ")

#Parsing th input file and storing all the nodes and I/P & O/P
initialize(raw_file)

#here we create the adj list corresponding to the list provided
build_graph(raw_file)
 
i = 0


for entry in Input:
    dictn = [] 
    counter(adj, 1, entry, dictn)
    del dictn

counter = 0

'''
for i in values:
    if i > 5:
        counter = counter + 1
print counter

counter = 0

for i in values:
    if i > 10:
        counter = counter + 1
print counter

counter = 0

for i in values:
    if i > 15:
        counter = counter + 1
print counter

counter = 0
'''

for i in values:
    if counter < i:
        counter = i

print (values)

print (counter)
