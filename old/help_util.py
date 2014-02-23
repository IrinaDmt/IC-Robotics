# actual median function only available in python 3.3+
#this version is 2.7.3
def median(list):
	odd = len(list) % 2
	ordered = sorted(list)
	length = len(list)
	if odd:
		return ordered[length / 2]
	else:
		a = ordered[(length + 1) / 2]
		b = ordered[(length - 1) / 2]
		return (a + b) / 2
