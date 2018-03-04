rm(list = ls())
setwd('/home/laurits/Desktop/BGSE/Term 2/Stochastic Models and Optimization/Final Project/SMO')

library(ggplot2)
library(ggthemes)
library(reshape2)
library(dplyr)

htest = read.csv('csv_files/htest-05gamma.csv')
company_list = c('Amazon', 'Bank of New York', 'Barclays', 'Coca Cola', 'lowe‘s Companies',
                'Nike', 'Norfolk Southern Railway', 'State Street Corporation', 'Walmart')
colnames(htest) = c('index', 'Riskless asset', company_list)
wealth_test <- htest
wealth <- rowSums(wealth_test[c('Riskless asset', company_list)])



sp500_weekly <- read.csv('csv_files/sp500weekly.csv')
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
  xlab('Date') + ylab('Difference') +
  ggtitle('Difference between portfolio value and S&P500') +
  geom_hline(yintercept = 0, linetype = 'dashed') +
  theme(axis.text = element_text(size = 20), axis.title = element_text(size = 20),
        plot.title = element_text(size = 24, hjust = 0.5),
        legend.position = 'right',
        legend.title = element_text(size = 22),
        legend.text = element_text(size = 20), strip.text = element_text(size = 20),
        legend.box.background = element_rect(colour = 'white'),
        legend.key = element_blank(),
        legend.key.size = unit(2, 'line'))

ggsave('plots/sp500_comparison_gamma0.5.png', width = 16, height = 9)


htest <- htest[1:(nrow(htest)-1),]
htest <- melt(htest, id = 'index', variable.name = 'Asset')
htest <- htest[!(htest$value == 0),]
ggplot(htest, aes(x = index, y = value, colour = Asset)) + 
  geom_point(size = 5) + geom_line(size = 0.3) +
  ggtitle('Investments in different stocks during testing periods') +
  xlab('Testing period') + ylab('Investment in stocks in USD') +
  theme(axis.text = element_text(size = 20), axis.title = element_text(size = 20),
        plot.title = element_text(size = 24, hjust = 0.5),
        legend.position = 'right',
        legend.title = element_text(size = 22),
        legend.text = element_text(size = 20), strip.text = element_text(size = 20),
        legend.box.background = element_rect(colour = 'white'),
        legend.key = element_blank(),
        legend.key.size = unit(2, 'line'))

ggsave('plots/htest_gamma0.5.png', width = 16, height = 9)



finalwealth <- read.csv('csv_files/finalwealthar-05gamma.csv')
colnames(finalwealth) <- c('index', 'wealth')
ggplot(finalwealth, aes(x = index, y = wealth)) + 
  geom_line(color = 'navy', size = 0.5) + geom_smooth(span = 0.3, color = 'red') +
  ggtitle('Final wealth of the training process') +
  xlab('Training period') + ylab('Wealth in USD') +
  theme(axis.text = element_text(size = 20), axis.title = element_text(size = 20),
        plot.title = element_text(size = 24, hjust = 0.5),
        legend.position = 'right',
        legend.title = element_text(size = 22),
        legend.text = element_text(size = 20), strip.text = element_text(size = 20),
        legend.box.background = element_rect(colour = 'white'),
        legend.key = element_blank(),
        legend.key.size = unit(2, 'line'))
ggsave('plots/finalwealth_gamma0.5.png', width = 16, height = 9)


V_optimize <- read.csv('csv_files/V_optimization-05gamma.csv')
colnames(V_optimize) <- c('index', 'V_opt')
ggplot(V_optimize, aes(x = index, y = V_opt)) + 
  geom_line(color = 'navy', size = 0.5) + geom_smooth(color = 'red', span = 0.3) +
  ggtitle('Final wealth of the training process') +
  xlab('Training period') + ylab('Wealth in USD') +
  theme(axis.text = element_text(size = 20), axis.title = element_text(size = 20),
        plot.title = element_text(size = 24, hjust = 0.5),
        legend.position = 'right',
        legend.title = element_text(size = 22),
        legend.text = element_text(size = 20), strip.text = element_text(size = 20),
        legend.box.background = element_rect(colour = 'white'),
        legend.key = element_blank(),
        legend.key.size = unit(2, 'line'))
ggsave('plots/V_optimize_gamma0.5.png', width = 16, height = 9)


##########################################################################################
##########################################################################################
##########################################################################################
# Now the same plots with the whole training set:
rm(list = ls())

htest = read.csv('csv_files/htest5.csv')
company_list = c('Amazon', 'Bank of New York', 'Barclays', 'Coca Cola', 'lowe‘s Companies',
                 'Nike', 'Norfolk Southern Railway', 'State Street Corporation', 'Walmart')
colnames(htest) = c('index', 'Riskless asset', company_list)
wealth_test <- htest
wealth <- rowSums(wealth_test[c('Riskless asset', company_list)])



sp500_weekly <- read.csv('csv_files/sp500weekly.csv')
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
  xlab('Date') + ylab('Difference') +
  ggtitle('Difference between portfolio value and S&P500') +
  geom_hline(yintercept = 0, linetype = 'dashed') +
  theme(axis.text = element_text(size = 20), axis.title = element_text(size = 20),
        plot.title = element_text(size = 24, hjust = 0.5),
        legend.position = 'right',
        legend.title = element_text(size = 22),
        legend.text = element_text(size = 20), strip.text = element_text(size = 20),
        legend.box.background = element_rect(colour = 'white'),
        legend.key = element_blank(),
        legend.key.size = unit(2, 'line'))

ggsave('plots/sp500_comparison5.png', width = 16, height = 9)


htest <- htest[1:(nrow(htest)-1),]
htest <- melt(htest, id = 'index', variable.name = 'Asset')
htest <- htest[!(htest$value == 0),]
ggplot(htest, aes(x = index, y = value, colour = Asset)) + 
  geom_point(size = 5) + geom_line(size = 0.3) +
  ggtitle('Investments in different stocks during testing periods') +
  xlab('Testing period') + ylab('Investment in stocks in USD') +
  theme(axis.text = element_text(size = 20), axis.title = element_text(size = 20),
        plot.title = element_text(size = 24, hjust = 0.5),
        legend.position = 'right',
        legend.title = element_text(size = 22),
        legend.text = element_text(size = 20), strip.text = element_text(size = 20),
        legend.box.background = element_rect(colour = 'white'),
        legend.key = element_blank(),
        legend.key.size = unit(2, 'line'))

ggsave('plots/htest5.png', width = 16, height = 9)



finalwealth <- read.csv('csv_files/finalwealthar5.csv')
colnames(finalwealth) <- c('index', 'wealth')
ggplot(finalwealth, aes(x = index, y = wealth)) + 
  geom_line(color = 'navy', size = 0.5) + geom_smooth(span = 0.3, color = 'red') +
  ggtitle('Final wealth of the training process') +
  xlab('Training period') + ylab('Wealth in USD') +
  theme(axis.text = element_text(size = 20), axis.title = element_text(size = 20),
        plot.title = element_text(size = 24, hjust = 0.5),
        legend.position = 'right',
        legend.title = element_text(size = 22),
        legend.text = element_text(size = 20), strip.text = element_text(size = 20),
        legend.box.background = element_rect(colour = 'white'),
        legend.key = element_blank(),
        legend.key.size = unit(2, 'line'))
ggsave('plots/finalwealth5.png', width = 16, height = 9)


V_optimize <- read.csv('csv_files/V_optimization5.csv')
colnames(V_optimize) <- c('index', 'V_opt')
ggplot(V_optimize, aes(x = index, y = V_opt)) + 
  geom_line(color = 'navy', size = 0.5) + geom_smooth(color = 'red', span = 0.3) +
  ggtitle('Final wealth of the training process') +
  xlab('Training period') + ylab('Wealth in USD') +
  theme(axis.text = element_text(size = 20), axis.title = element_text(size = 20),
        plot.title = element_text(size = 24, hjust = 0.5),
        legend.position = 'right',
        legend.title = element_text(size = 22),
        legend.text = element_text(size = 20), strip.text = element_text(size = 20),
        legend.box.background = element_rect(colour = 'white'),
        legend.key = element_blank(),
        legend.key.size = unit(2, 'line'))
ggsave('plots/V_optimize5.png', width = 16, height = 9)


