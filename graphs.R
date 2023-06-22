library(ggplot2)
perSector <- read.csv("generatedCSVs/postsPerSectors.csv",header = TRUE)
sectorPlot <- ggplot(perSector, aes( x=factor(sector,level = rev(perSector$sector)) , y = avgPosts)) + geom_bar(stat = 'identity', fill="steelblue") + theme(panel.background = element_blank()) + labs(x = "sector",title = "Avreage number of posts of each company per sector") + coord_flip()

png("perSector.png")
sectorPlot
dev.off()

salaries <- read.csv("generatedCSVs/salaries.csv",header = TRUE)
salariesPlot <-  ggplot(salaries,aes(x = avgLow, y =  factor(location,level = rev(salaries$location)))) + geom_point() + geom_point(aes(x = avgHigh, y =  factor(location,level = rev(salaries$location))),color = "red")+ theme(panel.grid.minor = element_blank(),axis.title.y=element_blank()) + scale_x_continuous( limits=c(25,140),breaks = seq(25,140,25)) + labs(x = "mean Low salary (black)   mean High salary(red)", title = " Average mean salary for location")

png("salariesByLow.png")
salariesPlot
dev.off()

salOrder <- salaries[order(salaries$avgRating, decreasing = TRUE),]

salByRat<- ggplot(salOrder,aes(y = avgHigh, x =  factor(location,level = rev(salOrder$location)))) + geom_bar(stat="identity", fill = "steelblue") + labs(x = "mean Low salary (black)   mean High salary(red)", title = " Average High salary for location ordered by average rating") + coord_flip() +  theme(panel.background = element_blank(), axis.title.y = element_blank(), axis.title.x = element_blank())


png("salariesByRating.png")
salByRat
dev.off()

jobs = read.csv("generatedCSVs/jobs.csv",header = TRUE)
jobs[jobs == "None"] = NaN
df2 <- jobs[!is.na(jobs$founded) & !is.na(jobs$high) & !is.na(jobs$rating) & !is.na(jobs$size),]
df2$founded <- as.numeric(as.character(df2$founded))
df2$rating <- as.numeric(as.character(df2$rating))
df2$high <- as.numeric(as.character(df2$high))
df2$size <- as.numeric(as.character(df2$size))



foundedOverHigh <-  ggplot(df2,aes(x = founded, y = high, color = rating))+ geom_point()+ scale_color_gradient(low = "white", high = "blue") +  theme(panel.background = element_blank(), axis.title.x = element_blank(),axis.title.y = element_blank()) + labs(title = "Offers of high salary over year of foundation")

png("foundedOverHigh.png")
foundedOverHigh
dev.off()

foundedOverHighWrapBySize <-ggplot(df2,aes(x = founded, y = high, color = rating))+ geom_point()+ facet_wrap(~size, ncol = 3)+ scale_color_gradient(low = "white", high = "blue") +  theme(panel.background = element_blank(), axis.title.x = element_blank(),axis.title.y = element_blank()) + labs(title = "Offers of high salary over year of foundation grouped by company size")

png("foundedOverHighWrappedBySize.png")
foundedOverHighWrapBySize
dev.off()



