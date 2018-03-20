from numpy.random import choice
from collections import Counter


def sample_no_replacement(full_set, previous_set=None):
	print "starting sample_no_replacement"
	if previous_set:
		print "prev set"
		print previous_set
	print full_set

	if set(previous_set) == set(full_set):
		#the user has seen each of the conditions of this vairbales at least once
		cond_counts = Counter(previous_set)
		#return a list of tuples of most common e.g.
		#[('a', 5), ('r', 2), ('b', 2)]
		cond_common_order = cond_counts.most_common()
		print "cond_common_order"
		print cond_common_order
		if cond_common_order[0][1] == cond_common_order[-1][1]:
			#all conds are evenly assigned, choose randomly
			cond = cond_common_order[choice(len(cond_common_order))]
			print cond
			cond = cond[0]
		else:
			#choose the one with least assignment 
			#(where same value is ordered arbitrarily)
			cond = cond_common_order[-1][0]
	else:
		#subject hasn't seen all versions yet
		cond_choices = set(full_set) - set(previous_set)
		print "cond_choices"
		print cond_choices
		cond = choice(list(cond_choices))

	return cond
