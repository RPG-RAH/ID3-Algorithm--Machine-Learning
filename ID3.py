#-----------------------------------------------------------------------------------------------------
#By NAME	:Rahul Gautham Putcha
#	USN		:	1PE15IS079
#	COLLEGE : PESIT-BSC
#-----------------------------------------------------------------------------------------------------
#Import Files
from math import log
#-----------------------------------------------------------------------------------------------------

#Function Definitions
#Function : Basic Count of attributes
def count(data_set,value,index) :
	count = 0
	for i in data_set :
		if i[index]==value :
			count+=1
	return count

#Function : Basic Entropy Calculation
def entropy(attrib_value_counts) :
	values = [float(i)/sum(attrib_value_counts) for i in attrib_value_counts]
	enp = [-i*log(i,2) if i!=0 else 0 for i in values]
	return sum(enp)

#Function : For Nodes CHILDREN set
def create_values_set(data_set,index) :
	return {i[index] for i in data_set}

#Function : Target Attribute's Class Attribute Count
def partial_count(data_set,attrib_value,attrib_index,class_attrib_value,class_index) :
	count = 0
	for i in data_set :
		if i[attrib_index] == attrib_value and i[class_index]==class_attrib_value:
			count+=1
	return count

#Function : Calculating the Entropy of the Attribute
def entropy_attribute(data_set,class_attrib_counts,childs,index) :
	table = {i:(partial_count(data_set,i,index,positive,-1),partial_count(data_set,i,index,negative,-1)) for i in childs}
	return sum([float(sum(table[key]))/sum(class_attrib_counts)*entropy(table[key]) for key in table])

#Function : Extract the Child Part of table
def partition_data(data_set,attr_index,child_value) :
		return [i[:attr_index]+i[attr_index+1:] for i in data_set if i[attr_index]==child_value]

#------------------------------------------------------------------------------------------------------

#ID3 Algorithm : Recursive	
def decide_next_node(header_data,data) :
	#1st Step : Compute Class Entropy
	if data:
		class_attribute_counts = [count(data,positive,-1),count(data,negative,-1)]
		if class_attribute_counts[0]== 0: return negative
		if class_attribute_counts[1]== 0: return positive
		class_entropy = entropy(class_attribute_counts)
		node_contest = {}
		for i in range(len(data[0])-1) :
			#2nd Step : Compute Attribute Entropies
			childs = create_values_set(data,i)
			attr_entropy = entropy_attribute(data,class_attribute_counts,childs,i)
			#3rd Step : Compute Gain
			node_contest.update({(class_entropy-attr_entropy) : (i,'',childs)})
		#4th Step : Computing the Max Information Gain
		next_node = node_contest[max(node_contest)]
		#Printing the Tree in JS-ON Format
		return {
					header_data[next_node[0]] : 	{ 
										i : decide_next_node( 
													header_data[:next_node[0]]+header_data[next_node[0]+1:],
													partition_data(data,next_node[0],i)
											) for i in next_node[2] 
									}
			   }
	return None

#-----------------------------------------------------------------------------------------------------
#Main Program
#File Reading
positive,negative = 'Yes','No'		#NOTE : Do Change the +ve and -ve attribute value depending on training data set
with open('test.csv') as fobj :
	training_data = [line.strip().split(',') for line in fobj]
	print('Your Training Data : ')
	for i in training_data :
		print(i)
header = training_data[0]
training_data   = training_data[1:]
#-----------------------------------------------------------------
#ID3 Execution
data = training_data
print('\n\nTree in json format:\n')
print(decide_next_node(header,data))
