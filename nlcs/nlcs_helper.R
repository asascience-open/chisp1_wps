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
    rawdata$OrganizationIdentifier <- OrganizationIdentifier
    rawdata$OrganizationFormalName <- OrganizationFormalName
    rawdata$ActivityIdentifier <- ActivityIdentifier
    rawdata$ActivityTypeCode <- ActivityTypeCode
    rawdata$ActivityMediaName <- ActivityMediaName
    rawdata$ActivityMediaSubdivisionName <- ActivityMediaSubdivisionName
    rawdata$ActivityStartDate <- ActivityStartDate
    rawdata$ActivityStartTime.Time <- ActivityStartTime_Time
    rawdata$ActivityStartTime.TimeZoneCode <- ActivityStartTime_TimeZoneCode
    rawdata$ActivityEndDate <- ActivityEndDate
    rawdata$ActivityEndTime.Time <- ActivityEndTime_Time
    rawdata$ActivityEndTime.TimeZoneCode <- ActivityEndTime_TimeZoneCode
    rawdata$ActivityDepthHeightMeasure.MeasureValue <- ActivityDepthHeightMeasure_MeasureValue
    rawdata$ActivityDepthHeightMeasure.MeasureUnitCode <- ActivityDepthHeightMeasure_MeasureUnitCode
    rawdata$ActivityDepthAltitudeReferencePointText <- ActivityDepthAltitudeReferencePointText
    rawdata$ActivityTopDepthHeightMeasure.MeasureValue <- ActivityTopDepthHeightMeasure_MeasureValue
    rawdata$ActivityTopDepthHeightMeasure.MeasureUnitCode <- ActivityTopDepthHeightMeasure_MeasureUnitCode
    rawdata$ActivityBottomDepthHeightMeasure.MeasureValue <- ActivityBottomDepthHeightMeasure_MeasureValue
    rawdata$ActivityBottomDepthHeightMeasure.MeasureUnitCode <- ActivityBottomDepthHeightMeasure_MeasureUnitCode
    rawdata$ProjectIdentifier <- ProjectIdentifier
    rawdata$ActivityConductingOrganizationText <- ActivityConductingOrganizationText
    rawdata$MonitoringLocationIdentifier <- MonitoringLocationIdentifier
    rawdata$ActivityCommentText <- ActivityCommentText
    rawdata$SampleAquifer <- SampleAquifer
    rawdata$HydrologicCondition <- HydrologicCondition
    rawdata$HydrologicEvent <- HydrologicEvent
    rawdata$SampleCollectionMethod.MethodIdentifier <- SampleCollectionMethod_MethodIdentifier
    rawdata$SampleCollectionMethod.MethodIdentifierContext <- SampleCollectionMethod_MethodIdentifierContext
    rawdata$SampleCollectionMethod.MethodName <- SampleCollectionMethod_MethodName
    rawdata$SampleCollectionEquipmentName <- SampleCollectionEquipmentName
    rawdata$ResultDetectionConditionText <- ResultDetectionConditionText
    rawdata$CharacteristicName <- CharacteristicName
    rawdata$ResultSampleFractionText <- ResultSampleFractionText
    rawdata$ResultMeasureValue <- ResultMeasureValue
    rawdata$ResultMeasure.MeasureUnitCode <- ResultMeasure_MeasureUnitCode
    rawdata$MeasureQualifierCode <- MeasureQualifierCode
    rawdata$ResultStatusIdentifier <- ResultStatusIdentifier
    rawdata$StatisticalBaseCode <- StatisticalBaseCode
    rawdata$ResultValueTypeName <- ResultValueTypeName
    rawdata$ResultWeightBasisText <- ResultWeightBasisText
    rawdata$ResultTimeBasisText <- ResultTimeBasisText
    rawdata$ResultTemperatureBasisText <- ResultTemperatureBasisText
    rawdata$ResultParticleSizeBasisText <- ResultParticleSizeBasisText
    rawdata$PrecisionValue <- PrecisionValue
    rawdata$ResultCommentText <- ResultCommentText
    rawdata$USGSPCode <- USGSPCode
    rawdata$ResultDepthHeightMeasure.MeasureValue <- ResultDepthHeightMeasure_MeasureValue
    rawdata$ResultDepthHeightMeasure.MeasureUnitCode <- ResultDepthHeightMeasure_MeasureUnitCode
    rawdata$ResultDepthAltitudeReferencePointText <- ResultDepthAltitudeReferencePointText
    rawdata$SubjectTaxonomicName <- SubjectTaxonomicName
    rawdata$SampleTissueAnatomyName <- SampleTissueAnatomyName
    rawdata$ResultAnalyticalMethod.MethodIdentifier <- ResultAnalyticalMethod_MethodIdentifier
    rawdata$ResultAnalyticalMethod.MethodIdentifierContext <- ResultAnalyticalMethod_MethodIdentifierContext
    rawdata$ResultAnalyticalMethod.MethodName <- ResultAnalyticalMethod_MethodName
    rawdata$MethodDescriptionText <- MethodDescriptionText
    rawdata$LaboratoryName <- LaboratoryName
    rawdata$AnalysisStartDate <- AnalysisStartDate
    rawdata$ResultLaboratoryCommentText <- ResultLaboratoryCommentText
    rawdata$DetectionQuantitationLimitTypeName <- DetectionQuantitationLimitTypeName
    rawdata$DetectionQuantitationLimitMeasure.MeasureValue <- DetectionQuantitationLimitMeasure_MeasureValue
    rawdata$DetectionQuantitationLimitMeasure.MeasureUnitCode <- DetectionQuantitationLimitMeasure_MeasureUnitCode
    rawdata$PreparationStartDate <- PreparationStartDate
    processed_data <- processQWData(rawdata)
    compressed_data <- compressData(processed_data, interactive=FALSE)
    Sample <- populateSampleColumns(compressed_data)
    return(Sample)
}
