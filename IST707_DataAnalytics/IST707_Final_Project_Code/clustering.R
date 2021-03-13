library(dplyr)
library(caret)
library(factoextra)
library(cluster)

# read processed data
df <- read.csv(file.choose())
summary(df)

# reformat data
df_cluster <- df %>%
  mutate(product_color = as.numeric(as.factor(product_color)),
         origin_country = as.numeric(as.factor(origin_country)),
         ) %>%
  select(-merchant_name,-rating_level,-units_sold_level,-merchant_rating,
         -product_variation_size_id,-product_variation_inventory,-inventory_total,
         -badge_local_product,-badge_product_quality,-badge_fast_shipping)

str(df_cluster)
summary(df_cluster)

### product segmentation ###
# normalization
normalize <- function(x) {
  (x - min(x)) / (max(x)-min(x))
  }

df_norm <- df_cluster %>%
  mutate(price = normalize(price),
         retail_price = normalize(retail_price),
         rating = normalize(rating),
         product_color = normalize(product_color),
         shipping_option_price = normalize(shipping_option_price),
         origin_country = normalize(origin_country)
         )

# elbow diagram
df_elbow_plot <- df_norm %>%
  fviz_nbclust(kmeans,method = "wss")

df_elbow_plot

# k-means cluster
clustering <- df_norm %>%
  kmeans(centers = 4)

fviz_cluster(clustering, data = df_norm)

# HAC
distance_matrix <- df_norm %>%
  dist(method = "euclidean")

hier_clust_average <- distance_matrix %>%
  agnes(method = "average")
hier_clust_weighted <- distance_matrix %>%
  agnes(method = "weighted")
hier_clust_single <- distance_matrix %>%
  agnes(method = "single")
hier_clust_ward <- distance_matrix %>%
  agnes(method = "ward")

# compare different method
hier_clust_average$ac
hier_clust_weighted$ac
hier_clust_single$ac
hier_clust_ward$ac

pltree(hier_clust_ward,cex = 0.6, hang = -1,main = "Dendrogram of agnes")

tree_cut <- hier_clust_ward %>%
  cutree(3)
table(tree_cut)

df_cluster <- df_cluster %>%
  mutate(cluster = tree_cut)

# display cluster
cluster_1 <- df_cluster[which(df_cluster$cluster==1),]
summary(cluster_1)

cluster_2 <- df_cluster[which(df_cluster$cluster==2),]
summary(cluster_2)

cluster_3 <- df_cluster[which(df_cluster$cluster==3),]
summary(cluster_3)
