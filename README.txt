The codes help analyze corpus from the CHILDES database of child oriented speech (recorded in naturalistic environment). These scripts are for Spanish recordings and are focused on pairs formed by two consecutive words. The analysis is on the single and paired endings and wether or not there's an agreement between the paired endings. 
It was coded on Spyder 4.2.5 with Python 3.8.8


*** WARNING

A few files from OreaPine and FernAguado corpus had to be manually edited for the code to run on them. 
This happens because of the way the cleaning_file function is built : the segmentation of the elements is based on the spaces between them and typically for the participants, sometimes a space is missing when it goes to the next line. In those cases, it is possible to manually add that space and it should work after that.

***

SpAgr_final gives result on a file level whereas SpAgr_v2 aggregates the results to give them on a child level. The columns of the output files are the same in both cases but the results from SpAgr_final can be too much to process if you run a statistical analysis on them, in which case you might want to use the aggregated results of SpAgr_v2.


SpAgr_final :

Creates one file per child with the results for each file.
Each line is for a pair type and has the following columns :
> language (=spanish)
> corpus name
> child's name
> file number 
> number of possible endings in the file
> number of possible paired endings in the file 
> the pair of words
> the ending of the first word of the pair
> the ending of the second word of the pair
> if there's an identity (1) or not (0)
> the count of this paired ending in the file
> the count of the first ending in the file
> the count of the second ending in the file
> the paired ending frequency in the file
> the first ending frequency in the file 
> the second ending frequency in the file

At the end of SpAgr_final, there are a few lines of code to change the format of the files from CHILDES : .cha files are converted to .txt files.


SpAgr_v2 : 

Same as SpAgr_final but aggregates the pair types on the child level, e.g. takes the pairs of all the files of one child into account when sorting them to find the types. 