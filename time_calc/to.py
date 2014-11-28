
max_num_setups = 14 # total number of setups

K = 1.2 #effiency value

match_time = 10 # time it takes per match

total_entrants = [40, 60, 80]


def exp_time(num_people_per_pool):
	return ( match_time * K * (num_people_per_pool) * (num_people_per_pool -1)) / (2 * setups_per_pool(num_people_per_pool))

def setups_per_pool(num_people_per_pool):
	return min(max_num_setups, (num_people_per_pool/ 2))

def concurrency_factor(setups_needed):
	return (max_num_setups // setups_needed)


def do_work(total_people):
	#print "with", total_people, "people"
	best_time = 1000000
	best_num = 0
	for num_pools in range(2,14):
		#print "FOR ", num_pools, "pools"
		num_people_per_pool = total_people / num_pools
		cf = concurrency_factor(setups_per_pool(num_people_per_pool))
		et = exp_time(num_people_per_pool)
		total_time = (et * num_pools) / cf
		print "for", num_people_per_pool, " people per pool with ", num_pools , " pools, it will take ",  ( float(total_time) / 60)
		#print "total_people: ", total_people
		#print "num people per pool", num_people_per_pool
		#print "setups needed:", setups_per_pool(num_people_per_pool)
		#print "concurrency_factor", cf
		#print "expected time for one pool",  et
		#print num_pools, " pools will take:",  total_time
		#print "\n\n"
		if total_time < best_time:
			best_time = total_time
			best_num = num_pools
	print "with", total_people, "people, best number of pools is:", best_num



if __name__ == "__main__":
	for x in total_entrants:
		do_work(x)