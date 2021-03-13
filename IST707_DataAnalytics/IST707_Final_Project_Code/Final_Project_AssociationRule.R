library(dplyr)
library(arules)

# read processed data
df <- read.csv(file.choose())

summary(df)
str(df)

# reformat data
df_ar <- df %>%
  mutate(badge_local_product = as.factor(badge_local_product),
         uses_ad_boosts = as.factor(uses_ad_boosts),
         badge_product_quality = as.factor(badge_product_quality),
         badge_fast_shipping = as.factor(badge_fast_shipping),
         product_color = as.factor(product_color),
         shipping_is_express = as.factor(shipping_is_express),
         origin_country = as.factor(origin_country),
         rating_level = as.factor(rating_level),
         merchant_rating = as.factor(merchant_rating)
         ) %>%
  select(-rating,-badges_count,-product_variation_size_id,-product_variation_inventory,-inventory_total,
         -units_sold_level,-merchant_name)
summary(df_ar)

# convert numeric variables
df_ar[,'price'] <- cut(as.numeric(df_ar$price), breaks = c(-Inf,6,11,Inf),labels = c('<6','6-11','>11'))
df_ar[,'retail_price'] <- cut(as.numeric(df_ar$retail_price), breaks = c(-Inf,7,26,Inf),labels = c('<7','7-26','>26'))
df_ar[,'shipping_option_price'] <- cut(as.numeric(df_ar$shipping_option_price), breaks = c(-Inf,3,Inf),labels = c('<3','>=3'))

str(df_ar)
# transfer into transaction
df_ar_trans <- as(df_ar,"transactions")

rating_rules <- apriori(df_ar_trans,parameter = list(supp = 0.01,conf = 0.8, minlen = 2),appearance = list(rhs='rating_level=high'))
rating_rules <- apriori(df_ar_trans,parameter = list(supp = 0.1,conf = 0.8, minlen = 2),appearance = list(rhs='rating_level=high'))

rating_rules <- apriori(df_ar_trans,parameter = list(supp = 0.05,conf = 0.9, minlen = 4),appearance = list(rhs='rating_level=high'))

summary(rating_rules)

inspect(sort(rating_rules,by="support"))


