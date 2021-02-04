from collections import defaultdict 

def get_friendly_dict(friend_list):
    ''' calculates the degree-one friends of each individual from 
    a list of friendship links in a social network.'''
    
    # add the degree-one friends of each person to a set in a dictionary
    friendly_dict = defaultdict(set)
    for pair in friend_list:
        for i in range(2):
            friendly_dict[pair[i]].add(pair[(i+1) % 2])     
    
    return friendly_dict

def friend_besties(individual, bestie_dict):
    '''returns a list of an individual's degree-one friends'''
    if individual in bestie_dict.keys():
        return sorted(list(bestie_dict[individual]))
    return []

def friend_second_besties(individual, bestie_dict):
    '''returns a list of the degree-two friends of an individual'''
    if individual not in bestie_dict.keys():
        return []
    
    # know who the individual is best friends with
    besties = bestie_dict[individual]
    
    # makes a set of the friends of the individual's best friends
    friends_friends = set()
    for friends in besties: 
        for x in bestie_dict[friends]:
            friends_friends.add(x)
        
    return sorted(list(friends_friends - besties - {individual}))

def besties_coverage(individuals, bestie_dict, relationship_list):
    '''Determines the proportion of connected individuals to the total size of 
    the network.'''
    
    # total number of individuals 
    network_size = len(bestie_dict.keys())
    
    # find the set of people connected and its size 
    connected_people = set()
    for individual in individuals:
        connected_people.add(individual)
        for function in relationship_list:
            for friend in function(individual, bestie_dict):
                connected_people.add(friend)
    connected_size = len(connected_people)
    
    # network coverage
    return connected_size / network_size

def friendly_prediction(unknown_user, features, bestie_dict, feat_dict):
    '''Makes predictions about the features of an unknown user based of the 
    features of their friends.'''
    
    # know the friend circles of the unknown user
    besties = friend_besties(unknown_user, bestie_dict)
    second_besties = friend_second_besties(unknown_user, bestie_dict)
    
def count_attributes(friend_list):
        '''inner function to count the attributes within a social circle
        for a particular feature.'''
        feature_count = defaultdict(int)
        for friend in friend_list:
            if friend in feat_dict.keys():
                if feature in feat_dict[friend].keys():
                    feature_count[feat_dict[friend][feature]] += 1
        return feature_count
    
    # create a dictionary of the most common attribute(s) in the social circle 
    # for each feature
    pred_dict = defaultdict(dict)
    
    for feature in features:
        mode_list = [] 
        
        # count the attributes among the besties (and second besties if needed)
        feature_count = count_attributes(besties)
        if not feature_count:
            feature_count = count_attributes(second_besties)
        
        # finds the mode attribute(s) for a given feature
        if feature_count:
            mode_attribute_freq = max(feature_count.values())
        for (x, y) in feature_count.items():
            if y == mode_attribute_freq:
                mode_list.append(x)
  
        pred_dict[feature] = sorted(mode_list)
    
    return pred_dict 
