#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Get the differences/agreements between lists. This version deals with two lists/sets. """

__author__  = "Ray Stefancsik"
__version__ = "0.1"

### provide two lists to compute agreements or differences
my_list1 = [ "(likely gluten-specific) T FH CD4 T cells	CellType", "absorptive and secretory lineages	CellType", "absorptive lineages	CellType", "actively cycling ECs	CellType", "age-related B cells	CellType", "antigen-presenting cells	CellType", "APCs	CellType", "arterial	CellType", "B cell	CellType", "B cell lineages	CellType", "B cells	CellType", "BEST4 enterocytes	CellType", "branch 1 cells	CellType", "branch 2	CellType", "Brunner’s gland cells	CellType", "capillary	CellType", "CCL4	CellType", "CCL4 CD69 ITGAE population	CellType", "CCL4 cells	CellType", "CCL4 effector	CellType", "CCL4 effectors	CellType", "CCL4 populations	CellType", "CCR7 T FH -like subset	CellType", "CCR7 T FH CD4 T cells	CellType" ]
        
my_list2 = [ "ACD, CD8 T RM (2) cell	CellType", "age-related B cells	CellType", "B cell	CellType", "B cells	CellType", "BEST4 enterocytes	CellType", "Brunner’s gland cells	CellType", "CCL4 , IKZF2 T RM (2) and natural IEL populations	CellType", "CCL4 CD69 ITGAE	CellType", "CCL4 cells	CellType", "CCL4 effector and IKZF2 T RM (2) population	CellType", "CCR7 T FH -like	CellType", "CCR7 T FH CD4 T cells	CellType" ]

my_set1 = set(my_list1)
my_set2 = set(my_list2)

# find and print element found only in set 1
only_in_1 = list(my_set1 - my_set2) 

print("\n\tonly in 1st:")
for i in only_in_1:
    print(i)

# find and print element found only in set 2
only_in_2 = list(my_set2 - my_set1) 

print("\n\tonly in 2nd:")
for i in only_in_2:
    print(i)

# find and print common elements in two lists (intersection of two sets)
#### find common elements in three lists: common_elements = my_set1.intersection(my_set2, my_set3)

common_elements = my_set1.intersection(my_set2)
print("\n\tcommon elements:")
for i in list(common_elements):
    print(i)

