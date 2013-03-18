
library("dataRetrieval")

process_nlcs_wq <- function(url,interactive=FALSE){
  suppressWarnings(retval <- read.delim(url, header = TRUE, quote="\"", dec=".", sep='\t', colClasses=c('character'), fill = TRUE))
  
  qualifier <- ifelse((
    (
      retval$ResultDetectionConditionText == "Not Detected"
      & length(grep("Lower", retval$DetectionQuantitationLimitTypeName)) > 0
    )
    | 
      (
        retval$ResultMeasureValue < retval$DetectionQuantitationLimitMeasure.MeasureValue
        & retval$ResultValueTypeName == "Actual"
      )
  ),
                      "<",
                      ""
  )
  
  correctedData<-ifelse((nchar(qualifier)==0),retval$ResultMeasureValue,retval$DetectionQuantitationLimitMeasure.MeasureValue)
  test <- data.frame(retval$USGSPCode)
  
  #   test$dateTime <- as.POSIXct(strptime(paste(retval$ActivityStartDate,retval$ActivityStartTime.Time,sep=" "), "%Y-%m-%d %H:%M:%S"))
  test$dateTime <- as.Date(retval$ActivityStartDate, "%Y-%m-%d")
  
  originalLength <- nrow(test)
  test$qualifier <- qualifier
  test$value <- as.numeric(correctedData)
  
  test <- test[!is.na(test$dateTime),]
  newLength <- nrow(test)
  if (originalLength != newLength){
    numberRemoved <- originalLength - newLength
    warningMessage <- paste(numberRemoved, " rows removed because no date was specified", sep="")
    warning(warningMessage)
  }
  
  colnames(test)<- c("USGSPCode","dateTime","qualifier","value")
  data <- reshape(test, idvar="dateTime", timevar = "USGSPCode", direction="wide")    
  data$dateTime <- format(data$dateTime, "%Y-%m-%d")
  data$dateTime <- as.Date(data$dateTime)
  return(data)
}

processQWData <- function(data){

  qualifier <- ifelse((data$ResultDetectionConditionText == "Not Detected" | 
                    data$ResultDetectionConditionText == "Detected Not Quantified" |
                    data$ResultMeasureValue < data$DetectionQuantitationLimitMeasure.MeasureValue),"<","")
  
  correctedData<-ifelse((nchar(qualifier)==0),data$ResultMeasureValue,data$DetectionQuantitationLimitMeasure.MeasureValue)
  test <- data.frame(data$USGSPCode)
  
  #   test$dateTime <- as.POSIXct(strptime(paste(data$ActivityStartDate,data$ActivityStartTime.Time,sep=" "), "%Y-%m-%d %H:%M:%S"))
  #print(data)
  test$dateTime <- as.Date(data$ActivityStartDate, "%Y-%m-%d")
  
  originalLength <- nrow(test)
  test$qualifier <- qualifier
  test$value <- as.numeric(correctedData)
  
  test <- test[!is.na(test$dateTime),]
  newLength <- nrow(test)
  if (originalLength != newLength){
    numberRemoved <- originalLength - newLength
    warningMessage <- paste(numberRemoved, " rows removed because no date was specified", sep="")
    warning(warningMessage)
  }
  
  colnames(test)<- c("USGSPCode","dateTime","qualifier","value")
  data <- suppressWarnings(reshape(test, idvar="dateTime", timevar = "USGSPCode", direction="wide"))
  
  data$dateTime <- format(data$dateTime, "%Y-%m-%d")
  data$dateTime <- as.Date(data$dateTime)
  return(data)
}
