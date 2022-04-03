## Cargamos las librerías
library(twitteR)
library(tidyverse)
library(rvest)

## Acceso a la app (Más detalles en: https://rpubs.com/Kyleen1991/594933)
consumerKey = "2wxeZDNZ8BvsJtrhiDkCvnbm2"
consumerSecret = "kgx56tL9laUXNvk5hBl3y2jJFfxacqrcMIkE6k0CjZdd9bhHvx"
accessToken = "57792955-6pD4IdZoMrq2RbmfPgZem83riwTM9CC6PjitpFPr1"
accessSecret = "IMDHnlITbGC2El7WzGMZJuh5Q64by9lpXNQAdVJJgAso5"
options(httr_oauth_cache=TRUE)
setup_twitter_oauth(consumer_key = consumerKey, consumer_secret = consumerSecret,
                    access_token = accessToken, access_secret = accessSecret)


## Interbank:
ibkpetweets<-userTimeline('interbank',n=3200)
## BBVA en Perú:
bbvapetweets<-userTimeline('bbva_peru',n=3200)
## Scotiabank Perú:
scbpetweets<-userTimeline('ScotiabankPE',n=3200)
## Banco de Crédito BCP:
bcppetweets<-userTimeline('BCPComunica',n=3200)

## Creamos los df

ibkpetweets_df<-twListToDF(ibkpetweets)
bbvapetweets_df<-twListToDF(bbvapetweets)
scbpetweets_df<-twListToDF(scbpetweets)
bcppetweets_df<-twListToDF(bcppetweets)

## Se unen todos los tweets en un único dataframe
tweets <- bind_rows(ibkpetweets_df,bbvapetweets_df,scbpetweets_df,bcppetweets_df)

## Elimina los saltos de línea internos de cada tweet
tweets$text <- str_replace_all(tweets$text, "[\r\n]" , " ")

## Exportamos los tweets extraídos
write.csv(tweets,file = "Tweets_Bancos.csv")

