import math

def expect(rating1, rating2):
	expect1 = 1/(1 + math.pow(10, (rating2-rating1)/400.0))
	expect2 = 1/(1 + math.pow(10, (rating1-rating2)/400.0))

	return [expect1, expect2]

def result(winner1):
	if (winner1 == True):
		result1 = 1 
		result2 = 0
	else:
		result1 = 0 
		result2 = 1

	return [result1, result2]

def adjust(teacher1, teacher2, result1, result2, expect1, expect2):
	adjust1 = teacher1.rating + 32*(result1 - expect1)
	adjust2 = teacher2.rating + 32*(result2 - expect2)

	return [adjust1, adjust2]

