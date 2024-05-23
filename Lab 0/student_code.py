def order(data, stats):
	""" Takes in an array 'data' and returns it in sorted order.
	Takes in a 'stats' array and returns the data's [mean, median, mode]"""

	# sorting data

	# compare first element
	for i in range(len(data)):
		# with its consecutive element
		for j in range(len(data) - i - 1):
			# if out of order then swap
			if data[j] > data[j+1]:
				temp_j = data[j]
				data[j] = data[j+1]
				data[j+1]= temp_j

	# stats array
	sum = 0
	mean = 0
	median = 0
	mode = 0

	# mean and mode
	winner = None
	winnerCount = 0
	curr = None
	currCount = 0
	for i in range(len(data)):
		sum += data[i]

		if winner == None:
			curr = data[i]
			winner = curr

		if data[i] == winner:
			winnerCount += 1

		if data[i] == curr:
			currCount += 1
		else:
			if currCount > winnerCount:
				winner = data[i-1]
				winnerCount = currCount
			curr = data[i]
			currCount = 1

	if currCount > winnerCount:
		winnerCount = currCount
		winner = curr

	mean = sum//len(data)
	mode = winner

	# median
	# if array is odd
	if(len(data) % 2 == 1):
		# check if only value
		if (len(data) == 1):
			median = data[0]
		else:
			median = data[int((len(data) - 1)/2)]
	# if its even
	else:
		median = data[int((len(data)/2) - 1)]

	stats[0] = mean
	stats[1] = median
	stats[2] = mode