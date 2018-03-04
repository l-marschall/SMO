rm(list = ls())
setwd('/home/laurits/Desktop/BGSE/Term 2/Stochastic Models and Optimization/Final Project/SMO')

library(ggplot2)
library(ggthemes)
library(reshape2)
library(dplyr)

htest = read.csv('htest.csv')
company_list = c('Amazon', 'Bank of New York', 'Barclays', 'Coca Cola', 'lowe‘s Companies',
                'Nike', 'Norfolk Southern Railway', 'State Street Corporation', 'Walmart')
colnames(htest) = c('index', 'Riskless asset', company_list)
wealth_test <- htest
wealth <- rowSums(wealth_test[c('Riskless asset', company_list)])

sp500_weekly <- read.csv('sp500weekly.csv')
sp500_weekly$returns <- 1 + (sp500_weekly$Close - lag(sp500_weekly$Close)) / sp500_weekly$Close
sp500_weekly <- sp500_weekly[(nrow(sp500_weekly)-156) : nrow(sp500_weekly),]
returns <- sp500_weekly$returns
dates <- as.Date(as.character(sp500_weekly$Date),'%Y-%m-%d')

wealth_sp500 <- rep(1000, length(returns))

for (i in (1 : (length(returns)-1))) {
  wealth_sp500[i+1] <- wealth_sp500[i] * returns[i]
}

diff <- wealth - wealth_sp500
sp500_comparison <- data.frame(dates, diff)
sp500_comparison <- sp500_comparison[1:(nrow(sp500_comparison)-1), ]
ggplot(sp500_comparison, aes(x = dates, diff)) + geom_line(color = 'navy', size = 1) +
  xlab('Difference') + ylab('Date') +
  ggtitle('Difference between portfolio value and S&P500') +
  geom_hline(yintercept = 0, linetype = 'dashed')
ggsave('plots/sp500_comparison_gamma0.9.pdf', width = 16, height = 9)


htest = melt(htest, id = 'index')
htest <- htest[!(htest$value == 0),]
ggplot(htest, aes(x = index, y = value, colour = variable)) + 
  geom_point(size = 5) + geom_line(size = 0.3) +
  ggtitle('Investments in different stocks over three years of the test set') +
  xlab('Period') + ylab('Investment in stocks in USD')
ggsave('plots/htest_gamma0.9.pdf', width = 16, height = 9)



finalwealth <- read.csv('finalwealthar.csv')
colnames(finalwealth) <- c('index', 'wealth')
ggplot(finalwealth, aes(x = index, y = wealth)) + 
  geom_line(color = 'navy', size = 0.5) + geom_smooth(color = 'red') +
  ggtitle('Final wealth of the training process') +
  xlab('Period') + ylab('Wealth in USD')
ggsave('plots/finalwealth_gamma0.9.pdf', width = 16, height = 9)


finaldf <- read.csv('finaldf.csv')


