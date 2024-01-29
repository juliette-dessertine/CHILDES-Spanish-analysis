#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 03:09:54 2024

@author: juliettedessertine
"""





'cleaning_file takes a file and returns all the utterances of non-child participants of the file.'
'More specifically, each "line" of non-child participants generates a list contaning the words'
'of that utterance. All those lists compose the elements of the clean_words list.'

def cleaning_file (file) :
    
    a = 'start'
    list_data = [] #all the lines of the file
    cut_data = [] #lines of adults only
    raw_data = open(file, 'r')
    while a != '' :
        a = raw_data.readline()
        list_data.append(a)
     
    

    #here starts a trick to avoid problems when some file don't have the @Options line in the headers lines 
    count_case = 0
    replace = []
    for k in list_data :
        if '@Options' in k :
            count_case += 1
        elif '@ID' in k :
            replace.append(list_data.index(k))
            
        
    if count_case == 0 :
        list_data[min(replace)] = '@Options'   
    #end of the trick
    
    
    a = list_data[4]
    i = 5
    while '@Options' not in list_data[i] : #to find the line containing the participants 
        a += list_data[i]
        i += 1
    
    raw_participants = a #line with the participants 
    segment_participants = []
    for k in range(len(raw_participants)):
        if raw_participants[k] == ',' :
            segment_participants.append(k+1)
    segment_participants.append(len(raw_participants)) #index of where to cut the line to get the participants
    
    cut_participants = []
    lim = 0
    for cut in segment_participants :
        cut_participants.append(raw_participants[lim:cut]) #list of all participants
        lim = cut
    
    adults_only = [] #list of aonly adult participants
    for elmnt in cut_participants : 
        if len(elmnt) > 1 and 'Target_Child' not in elmnt and '@Languages' not in elmnt: 
            adults_only.append(elmnt)
    
    
    space_index = [[] for k in range(len(adults_only))]
    for i in range(len(adults_only)) :
        for k in range(len(adults_only[i])) : 
            if adults_only[i][k] == ' ' : 
                space_index[i].append(k) #index of where to cut to only get the tag of the adult
    
    name_tags = [] #tags of all the adults
    for i in range(len(space_index)) :
        name_tags.append('*'+ adults_only[i][space_index[i][0]+1:space_index[i][1]]) #+1 to avoid the space before the tag
                
            
    for line in list_data : 
        for tag in name_tags : 
            if tag in line : 
                cut_data.append(line) #taking only the lines said by non child

    
    segment_data = [[] for k in range(len(cut_data))] #for each line, the index of where to cut to isolate the words
    for k in range(len(cut_data)):
        for i in range(len(cut_data[k])) :
            if cut_data[k][i] == ':' :
                segment_data[k].append(i+1)
            elif cut_data[k][i] == ' ' :
                segment_data[k].append(i) 
                
    
    words_only = [[] for k in range(len(cut_data))] #for each line, list of the words/elements in it
    for i in range(len(segment_data)) :
        lim = segment_data[i][0]
        for j in range(len(segment_data[i])) :
            line = cut_data[i]
            words_only[i].append(line[lim+1:segment_data[i][j]])
            lim = segment_data[i][j]
    
    
    clean_words = [[] for k in range(len(cut_data))] #cleaning the elements of the line by getting rid of symbols
    for i in range (len(words_only)) :
        for k in words_only[i] :
            if k != '' and '[' not in k and ']' not in k and '(' not in k and '.' not in k and '?' not in k and '>' not in k and '<' not in k and '!' not in k : 
                if '@' in k :
                    clean_words[i].append(k[:k.index('@')])
                else :
                    clean_words[i].append(k)
                
                
    return clean_words 


    
'paired_endings takes the isolated words and pairs for each line all two consecutive words if the two'
'words are different and both are more than one letter long. After that it selects the types of pairs so'
'each pair is unique'

def paired_endings (clean_words) :
    
    pairs = []
    for k in range(len(clean_words)) :
        for i in range(len(clean_words[k])-1) :
            if len(clean_words[k][i]) > 1 and len(clean_words[k][i+1]) > 1 and clean_words[k][i] != clean_words[k][i+1] : 
                potential_pair = [clean_words[k][i],clean_words[k][i+1]]
                if potential_pair not in pairs : 
                    pairs.append(potential_pair) #unique pairs of two consecutive different words
    
    return pairs 




'get_ending takes a word and returns its "phonetical" ending, meaning it could be a single letter'
'or several ones if the words ends in a diphtongue or consonant. if word ends in a vowel, function looks' 
'if the vowel is part of a diphtongue to include it in the ending. if word ends in consonant, function'
'gets to the closest vowel and then looks if it is part of a diphtongue following same procedure as'
'when the word ends with vowel. the argument size_lim is mainly a debugging which imposes a word size'
'limit set to 2.'

def get_ending (word, size_lim) : 

        
    ending = word[len(word)-1] #taking last letter
        
    dip_a = ['i','u']
    dip_e = ['i','u']
    dip_i = ['a','e','o','u']
    dip2_i = ['ué','ié','io','ua','iá']
    dip_o = ['i','u']
    dip_u = ['i','a','e']
    dip2_u = ['ua']
    dip_é = ['i']
    dip_y = ['a','e','o','u']
    dip2_y = ['ue','ua']
        
        
    vowels = ['a','e','i','o','u','á','é','í','ó','ú','y']
        
    if ending in vowels : #if word ends with vowel
            
        if ending == 'a' : 
            for letter in dip_a : #looks for a diphtongue before the vowel
                if len(word) >= size_lim and word[len(word)-2] == letter : #size_lim avoids looking for unexistent letter which would stop the function from running
                    ending = letter + ending #adds previous letters of the diphtongue to the ending
        
        elif ending == 'e' :
            for letter in dip_e :
                if len(word) >= size_lim and word[len(word)-2] == letter :
                    if len(word) >= size_lim+1 and word[len(word)-3]+word[len(word)-2] == 'qu' :
                        ending = 'e'
                    elif len(word) >= size_lim+1 and word[len(word)-3]+word[len(word)-2] == 'gu' :
                        ending = 'e'
                    else :
                        ending = letter + ending 
                        
        elif ending == 'i' :
            for letter in dip_i :
                if len(word) >= size_lim and word[len(word)-2] == letter :
                    if len(word) >= size_lim+1 and word[len(word)-3]+word[len(word)-2] == 'gu' :
                        ending = 'i'
                    else :
                        ending = letter + ending 
            for letters in dip2_i :
                if len(word) >= size_lim+1 and word[len(word)-3]+word[len(word)-2] == letters :
                    ending = letters + 'i'
                        
        elif ending == 'o' :
            for letter in dip_o :
                if len(word) >= size_lim and word[len(word)-2] == letter :
                    ending = letter + ending
                        
        elif ending == 'u' :
            for letter in dip_u :
                if len(word) >= size_lim and word[len(word)-2] == letter :
                    ending += letter
            for letters in dip2_u :
                if len(word) >= 3 and word[len(word)-3]+word[len(word)-2] == letters :
                    ending = letters + 'u'
                     
        elif ending == 'é' :
            for letter in dip_é :
                if len(word) >= size_lim and word[len(word)-2] == letter :
                    if len(word) >= size_lim+1 and word[len(word)-3]+word[len(word)-2] == 'gu' :
                        ending = 'é'
                    else :
                        ending = letter + ending 
        
        elif ending == 'y' :
            for letter in dip_y :
                if len(word) >= size_lim and word[len(word)-2] == letter :
                    ending = letter + ending
            for letters in dip2_y :
                if len(word) >= 3 and word[len(word)-3]+word[len(word)-2] == letters :
                    ending = letters +'y'
                    
            
    else : #if word ends with consonant

        index = len(word)-2 #index of letter just before last consonant of the word, e.g. last letter 
        previous_letter = word[index]
        while previous_letter not in vowels and index >= 0 : #going through the letters backwards until it finds a vowel while staying "inside" the word 
            index = index - 1
            previous_letter = word[index]
            
        last_part = word[index+1:] #keeping in store the final consonants 
        word = word[:index+1] #taking the other part of the word as a new one to work the same way (with potential diphtongues) as if the word ended with a vowel
        
        if len(word) > 1 : #selecting the vowel ending to search for diphtongues
            ending = word[len(word)-1]
        else :
            ending = word

        #searching for diphtongues
        if ending == 'a' :
            for letter in dip_a :
                if len(word) >= size_lim and word[len(word)-2] == letter :
                    ending = letter + ending
            
        elif ending == 'e' :
            for letter in dip_e :
                if len(word) >= size_lim and word[len(word)-2] == letter :
                    if len(word) >= size_lim+1 and word[len(word)-3]+word[len(word)-2] == 'qu' :
                        ending = 'e'
                    elif len(word) >= size_lim+1 and word[len(word)-3]+word[len(word)-2] == 'gu' :
                        ending = 'e'
                    else :
                        ending = letter + ending 
                            
        elif ending == 'i' :
            for letter in dip_i :
                if len(word) >= size_lim and word[len(word)-2] == letter :
                    if len(word) >= size_lim+1 and word[len(word)-3]+word[len(word)-2] == 'gu' :
                        ending = 'i'
                    else :
                        ending = letter + ending 
            for letters in dip2_i :
                if len(word) >= size_lim+1 and word[len(word)-3]+word[len(word)-2] == letters :
                    ending = letters + 'i' 
                            
        elif ending == 'o' :
            for letter in dip_o :
                if len(word) >= size_lim and word[len(word)-2] == letter :
                    ending = letter + ending
                            
        elif ending == 'u' :
            for letter in dip_u :
                if len(word) >= size_lim and word[len(word)-2] == letter :
                    ending = letter + ending
            for letters in dip2_u :
                if len(word) >= 3 and word[len(word)-3]+word[len(word)-2] == letters :
                    ending = letters + 'u' 
                         
        elif ending == 'é' :
            for letter in dip_é :
                if len(word) >= size_lim and word[len(word)-2] == letter :
                    if len(word) >= size_lim+1 and word[len(word)-3]+word[len(word)-2] == 'gu' :
                        ending = 'é'
                    else :
                        ending = letter + ending 
                        
        elif ending == 'y' :
            for letter in dip_y :
                if len(word) >= size_lim and word[len(word)-2] == letter :
                    ending += letter
            for letters in dip2_y :
                if len(word) >= 3 and word[len(word)-3]+word[len(word)-2] == letters :
                    ending = letters + 'y'
                        
        if last_part != 'h' : #excluding the 'h' as it is silent 
            ending += last_part #adding the ending found with the vowel-diphtongue procedure to the final consonants
    
    
 
    return ending 

            

      
'get_ending_pair_count takes all the types of pair of a file, each pair being two consecutive words, and'
'returns the total number of types of paired endings (how many different pairs of endings exist),'
'the list of those types of paired endings, and the list of the counts of each of those types of'
'paired endings'

def get_ending_pair_count (pairs) :  

    ending_pair = [] #types of paired endings
    ending_pair_count = [] #counts of each type of paired endings
    all_ending_pairs = [] #paired endings of each type of word pair
    ending_pair_types = pairs #types of pairs (= word pairs)
   
        
    for pair in ending_pair_types :
        all_ending_pairs.append([get_ending(pair[0],2),get_ending(pair[1],2)]) #getting the ending of each word of the pair, with size_lim = 2

    for end_pair in all_ending_pairs :
        potential_ending_pair = end_pair 
        if potential_ending_pair not in ending_pair : #excluding potential repetition of paired endings coming from different word pairs having the same endings
            ending_pair.append(potential_ending_pair)
        
    
    count = 0
    for k in ending_pair :
        for j in all_ending_pairs :
            if k == j :
                count+= 1
        ending_pair_count.append(count) #list of the count for each type of paired ending
        count = 0
    
    
    return len(all_ending_pairs), ending_pair, ending_pair_count



'get_ending_indiv_count is basically the same as get_ending_pair_count but for individual endings.'
'It takes all the types of pairs of a file and returns the number of endings from the types of words' 
'(= number of types of words), the types of endings (regardless of their word of origin, meaning if two' 
'different words have the same ending, this ending will only appear once), and the list of the counts'
'of each of those types of ending.'

def get_ending_indiv_count (pairs) :
    
    ending_inv = [] #types of ending
    all_endings = [] #endings of all the types of word
    ending_counts = [] #counts of each type of ending
    word_types = [] #types of word
    
    for i in range(len(pairs)) : 
        pair = pairs[i]
        word_1 = pair[0]
        word_2 = pair[1]
        
        potential_word = word_1 
        if potential_word not in word_types :
            word_types.append(potential_word)
        
        potential_word = word_2 
        if potential_word not in word_types :
            word_types.append(potential_word)
        
    for word in word_types :
        all_endings.append(get_ending(word,2))
    
    for ending in all_endings :
        potential_ending = ending 
        if potential_ending not in ending_inv :
            ending_inv.append(potential_ending)

    count = 0
    for k in ending_inv :
        for j in all_endings :
            if k == j :
                count += 1
        ending_counts.append(count) #list of the count for each type of individual ending
        count = 0
    
    ending_inv_size = len(all_endings)
    
    return ending_inv_size, ending_inv, ending_counts 



'get_data takes the results from get_ending_indiv_count and get_ending_pair_count to calculate'
'the frequencies and the other informations that will be added to the csv file. The frequency'
'of an ending equates to the count of this ending in the file (how many times it appears in all'
'the types of word of the file) divided by the total number of endings from different words. The'
'frequency of a paired ending equates to the count of this paired ending in the file divided by'
'the total number of paired endings.'

def get_data (name, pairs, name_file) :
    
    data = []
    
    ending_inv_size = get_ending_indiv_count(pairs)[0]
    ending_inv = get_ending_indiv_count(pairs)[1]
    ending_counts = get_ending_indiv_count(pairs)[2]
    
    ending_pair_size = get_ending_pair_count(pairs)[0]
    ending_pair = get_ending_pair_count(pairs)[1]

    
    ending_pair_count = get_ending_pair_count(pairs)[2]
    
    
    
    for i in range(len(pairs)):
        language = "spanish" #other info for the csv file, to be changed manually 
        corpus = "OreaPine" #name of the corpus, to be changed manually 
        file = name_file
        
        pair = pairs[i]
        word_1 = pair[0]
        word_2 = pair[1]
        size_lim = 2
        ending_1 = get_ending(word_1, size_lim)
        ending_2 = get_ending(word_2, size_lim)

            
        index = ending_pair.index([ending_1,ending_2])
        this_ending_pair_count = ending_pair_count[index]
        
        identity = 0
        if ending_1 == ending_2 :
            identity = 1
            
        
        index_end_1 = ending_inv.index(ending_1)
        index_end_2 = ending_inv.index(ending_2)
        ending_1_count = ending_counts[index_end_1]
        ending_2_count = ending_counts[index_end_2]
        
        ending_pair_freq = this_ending_pair_count/ending_pair_size
        ending_1_freq = ending_1_count/ending_inv_size
        ending_2_freq = ending_2_count/ending_inv_size
            
        data.append([language, corpus, name, file, len(ending_inv), len(ending_pair), pair, ending_1, ending_2, identity, this_ending_pair_count, ending_1_count, ending_2_count, ending_pair_freq, ending_1_freq, ending_2_freq ])
        
    return data 




'writing_file essentially writes the data for each pair of words into the csv file'

def writing_file (name, pairs, name_file) : 
    
    import csv

    data = get_data(name, pairs, name_file) #get all necessary data for the pairs of the file
    with open(name+"_file.csv", "a") as f:
        writer = csv.writer(f, delimiter=";", lineterminator="\n")
        writer.writerows(data)
    f.close()



'complete concentrates all the steps to produce the csv file with the results of each file of the corpus'    
    
def complete (name, file, name_file) :
    
    cleaned = cleaning_file(file) #first get the cleaned words from the files
    pairs = paired_endings(cleaned) #then get the pairs (in types)
    writing_file(name, pairs, name_file) #and finally get the data and write it in the csv file



'create_files goes through the corpus to get all the files from all the children and actually creates the'
'csv files with the header'
    
def create_files () : 
    
    import os 
    os.chdir("/Users/juliettedessertine/Desktop/UCLA_LAlab/spanish/Spanish_OreaPine") #directory of the corpus (containing a file for each child, and in it all the child's files), to be changed manually 
    if '.DS_Store' in os.listdir() :
        os.remove('.DS_Store')
    individuals = os.listdir()

    for i in individuals :
        name = i 
        os.chdir(i)
        if '.DS_Store' in os.listdir() : #to get rid of a DS_Store file that's often here 
            os.remove('.DS_Store')
        records = os.listdir()
        
        import csv
        field = ["language", "corpus", "name", "file", "file nb possible endings", "file nb possible paired endings", "pair", "ending 1", "ending 2", "identity", "ending pair count file", "ending 1 count", "ending 2 count", "ending pair freq", "ending 1 freq", "ending 2 freq"]
        with open(name+"_file.csv", "a") as f:
            writer = csv.writer(f, delimiter=";", lineterminator="\n")
            writer.writerow(field)
        
        
        for k in records :
            name_file = k
            complete(name,k,name_file)

        os.chdir("..")


   
    



## help : changing .cha files in .txt files 

# import os
# os.chdir("/Users/juliettedessertine/Desktop/UCLA_LAlab/spanish/Spanish_OreaPine")
# if '.DS_Store' in os.listdir() :
#     os.remove('.DS_Store')
# individuals = os.listdir()

# for i in individuals :
#     name = i 
#     os.chdir(i)
#     if '.DS_Store' in os.listdir() : 
#         os.remove('.DS_Store')
#     records = os.listdir()
#     for k in records : 
#         os.rename(k, k[:len(k)-3]+'txt')
#     os.chdir("..")

##










