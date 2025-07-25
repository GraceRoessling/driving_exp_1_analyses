# Define the contingency table
map_selection <- matrix(c(
  17, 3,
  16, 4,
  7, 13
), nrow = 3, byrow = TRUE)

rownames(map_selection) <- c("Control", "Scrambled Landmarks", "Scrambled Segments")
colnames(map_selection) <- c("Correct", "Incorrect")

groups <- rownames(map_selection)

# Perform pairwise chi-square tests with reporting
pairwise_chisq_detailed <- function(table) {
  n <- nrow(table)
  comparisons <- list()
  
  # Collect results in a data frame
  results <- data.frame(
    Comparison = character(),
    X2 = numeric(),
    df = integer(),
    Raw_p = numeric(),
    Adjusted_p = numeric(),
    stringsAsFactors = FALSE
  )
  
  for(i in 1:(n-1)) {
    for(j in (i+1):n) {
      group1 <- rownames(table)[i]
      group2 <- rownames(table)[j]
      pair_table <- table[c(i,j), ]
      
      test <- chisq.test(pair_table, correct = FALSE)
      
      # Store results
      results <- rbind(results, data.frame(
        Comparison = paste(group1, "vs", group2),
        X2 = round(test$statistic, 3),
        df = test$parameter,
        Raw_p = test$p.value,
        Adjusted_p = NA  # Placeholder, will adjust below
      ))
    }
  }
  
  # Adjust p-values
  results$Adjusted_p <- p.adjust(results$Raw_p, method = "bonferroni")
  
  return(results)
}

# Run the pairwise tests
pairwise_results <- pairwise_chisq_detailed(map_selection)

# Print results
print(pairwise_results)
