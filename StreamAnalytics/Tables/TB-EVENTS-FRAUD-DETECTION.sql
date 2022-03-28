SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[TB_EVENTS_FRAUD_DETECTION]
( 
	[id] [varchar](100)  NULL,
	[customeridOrig] [int]  NULL,
	[EventEnqueuedUtcTime] [datetime]  NULL,
	[type] [int]  NULL,
	[amount] [money]  NULL,
	[oldbalanceOrg] [money]  NULL,
	[newbalanceOrig] [money]  NULL,
	[customeridDest] [int]  NULL,
	[oldbalanceDest] [money]  NULL,
	[newbalanceDest] [money]  NULL,
	[hour] [tinyint]  NULL,
	[dayOfMonth] [tinyint]  NULL,
	[isMerchantDest] [bit]  NULL,
	[errorBalanceOrig] [money]  NULL,
	[errorBalanceDest] [money]  NULL,
	[EventProcessedUtcTime] [datetime]  NULL,
	[prediction] [bit]  NULL,
	[fraud] [bit]  NULL
)
WITH
(
	DISTRIBUTION = ROUND_ROBIN,
	CLUSTERED COLUMNSTORE INDEX
)
GO