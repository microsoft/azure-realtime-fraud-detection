SELECT GetMetadataPropertyValue([EH-FRAUD], 'EventId') AS id,
       EventEnqueuedUtcTime,
       customeridOrig,
       type,
       amount,
       oldbalanceOrg,
       newbalanceOrig,
       customeridDest,
       oldbalanceDest,
       newbalanceDest,
       hour,
       dayOfMonth,
       isMerchantDest,
       errorBalanceOrig,
       errorBalanceDest,
       EventProcessedUtcTime,
       CAST(prediction AS bit) AS prediction      
INTO [COSMOSDB-FRAUD]
FROM
    [EH-FRAUD]


SELECT GetMetadataPropertyValue([EH-FRAUD], 'EventId') AS id,
       EventEnqueuedUtcTime,
       customeridOrig,
       type,
       amount,
       oldbalanceOrg,
       newbalanceOrig,
       customeridDest,
       oldbalanceDest,
       newbalanceDest,
       hour,
       dayOfMonth,
       isMerchantDest,
       errorBalanceOrig,
       errorBalanceDest,
       EventProcessedUtcTime,
       CAST(prediction AS bit) AS prediction
INTO SQLPOOL
FROM [EH-FRAUD]