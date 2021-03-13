library(dplyr)

# read csv
product_info <- read.csv(file.choose())
str(product_info)

# remove irrelevant columns
new_product_info <- product_info %>%
  select(-title, -title_orig, -currency_buyer,-tags,-shipping_option_name,
         -has_urgency_banner,-urgency_text,-merchant_title,
         -merchant_info_subtitle,-merchant_id,-merchant_has_profile_picture,
         -merchant_profile_picture,-product_url,-product_picture,-product_id,
         -theme,-crawl_month,-countries_shipped_to,-merchant_rating_count)
summary(new_product_info)

# fill missing values
new_product_info$rating_five_count[is.na(new_product_info$rating_five_count)] <- mean(new_product_info$rating_five_count,na.rm = TRUE)
new_product_info$rating_four_count[is.na(new_product_info$rating_four_count)] <- mean(new_product_info$rating_four_count,na.rm = TRUE)
new_product_info$rating_three_count[is.na(new_product_info$rating_three_count)] <- mean(new_product_info$rating_three_count,na.rm = TRUE)
new_product_info$rating_two_count[is.na(new_product_info$rating_two_count)] <- mean(new_product_info$rating_two_count,na.rm = TRUE)
new_product_info$rating_one_count[is.na(new_product_info$rating_one_count)] <- mean(new_product_info$rating_one_count,na.rm = TRUE)
summary(new_product_info)

# fill null value
new_product_info <- new_product_info[-which(new_product_info$origin_country == ''),]
new_product_info <- new_product_info[-which(new_product_info$product_color == ''),]
new_product_info <- new_product_info[-which(new_product_info$product_variation_size_id == ''),]
new_product_info <- new_product_info[-which(new_product_info$merchant_name == ''),]
summary(new_product_info)

# reformat data
new_product_info <- new_product_info %>%
  mutate(product_color = as.factor(product_color),
         product_variation_size_id = as.factor(product_variation_size_id),
         origin_country = as.factor(origin_country),
         merchant_name = as.factor(merchant_name))
summary(new_product_info)

# create a new column -- rating level
new_product_info$rating_level <- new_product_info$rating_five_count/new_product_info$rating_count
new_product_info$rating_level[is.infinite(new_product_info$rating_level)] <- 0

# divide the range of two columns into intervals
new_product_info[,'rating_level'] <- cut(new_product_info$rating_level,breaks = c(-Inf,0.5,1),labels = c('low','high'))
new_product_info[,'units_sold_level'] <- cut(new_product_info$units_sold,breaks = c(-Inf,1000,Inf),labels = c('low','high'))

new_product_info <- new_product_info %>%
  select(-units_sold,-rating_count,-rating_five_count,-rating_four_count,-rating_three_count,-rating_two_count,-rating_one_count)

summary(new_product_info)
str(new_product_info)

# write csv 
write.csv(new_product_info,file="/Users/zly_0930/Desktop/IST707/final project/revised_data.csv",quote=F,row.names = F)
