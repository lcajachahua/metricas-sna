raw_text <- paste(readLines("C:/TDAPPS/R/Corrector/crea.txt"), collapse = " ")
split_text <- strsplit(raw_text, "[^abcdefghijklmnñopqrstuvwxyzáéíóúäëïöüçàèìòùâêîôû']+")
sorted_words  <- as.table(as.matrix(data.frame(split_text))) 

correct <- function(word) {
  edit_dist <- adist(word, sorted_words)
  min_edit_dist <- min(edit_dist, 2)
  proposals_by_prob <- c(sorted_words[ edit_dist <= min(edit_dist, 2)])
  proposals_by_prob <- c(proposals_by_prob, word)
  proposals_by_prob[1]
}

correct("correrctor")

correct("ortogrfaico")

correct("wn")

correct("foncionamento")

# Distancia 2 ediciones
correct("edictioness") 


lista<-c("rojiso","ariba","pelosa")

sapply(head(lista),correct)

lapply(head(lista),correct)





