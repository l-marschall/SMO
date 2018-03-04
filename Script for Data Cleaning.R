### Merging all sets
rm(list=ls())
#library(dplyr) I don't believe it's needed anymore
setwd("/home/Nickfis/Documents/Barcelona GSE/2 Trimester/Financial Econometrics/Problem Set 1/problemset-data/Stocks for SMO")
temp = list.files(pattern="*.csv") #list.files() looks through current wd. Pattern specifies I want all csv files.
for (i in 1:length(temp)) assign(temp[i], read.csv(temp[i]))#, row.names=1))
# rm elements that are not datasets.
rm(i)
rm(temp)
# needed to remove the elements to now call the function to get all the objects in the workspace
check <- mget(setdiff(ls(),"B"))

for (i in 1:length(check)){
  if (ncol(check[[i]])>2){
    check[[i]] <- as.data.frame(cbind(check[[i]][1], check[[i]][5]))
  }
}


# taking care of the column names
colnames_clean<-names(check)
colnames_clean<- substr(colnames_clean,1,nchar(colnames_clean)-4) # as the second column name for each dataframe

for (i in 1:length(check)){
  colnames(check[[i]])<-c("Timestamp", colnames_clean[i])
  print(colnames(check[[i]]))
}

# take the unique values of the previously created list to name the dataframes in the new list
df_names<-unique(colnames_clean)
names(check) <- df_names

#### now finally merge
finaldf<-Reduce(function(x, y) merge(x, y, all=TRUE), check)
indexna<-complete.cases(finaldf)
finaldf <- finaldf[indexna,]

tokeep <- seq(from=1, to=nrow(finaldf), by=5)
finaldf<-finaldf[tokeep,]

# write it to a csv file
write.csv(finaldf, 'finaldf.csv')
