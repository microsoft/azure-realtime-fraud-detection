# Project

> This repo has been populated by an initial template to help get you started. Please
> make sure to update the content to build a great experience for community-building.

As the maintainer of this project, please make a few updates:

- Improving this README.MD file to provide a great experience
- Updating SUPPORT.MD with content about this project's support experience
- Understanding the security reporting process in SECURITY.MD
- Remove this section from the README

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.


# ToDo

## AzureML
*  Pegar Notebooks, Scripts de Inferência dentro do Azure ML e o que for necessário dentro do Azure ML e colocar na Pasta de Azure ML. 
* Esses scripts são os que criam a imagem dos modelos que está dentro do AKS ?

## Event Hubs

* Na hora do script de criação criar um tópico com o nome de "ehfraud" e um consumer group dentro desse tópico "asa-consumer-group-fraud" além do consumer "#Default"

## Stream Analytics

* Único Input é o do Event hub 
* Quey dentro da pasta StreamAnalytics
* O Stream Analtics tem 2 outpus, sendo o primeiro para o CosmosDB (cosmosdb-tesserato-fraud) e o segundo para o Azure Synapse Analytics


## CosmosDB
* CosmosDB (cosmosdb-tesserato-fraud) criado com 7 constainers diferentes (precisamos de todos?) + um databse (Fraud)
    * Benford-First-Digit
    * Benford-Second-Digit
    * Categories
    * Customers
    * leases (Azure Functions Change Feed)
    * Orders
    * Transactions

## CosmosDB Gremlin API Graph
    
* Criado com um banco de dados (frauddetectiondb)
* Um container (fraudring)

## Azure Functios 

* Todas já estão no repositório, apenas documentar certinho o momento em que vamos provisionar cada uma delas 




















