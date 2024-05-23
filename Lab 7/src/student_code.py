import common
import math #note, for this lab only, your are allowed to import math

BIN_SIZE_LINE = 2000
BIN_SIZE_CIRCLE = 200

def detect_slope_intercept(image: list) -> common.Line:
	"""Given an 2-dimensional array of pixels (0 or 255), return a Line structure with m slope and b y-intercept"""
	
	# we know -10 ≤ m < 10 and -1000 ≤ b < 1000
	houghSpace = common.init_space(BIN_SIZE_LINE, BIN_SIZE_LINE)
	# initialize line
	line = common.Line()

	# loop through every pixel in the image
	for y in range(common.constants.HEIGHT):
		for x in range(common.constants.WIDTH):

			# if pixel is white, skip
			if image[y][x]:
				continue
			# otherwise, continue

			# for -10 ≤ m < 10 with a step of 0.01 = 2,000 unique m's
			for m_iterator in range(BIN_SIZE_LINE):
				# real m
				m = (m_iterator - 1000) / 100
				# real b ∈ [-1000, 1000)
				b = round(-m*x + y)
				# b_iterator ∈ [0, 2000)
				b_iterator = b + 1000
				# only graph lines that are within the bounds of our array, period
				if 0 <= b_iterator < BIN_SIZE_LINE and 0 <= m_iterator < BIN_SIZE_LINE:
					houghSpace[b_iterator][m_iterator] += 1
	
	# look for max bin in hough space
	maxVotes, maxVotes_b, maxVotes_m = None, None, None
	for b_iterator in range(BIN_SIZE_LINE):
		for m_iterator in range(BIN_SIZE_LINE):
			votes = houghSpace[b_iterator][m_iterator]
			if maxVotes == None:
				maxVotes = votes
				continue
			if votes > maxVotes:
				maxVotes = votes
				maxVotes_b = b_iterator - 1000
				maxVotes_m = (m_iterator - 1000) / 100

	# update line
	line.b, line.m = maxVotes_b, maxVotes_m

	return line

def detect_circles(image: list) -> int:
	"""Given an 2-dimensional array of pixels (0 or 255), return the amount of circles within the image"""

	# we know 0 ≤ a < 200 and 0 ≤ b < 200
	houghSpace = common.init_space(BIN_SIZE_CIRCLE, BIN_SIZE_CIRCLE)
	# define radius
	r = 30
	# initialize circle count
	circleCount = 0

	# loop through every pixel in the image
	for y in range(common.constants.HEIGHT):
		for x in range(common.constants.WIDTH):

			# if pixel is white, skip
			if image[y][x]:
				continue
			# otherwise, continue

			# for 0 ≤ a < 200 with a step of 1 = 200 unique a's
			for a in range(BIN_SIZE_CIRCLE):

				# don't care if it's out of the domain
				# if r² < (xᵢ-a)², skip
				if abs(a-x) > r:
					continue

				# (xᵢ-a)² + (yᵢ-b)² = r²
				# b = y ± √(r² - (xᵢ-a)²)
				sqrt = math.sqrt(r**2 - (a-x)**2)
				# round to nearest int
				b_upper = round(y + sqrt)
				b_lower = round(y - sqrt)

				# if upper semi-circle is within the range of the array, plot it
				if 0 <= b_lower < BIN_SIZE_CIRCLE:
					houghSpace[b_lower][a] += 1
				# if lower semi-circle is within the range of the array and
				# isn't the same point as the upper semi-circle, plot it
				if 0 <= b_upper < BIN_SIZE_CIRCLE and b_upper != b_lower:
					houghSpace[b_upper][a] += 1

	# look for max bin in hough space
	maxVotes = None
	for b in range(BIN_SIZE_CIRCLE):
		for a in range(BIN_SIZE_CIRCLE):
			votes = houghSpace[b][a]
			if maxVotes == None:
				maxVotes = votes
				continue
			if votes >= maxVotes:
				maxVotes = votes
	
	# look for how many bins match the threshold
	for b in range(BIN_SIZE_CIRCLE):
		for a in range(BIN_SIZE_CIRCLE):
			votes = houghSpace[b][a]
			if 68 <= votes <= maxVotes:
				circleCount += 1

	return circleCount