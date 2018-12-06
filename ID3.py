from math import log
import json

positive,negative = 'Y','N'
#-----------------------------------------------------------------------------------------------
def class_count(data,index) :		#Return class_label (#+ve,#-ve)
	return sum(1 for i in data if i[index]==positive),sum(1 for i in data if i[index]==negative)

def entropy(class_counts) :	# Returns -E(pi*log2(pi))
	return -sum((float(i)/sum(class_counts))*log(float(i)/sum(class_counts),2) 
	             if i else 0 for i in class_counts)

def attribute_count(data,index,class_index) :	# Returns {child : (positive_count,negative_count)} set
	child      = {i[index] for i in data}
	attr_count = {}
	for i in child :
		attr_count.update({i : (sum(1 for j in data if (j[index],j[class_index])==(i,positive)),
		                        sum(1 for j in data if (j[index],j[class_index])==(i,negative))) })
	return attr_count

def attribute_entropy(attribute_counts,class_counts) :	# Returns E[(|Sv|/|S|)*Entropy(Sv) ]
	return sum( (float(sum(count))/sum(class_counts))*entropy(count)
	             for count in attribute_counts.values() )

def partition_data(data,index,child_value) :	#Splits , removes unecessary column table and 
												#then joins so table is used for next node seletion
	return [i[:index]+i[index+1:] for i in data if i[index]==child_value]

#-----------------------------------------------------------------------------------------------
def ID3(header,data) :
	if data :
		for i in data : 
			if len(i)<=1 : return
		class_counts = class_count(data,-1)
		if(class_counts[1]==0) : return positive
		if(class_counts[0]==0) : return negative

		class_entropy= entropy(class_counts)
		node_contest = {}
		for i in range(len(data[0])-1) :
			attr_entropy = attribute_entropy(attribute_count(data,i,-1) , class_counts)
			node_contest[class_entropy-attr_entropy] = i
		root  = node_contest[max(node_contest)]
		child = {i[root] for i in data}

		return { header[root] : { i : ID3(
					    			header[:root]+header[root+1:],
			                        partition_data(data,root,i)
			                        ) for i in child } }
#--------------------------------------------------------------------
def getQuery(tree) :
	tree = tree[tree.keys()[0]]
	while True :
		if type(tree)==dict :
			print 'Key-Options : ',tree.keys()
			key = raw_input('Check For : ')
			tree = tree[key]
		else :
			print(tree)
			break
#----------------------------------------------------------------------------------		
with open('data.csv') as fobj :
	data   = [line.strip().split(',') for line in fobj]
	header = data[0]
	data   = data[1:]
	tree = ID3(header,data)
	print json.dumps(tree,indent=4)
	getQuery(tree)
