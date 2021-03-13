library(caret)
library(dplyr)
library(kernlab)
library(stringr)
library(fastAdaboost)
library(ranger)

# read processed data
df <- read.csv(file.choose())
str(df)

# reformat data
df_class <- df %>%
  mutate(uses_ad_boosts = as.factor(uses_ad_boosts),
         badge_local_product = as.factor(badge_local_product),
         badge_product_quality = as.factor(badge_product_quality),
         badge_fast_shipping = as.factor(badge_fast_shipping),
         product_color = as.factor(product_color),
         product_variation_size_id = as.factor(product_variation_size_id),
         shipping_is_express = as.factor(shipping_is_express),
         origin_country = as.factor(origin_country),
         units_sold_level = as.factor(case_when(units_sold_level == 'high'~1,TRUE~0))) %>%
  select(-badges_count,-merchant_name,-rating_level)

str(df_class)

### split data ###
set.seed(1)
trainIndex <- createDataPartition(df_class$units_sold_level, 
                                  p = .8, 
                                  list = FALSE, 
                                  times = 1)
trainset <- df_class[trainIndex,]
testset <- df_class[-trainIndex,]

Controls <- trainControl(method = "repeatedcv",
                         number = 10)

# KNN
# Creating a min-max normalization function
norm_min_max <-function(x) { 
  ( x - min(x) ) / ( max(x) - min(x) )
}

# train model
knn_train <- trainset %>%
  mutate(price = norm_min_max(price),
         rating = norm_min_max(rating),
         product_variation_inventory = norm_min_max(product_variation_inventory),
         shipping_option_price = norm_min_max(shipping_option_price),
         inventory_total = norm_min_max(inventory_total),
         merchant_rating = norm_min_max(merchant_rating))

knn_test <- testset %>%
  mutate(price = norm_min_max(price),
         rating = norm_min_max(rating),
         product_variation_inventory = norm_min_max(product_variation_inventory),
         shipping_option_price = norm_min_max(shipping_option_price),
         inventory_total = norm_min_max(inventory_total),
         merchant_rating = norm_min_max(merchant_rating))

knn_train_category <- df_class[trainIndex, 'units_sold_level']
knn_test_category <- df_class[-trainIndex, 'units_sold_level']

model_knn <- train(units_sold_level ~ ., 
                   data = knn_train, 
                   method = "knn",
                   trControl = Controls, 
                   tuneLength=40)

model_knn

# evaluation
knnPredict <- predict(model_knn,
                      newdata = knn_test)
cm_knn <- confusionMatrix(knnPredict, 
                          knn_test_category)

# Random Forest
training_independent_vars = trainset[,-16]
trainingOutcomes = trainset$units_sold_level

model_rf <- train(training_independent_vars,
                  trainingOutcomes,
                  method = 'ranger',
                  trControl = Controls,
                  tuneGrid = expand.grid(mtry=c(8,10,12),splitrule='gini',min.node.size = c(1,2,4)))
model_rf

# evaluation
rfPredict <- predict(model_rf,
                     newdata = testset)
cm_rf <- confusionMatrix(rfPredict, 
                         testset$units_sold_level)

### SVMs ###
# preprocess for svm
str(df_class)
df_class1 <- df_class %>%
  mutate(product_color = as.factor(as.numeric(product_color)),
         product_variation_size_id = as.factor(as.numeric(product_variation_size_id)),
         origin_country = as.factor(as.numeric(origin_country)))

str(df_class1)

# split
svm_trainset <-df_class1[trainIndex,]
svm_testset <-df_class1[-trainIndex,]

#Polynomial Kernel
model_pk <-train(units_sold_level ~ .,
                 data = svm_trainset, 
                 method="svmPoly",
                 trControl = Controls,
                 tuneGrid=expand.grid(degree=c(1,2),scale=0.1,C =c(0.05,0.1,0.5)))
model_pk

# evaluation
pkPredict <- predict(model_pk,
                     newdata = svm_testset )
cm_pk <- confusionMatrix(pkPredict, 
                         svm_testset$units_sold_level)

# ANN
model_ann <- train(units_sold_level ~ .,
                  data = svm_trainset,
                  method = "nnet",
                  trControl = Controls,
                  tuneGrid = expand.grid(size = c(1,2,3), decay = c(0.05,0.1)))
model_ann
# prediction
annPredict <- predict(model_ann,
                       newdata = svm_testset)

cm_ann <- confusionMatrix(annPredict, testset$units_sold_level)

# comparison
cm_knn
cm_rf
cm_pk
cm_ann

# visualization
roc_imp <- varImp(model_pk, scale = FALSE)
plot(roc_imp)
