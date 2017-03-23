library(magrittr)
library(tidyverse)

# install.packages("rpart.plot")
# install.packages("rattle")
# install.packages("rattle")
library(rpart)
library(rpart.plot)
library(rattle)
library(randomForest)

## set working directory first
dat.before <- read.csv("data/2015.csv")
dat.after <- read.csv("data/2016.csv")
# dat %>% head %>% str
# dat %>% dim

set.seed(1205)
dat.train <- dat.before %>% filter(season_type==2) %>% select(-id,-season_type)
dat.test <- dat.after %>% filter(season_type==2) %>% select(-id,-season_type)

dtreeM <- rpart(formula = two_way_winner ~ ., 
                data = dat.train %>% select(-handicap_winner,-over_under_result,
                                           -home_line_margin)
                ,method = "class"
                , control = rpart.control(maxdepth = 4)
                )
dtreeM
fancyRpartPlot(dtreeM)

#(2)跑隨機樹森林模型
randomforestM <- randomForest(two_way_winner ~ ., data = dat.train %>% select(-handicap_winner,-over_under_result,
                                                                              -home_line_margin), 
                              importane = T, proximity = T, do.trace = 100)
randomforestM

#錯誤率: 利用OOB(Out Of Bag)運算出來的
plot(randomforestM)

#衡量每一個變數對Y值的重要性，取到小數點第二位
round(importance(randomforestM), 2)

result <- predict(dtreeM, newdata = dat.test, type = "class")
#(6)建立混淆矩陣(confusion matrix)觀察模型表現

#(3)預測
result <- predict(randomforestM, newdata = dat.test, type = "class")
# result_Approved <- ifelse(result > 0.6, 1, 0)

cm <- table(dat.test$two_way_winner, result, dnn = c("實際", "預測"))
cm

#(6)正確率
#計算主場正確率
cm[4] / sum(cm[, 2])

#計算客場正確率
cm[1] / sum(cm[, 1])

#整體準確率(取出對角/總數)
accuracy <- sum(diag(cm)) / sum(cm)
accuracy

## 讓分 ##########################################
dat.train <- dat.before %>% filter(season_type==2) %>% select(-id,-season_type)
dat.train %<>% filter(handicap_winner %in% c("away","home")) 
dat.train %<>% mutate(handicap_winner = as.character(dat.train$handicap_winner) %>% as.factor)
dat.test <- dat.after %>% filter(season_type==2) %>% select(-id,-season_type)
dat.test %<>% filter(handicap_winner %in% c("away","home")) 
dat.test %<>% mutate(handicap_winner = as.character(dat.test$handicap_winner) %>% as.factor)

dtreeM <- rpart(formula =  handicap_winner ~ ., 
                data = dat.train %>% select(-two_way_winner,-over_under_result)
                ,method = "class"
                , control = rpart.control(maxdepth = 4)
)
dtreeM
fancyRpartPlot(dtreeM)

# dat.before$handicap_winner %>% table
# dat.before %>% head %>% View
randomforestM <- randomForest(handicap_winner ~ ., 
                              data = dat.train %>% select(-two_way_winner,
                                                          -over_under_result, -home_line_margin,
                                                          -over_under) %>% na.omit, 
                              importane = T, proximity = T, do.trace = 100)
randomforestM

#錯誤率: 利用OOB(Out Of Bag)運算出來的
plot(randomforestM)
round(importance(randomforestM), 2)

result <- predict(dtreeM, newdata = dat.test, type = "class")
result <- predict(randomforestM, newdata = dat.test, type = "class")
#(6)建立混淆矩陣(confusion matrix)觀察模型表現
cm <- table(dat.test$handicap_winner, result, dnn = c("實際", "預測"))
cm

#(6)正確率
#計算主場正確率
cm[4] / sum(cm[, 2])

#計算客場正確率
cm[1] / sum(cm[, 1])

#整體準確率(取出對角/總數)
accuracy <- sum(diag(cm)) / sum(cm)
accuracy


## 大小分 #########
dat.train %<>% filter(over_under_result %in% c("over","under")) 
dat.train %<>% mutate(over_under_result = as.character(dat.train$over_under_result) %>% as.factor)
# dat.train %>% dim
# dat.train$over_under_result %>% table
dtreeM <- rpart(formula =  over_under_result~ ., 
                data = dat.train %>% select(-two_way_winner,-handicap_winner)
                ,method = "class"
                , control = rpart.control(maxdepth = 4)
)
dtreeM
fancyRpartPlot(dtreeM)

# dat.before$handicap_winner %>% table
# dat.before %>% head %>% View
dat.test %<>% filter(over_under_result %in% c("over","under")) 
dat.test %<>% mutate(over_under_result = as.character(dat.test$over_under_result) %>% as.factor)

result <- predict(dtreeM, newdata = dat.test, type = "class")

#(6)建立混淆矩陣(confusion matrix)觀察模型表現
cm <- table(dat.test$over_under_result, result, dnn = c("實際", "預測"))
cm

#(6)正確率
#計算主場正確率
cm[4] / sum(cm[, 2])

#計算客場正確率
cm[1] / sum(cm[, 1])

#整體準確率(取出對角/總數)
accuracy <- sum(diag(cm)) / sum(cm)
accuracy
