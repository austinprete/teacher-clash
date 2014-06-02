import models
import random
import rating


def fetch_teachers(num_teachers):
	rand1 = random.randint(0, (num_teachers-1))
	q = models.Teacher.all()
	q.filter("number =", rand1)
	results = q.fetch(1)
	result = None
	teacher1 = None
	for result in results:
		teacher1 = result
	teacher2 = fetch_teachertwo(rand1, (num_teachers-1))
	return (teacher1, teacher2)

def fetch_teachertwo(rand1, num_teachers):
	rand2 = random.randint(0, num_teachers)
	if rand1 != rand2:
		q = models.Teacher.all()
		q.filter("number =", rand2)
		results = q.fetch(1)
		result = None
		teacher2 = None
		for result in results:
			teacher2 = result
		return teacher2
	else: 
		teachertwo(rand1, num_teachers)

def adjust_ratings(teacher1, teacher2, winner): 
	if winner == teacher1:
		winner1 = True
	else:
		winner1 = False
	expect1, expect2 = rating.expect(teacher1.rating, teacher2.rating)
	result1, result2 = rating.result(winner1)
	teacher1.rating, teacher2.rating = map(int, (rating.adjust(teacher1, teacher2, result1, result2, expect1, expect2)))
	teacher1.put()
	teacher2.put()

