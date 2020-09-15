def calculate_rating_string(rating_list):
	"""
	input - list of rating numbers
	output - string consisting of the evaluated rating score
	"""
	paren = []
	for i in rating_list:  

		# Calculating the difference between opening and closing braces for the digit 
		if (paren.count('(') - paren.count(')')) <= i: 

			# If the next digit is greater, then open the brackets 
			while (paren.count('(') - paren.count(')')) != i: 
				paren.append('(')          
			paren.append(i)      
			  
			# Similarly, find the difference between opening and closing braces 
		elif (paren.count('(') - paren.count(')')) > i: 

			# If the next digit is smaller, then close the brackets 
			while (paren.count('(') - paren.count(')')) != i: 
				paren.append(')') 
			paren.append(i)   

	# Finally, close the remaining brackets 
	while (paren.count('(') - paren.count(')')) != 0: 
		paren.append(')') 

	# Returning the string 
	return ''.join(map(str, paren)) 