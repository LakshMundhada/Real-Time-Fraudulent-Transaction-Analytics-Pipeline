# Real Time Credit Card Fraud Transaction Analytics Pipeline

## Overview

The Real Time Credit Card Fraud Transaction Analytics Pipeline is a comprehensive solution designed to detect fraudulent transactions in real-time by analyzing both historical and streaming transaction data. This project utilizes various AWS services and open-source technologies to process, analyze, visualize, and monitor credit card transactions efficiently.

## Key Components

### Data Sources
- **Historical Data**: Stored in S3, comprising over 8 million rows of transactional data.
- **Streaming Data**: Streamed through Confluent Kafka, representing real-time credit card transactions.

### Technologies Used
- **Apache Spark**: Processes and analyzes streaming and historical transaction data.
- **AWS S3**: Stores analyzed data and serves as a data source for AWS Glue.
- **AWS Glue**: Used for crawling data, cataloging schemas, and preparing data for analysis.
- **Athena**: Enables ad-hoc querying of data stored in S3 via the Glue Data Catalog.
- **Tableau**: Visualizes insights derived from the analyzed data, facilitating interactive exploration.
- **AWS CloudFormation**: Automates the deployment and management of AWS resources.
- **GitActions**: Facilitates continuous integration and deployment processes.

## Workflow

1. **Data Ingestion**: Historical transactional data is fetched from S3, while real-time transaction streams are obtained from Confluent Kafka.
2. **Data Processing**: Apache Spark applies predefined rules to analyze the streaming data against historical transactions.
3. **Data Storage**: Analyzed data, including both genuine and fraudulent transactions, is stored in an AWS S3 bucket.
4. **Schema Management**: AWS Glue crawls the data, cataloging schemas and making them available in the Glue Data Catalog.
5. **Ad-Hoc Queries**: Athena allows users to run ad-hoc queries against the data stored in S3, leveraging the Glue Data Catalog for schema information.
6. **Visualization**: Tableau connects to Athena using the ODBC Athena connector, enabling real-time visualization of transactional insights.
7. **Automation and Deployment**: The entire pipeline, including infrastructure provisioning and deployment, is automated using AWS CloudFormation and GitActions.

## Conclusion

The Real Time Credit Card Fraud Transaction Analytics Pipeline provides a scalable, efficient, and automated solution for detecting fraudulent transactions in real-time. By leveraging the power of AWS services and open-source technologies, the pipeline offers robust data processing, analysis, visualization, and monitoring capabilities, empowering organizations to safeguard against financial fraud effectively.
