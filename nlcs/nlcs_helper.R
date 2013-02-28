library("dataRetrieval")

process_nlcs_wq <- function(OrganizationIdentifier,
                            OrganizationFormalName,
                            ActivityIdentifier,
                            ActivityTypeCode,
                            ActivityMediaName,
                            ActivityMediaSubdivisionName,
                            ActivityStartDate,
                            ActivityStartTime_Time,
                            ActivityStartTime_TimeZoneCode,
                            ActivityEndDate,
                            ActivityEndTime_Time,
                            ActivityEndTime_TimeZoneCode,
                            ActivityDepthHeightMeasure_MeasureValue,
                            ActivityDepthHeightMeasure_MeasureUnitCode,
                            ActivityDepthAltitudeReferencePointText,
                            ActivityTopDepthHeightMeasure_MeasureValue,
                            ActivityTopDepthHeightMeasure_MeasureUnitCode,
                            ActivityBottomDepthHeightMeasure_MeasureValue,
                            ActivityBottomDepthHeightMeasure_MeasureUnitCode,
                            ProjectIdentifier,
                            ActivityConductingOrganizationText,
                            MonitoringLocationIdentifier,
                            ActivityCommentText,
                            SampleAquifer,
                            HydrologicCondition,
                            HydrologicEvent,
                            SampleCollectionMethod_MethodIdentifier,
                            SampleCollectionMethod_MethodIdentifierContext,
                            SampleCollectionMethod_MethodName,
                            SampleCollectionEquipmentName,
                            ResultDetectionConditionText,
                            CharacteristicName,
                            ResultSampleFractionText,
                            ResultMeasureValue,
                            ResultMeasure_MeasureUnitCode,
                            MeasureQualifierCode,
                            ResultStatusIdentifier,
                            StatisticalBaseCode,
                            ResultValueTypeName,
                            ResultWeightBasisText,
                            ResultTimeBasisText,
                            ResultTemperatureBasisText,
                            ResultParticleSizeBasisText,
                            PrecisionValue,
                            ResultCommentText,
                            USGSPCode,
                            ResultDepthHeightMeasure_MeasureValue,
                            ResultDepthHeightMeasure_MeasureUnitCode,
                            ResultDepthAltitudeReferencePointText,
                            SubjectTaxonomicName,
                            SampleTissueAnatomyName,
                            ResultAnalyticalMethod_MethodIdentifier,
                            ResultAnalyticalMethod_MethodIdentifierContext,
                            ResultAnalyticalMethod_MethodName,
                            MethodDescriptionText,
                            LaboratoryName,
                            AnalysisStartDate,
                            ResultLaboratoryCommentText,
                            DetectionQuantitationLimitTypeName,
                            DetectionQuantitationLimitMeasure_MeasureValue,
                            DetectionQuantitationLimitMeasure_MeasureUnitCode,
                            PreparationStartDate){
    #data <- getQWData(siteNumber,ParameterCd,StartDate,EndDate,interactive=interactive)
    #rawSample <- getRawQWData(siteNumber,ParameterCd,StartDate,EndDate,interactive)
    print(OrganizationIdentifier)
    rawdata <- data.frame(OrganizationIdentifier,
                            OrganizationFormalName,
                            ActivityIdentifier,
                            ActivityTypeCode,
                            ActivityMediaName,
                            ActivityMediaSubdivisionName,
                            ActivityStartDate,
                            ActivityStartTime_Time,
                            ActivityStartTime_TimeZoneCode,
                            ActivityEndDate,
                            ActivityEndTime_Time,
                            ActivityEndTime_TimeZoneCode,
                            ActivityDepthHeightMeasure_MeasureValue,
                            ActivityDepthHeightMeasure_MeasureUnitCode,
                            ActivityDepthAltitudeReferencePointText,
                            ActivityTopDepthHeightMeasure_MeasureValue,
                            ActivityTopDepthHeightMeasure_MeasureUnitCode,
                            ActivityBottomDepthHeightMeasure_MeasureValue,
                            ActivityBottomDepthHeightMeasure_MeasureUnitCode,
                            ProjectIdentifier,
                            ActivityConductingOrganizationText,
                            MonitoringLocationIdentifier,
                            ActivityCommentText,
                            SampleAquifer,
                            HydrologicCondition,
                            HydrologicEvent,
                            SampleCollectionMethod_MethodIdentifier,
                            SampleCollectionMethod_MethodIdentifierContext,
                            SampleCollectionMethod_MethodName,
                            SampleCollectionEquipmentName,
                            ResultDetectionConditionText,
                            CharacteristicName,
                            ResultSampleFractionText,
                            ResultMeasureValue,
                            ResultMeasure_MeasureUnitCode,
                            MeasureQualifierCode,
                            ResultStatusIdentifier,
                            StatisticalBaseCode,
                            ResultValueTypeName,
                            ResultWeightBasisText,
                            ResultTimeBasisText,
                            ResultTemperatureBasisText,
                            ResultParticleSizeBasisText,
                            PrecisionValue,
                            ResultCommentText,
                            USGSPCode,
                            ResultDepthHeightMeasure_MeasureValue,
                            ResultDepthHeightMeasure_MeasureUnitCode,
                            ResultDepthAltitudeReferencePointText,
                            SubjectTaxonomicName,
                            SampleTissueAnatomyName,
                            ResultAnalyticalMethod_MethodIdentifier,
                            ResultAnalyticalMethod_MethodIdentifierContext,
                            ResultAnalyticalMethod_MethodName,
                            MethodDescriptionText,
                            LaboratoryName,
                            AnalysisStartDate,
                            ResultLaboratoryCommentText,
                            DetectionQuantitationLimitTypeName,
                            DetectionQuantitationLimitMeasure_MeasureValue,
                            DetectionQuantitationLimitMeasure_MeasureUnitCode,
                            PreparationStartDate)
    rawdata.names<-c('OrganizationIdentifier','OrganizationFormalName','ActivityIdentifier','ActivityTypeCode','ActivityMediaName','ActivityMediaSubdivisionName','ActivityStartDate','ActivityStartTime.Time','ActivityStartTime.TimeZoneCode','ActivityEndDate','ActivityEndTime.Time','ActivityEndTime.TimeZoneCode','ActivityDepthHeightMeasure.MeasureValue','ActivityDepthHeightMeasure.MeasureUnitCode','ActivityDepthAltitudeReferencePointText','ActivityTopDepthHeightMeasure.MeasureValue','ActivityTopDepthHeightMeasure.MeasureUnitCode','ActivityBottomDepthHeightMeasure.MeasureValue','ActivityBottomDepthHeightMeasure.MeasureUnitCode','ProjectIdentifier','ActivityConductingOrganizationText','MonitoringLocationIdentifier','ActivityCommentText','SampleAquifer','HydrologicCondition','HydrologicEvent','SampleCollectionMethod.MethodIdentifier','SampleCollectionMethod.MethodIdentifierContext','SampleCollectionMethod.MethodName','SampleCollectionEquipmentName','ResultDetectionConditionText','CharacteristicName','ResultSampleFractionText','ResultMeasureValue','ResultMeasure.MeasureUnitCode','MeasureQualifierCode','ResultStatusIdentifier','StatisticalBaseCode','ResultValueTypeName','ResultWeightBasisText','ResultTimeBasisText','ResultTemperatureBasisText','ResultParticleSizeBasisText','PrecisionValue','ResultCommentText','USGSPCode','ResultDepthHeightMeasure.MeasureValue','ResultDepthHeightMeasure.MeasureUnitCode','ResultDepthAltitudeReferencePointText','SubjectTaxonomicName','SampleTissueAnatomyName','ResultAnalyticalMethod.MethodIdentifier','ResultAnalyticalMethod.MethodIdentifierContext','ResultAnalyticalMethod.MethodName','MethodDescriptionText','LaboratoryName','AnalysisStartDate','ResultLaboratoryCommentText','DetectionQuantitationLimitTypeName','DetectionQuantitationLimitMeasure.MeasureValue','DetectionQuantitationLimitMeasure.MeasureUnitCode','PreparationStartDate')
    processed_data <- processQWData(rawdata)
    compressed_data <- compressData(processed_data, interactive=FALSE)
    Sample <- populateSampleColumns(compressed_data)
    return(Sample)
}

processQWData <- function(data){

  qualifier <- ifelse((data$ResultDetectionConditionText == "Not Detected" | 
                    data$ResultDetectionConditionText == "Detected Not Quantified" |
                    data$ResultMeasureValue < data$DetectionQuantitationLimitMeasure.MeasureValue),"<","")
  
  correctedData<-ifelse((nchar(qualifier)==0),data$ResultMeasureValue,data$DetectionQuantitationLimitMeasure.MeasureValue)
  test <- data.frame(data$USGSPCode)
  
  #   test$dateTime <- as.POSIXct(strptime(paste(data$ActivityStartDate,data$ActivityStartTime.Time,sep=" "), "%Y-%m-%d %H:%M:%S"))
  print(data)
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
