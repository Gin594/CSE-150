from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem) 
        # initialize empty stack
        spots = []
        while True:
            # check confilict
            if self.propagate(domains) is not False:
                # check consistent assignment for all spot 
                if self.isconsistent(domains) is not False:
                    return domains
                else:
                    # copy domains in order to back track
                    orig_domains = copy.deepcopy(domains)
                    # make decision
                    spot, num = self.search(domains)
                    spots.append((spot, num, orig_domains))
            else:
                # if stack is empty then no solution
                if len(spots) == 0:
                    return None
                else:
                    # back track domains
                    domains = self.backtrack(spots, domains)
        
        # TODO: implement backtracking search. 

        # TODO: delete this block ->
        # Note that the display and test functions in the main file take domains as inputs. 
        #   So when returning the final solution, make sure to take your assignment function 
        #   and turn the value into a single element list and return them as a domain map. 
        # for spot in sd_spots:
        #     domains[spot] = [1]
        # return domains
        # <- TODO: delete this block

    # TODO: add any supporting function you need

    # help function to check whether is consistent assignment
    def isconsistent(self, domains):
        for spot in sd_spots:
            if len(domains[spot]) != 1:
                return False
        return True

    
    def propagate(self, domains):
        # for each spot in the board
        for spot in sd_spots:
            # if length of domains[spot] is 1, remove spot's num 
            # from its peers' domains
            if len(domains[spot]) == 1:
                for peer in sd_peers[spot]:
                    if domains[spot][0] in domains[peer]:
                        domains[peer].remove(domains[spot][0])
                    # if above cause any domain to be empty
                    # there is a confilict
                    if len(domains[peer]) == 0:
                        return False
        return True

    def search(self, domains):
        # initialize unassigned value list
        unassigned = []
        # initialize the smallest unassigned spot
        sp = sd_spots[0]
        value = 0
        # find unassigned spots
        for spot in sd_spots:
            if len(domains[spot]) > 1:
                unassigned.append(spot)
        min_value = len(unassigned)
        for u in unassigned:
            # check smallest domain
            if len(domains[u]) < min_value:
                min_value = len(domains[u])
                # update the smallest spot
                sp = u
        # pick arbitrary value in domains[spot]
        value = domains[sp][random.randint(0, len(domains[sp])-1)]
        # restrict the domain of spot to value
        for v in domains[sp]:
            if v != value:
                domains[sp].remove(v)
        return sp, domains[sp][0]


    def backtrack(self, spots, domains):
        spot, num, orig_domains = spots.pop()
        # replace domains with orig domains
        domains = orig_domains
        # remove num from the domain of spot
        domains[spot].remove(num)
        return domains




    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
