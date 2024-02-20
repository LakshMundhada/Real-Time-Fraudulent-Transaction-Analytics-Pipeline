# Real-Time Credit Card Fraud Transaction Analytics Pipeline

## Overview

The Real-Time Credit Card Fraud Transaction Analytics Pipeline is a comprehensive solution designed to detect real-time fraudulent transactions by analysing historical and streaming transaction data. This project utilizes various AWS services and open-source technologies to efficiently process, analyze, visualize, and monitor credit card transactions.

## Description

This project integrates historical data stored in Amazon S3 with streaming data sourced from Confluent Kafka using Apache Spark. Leveraging Spark's powerful processing capabilities, the system applies predefined conditions to distinguish between fraudulent and genuine transactions in real time. The processed data is then written back to S3 for storage.

To enable seamless data exploration and visualization, the project utilizes AWS Athena for SQL-based queries on the stored data. Furthermore, the insights gained from the processed data are visualized using Tableau, and connected to the data source through a specialized connector.

To streamline the workflow and ensure reproducibility, the entire pipeline is automated using GitHub Actions, with infrastructure provisioning handled by CloudFormation templates (CFT). This end-to-end solution offers a robust, scalable, and automated framework for real-time fraud detection and actionable insights, enhancing decision-making processes.


## Key Components

### Data Sources
- **Historical Data**: Stored in S3, comprising over 8 million rows of transactional data.
- **Streaming Data**: Streamed through Confluent Kafka, representing real-time credit card transactions.

### Technologies Used
- **AWS RDS**: Database for storing unique customer information securely.
- **Apache Spark**: Processes and analyzes streaming and historical transaction data.
- **AWS S3**: Stores analyzed data and serves as a data source for AWS Glue.
- **AWS Crawler**: Used for crawling data, cataloguing schemas, and preparing data for analysis.
- **Athena**: Enables ad-hoc querying of data stored in S3 via the Glue Data Catalog.
- **Tableau**: Visualizes insights derived from the analyzed data, facilitating interactive exploration.
- **AWS CloudFormation**: Automates the deployment and management of AWS resources.
- **GitActions**: Facilitates continuous integration and deployment processes.

## Workflow

1. **Data Ingestion**: Historical transactional data is fetched from S3, while real-time transaction streams are obtained from Confluent Kafka.
2. **Data Processing**: Apache Spark applies predefined rules to analyze the streaming data against historical transactions.
3. **Data Storage**: Analyzed data, including both genuine and fraudulent transactions, is stored in an AWS S3 bucket.
4. **Schema Management**: AWS Glue crawls the data, cataloguing schemas and making them available in the Glue Data Catalog.
5. **Ad-Hoc Queries**: Athena allows users to run ad-hoc queries against the data stored in S3, leveraging the Glue Data Catalog for schema information.
6. **Visualization**: Tableau connects to Athena using the ODBC Athena connector, enabling real-time visualization of transactional insights.
7. **Automation and Deployment**: The entire pipeline, including infrastructure provisioning and deployment, is automated using AWS CloudFormation and GitActions.

# Architecture
![Architecture Diagram](https://github.com/LakshMundhada/Real-Time-Fraudulent-Transaction-Analytics-Pipeline/assets/150781667/a0357a50-42e4-4a2f-96b9-006df45aae39)

# Deployment Steps

Set up IAM roles with appropriate permissions for accessing AWS services like S3, Glue, Athena, and CloudFormation.

## Step 1: Prepare Data Sources

- Ensure historical transactional data is stored in S3 and streaming data is available through Confluent Kafka.
- Set up MySQL RDBMS for storing historical transaction data if not already available.

## Step 2: Configure AWS Services

- Set up an S3 bucket to store analyzed data.
- Configure Confluent Kafka for streaming data ingestion.
- Set up AWS Glue to crawl data, catalog schemas, and prepare data for analysis.
- Configure Athena for ad-hoc querying of data stored in S3 via the Glue Data Catalog.

## Step 3: Develop and Test Apache Spark Application

- Develop Apache Spark application to process streaming and historical transaction data.
- Test the application locally to ensure proper functionality and accuracy of fraud detection algorithms.

## Step 4: Set Up Tableau for Visualization

- Install and configure Tableau Server or Tableau Online.
- Connect Tableau to Athena using the ODBC Athena connector for real-time visualization of transactional insights.

## Step 5: Automate Deployment with AWS CloudFormation and GitActions

- Create CloudFormation templates to provision and manage AWS resources required for the pipeline.
- Set up GitActions for continuous integration and deployment.
- Define deployment workflows in GitActions to automate the deployment process.

## Step 6: Deploy and Monitor Pipeline

- Deploy the Real Time Credit Card Fraud Transaction Analytics Pipeline using CloudFormation.
- Monitor the pipeline for performance, scalability, and accuracy of fraud detection.
- Implement monitoring and logging mechanisms to track pipeline health and performance metrics.

## Conclusion

The Real Time Credit Card Fraud Transaction Analytics Pipeline provides a scalable, efficient, and automated solution for detecting fraudulent transactions in real-time. By leveraging the power of AWS services and open-source technologies, the pipeline offers robust data processing, analysis, visualization, and monitoring capabilities, empowering organizations to safeguard against financial fraud effectively.
