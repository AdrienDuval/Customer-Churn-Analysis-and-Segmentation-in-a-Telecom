# Data Science Project  
## Customer Churn Analysis and Segmentation in a Telecom / SaaS Context

---

## 1. Context and Business Background

Telecom and SaaS companies operate on a **subscription-based business model**, where recurring revenue depends on customers staying over time.

When a customer leaves the company (a phenomenon known as **customer churn**):
- future recurring revenue is lost,
- customer acquisition costs are wasted,
- operational and marketing costs increase.

Reducing churn is therefore a **major business priority**, as retaining existing customers is significantly cheaper than acquiring new ones.

This project addresses this challenge using data science techniques to:
1. **Understand different types of customers**, and  
2. **Predict which customers are likely to leave**, so that preventive actions can be taken.

---

## 2. Problem Statement

The project is structured around the following key business questions:

> **How can a Telecom / SaaS company better understand its customers and predict churn in order to reduce revenue loss and improve retention strategies?**

This problem is approached from two complementary angles:
- **Unsupervised learning** to identify natural customer segments,
- **Supervised learning** to predict customer churn.

---

## 3. Dataset Description

### 3.1 Dataset Overview

The dataset used is the **Telco Customer Churn dataset**, which contains information about customers of a Telecom/SaaS company.

Key characteristics:
- **7,043 customers**
- **33 variables**
- Mix of **categorical and numerical features**
- Clear churn indicators

Each row represents one customer, with attributes related to:
- demographic information,
- subscription and contract details,
- service usage,
- billing and payment behavior,
- churn outcome.

---

### 3.2 Key Variables

- **Customer information**: Gender, Age, Senior Citizen, Partner, Dependents  
- **Subscription & contract**: Tenure Months, Contract Type, Payment Method  
- **Services**: Internet Service, Streaming, Tech Support, Online Security, etc.  
- **Billing & value**: Monthly Charges, Total Charges, CLTV  
- **Churn indicators**: Churn Label, Churn Value  

---

### 3.3 Target Variable

For supervised learning, the target variable is:

- **Churn Value**  
  - `1` → Customer churned  
  - `0` → Customer stayed  

This binary variable allows a clear classification task.

---

## 4. Exploratory Data Analysis (EDA)

The EDA phase aims to understand the dataset before modeling.

Key steps include:
- data structure and data types analysis,
- missing value detection and handling,
- distribution analysis of numerical variables,
- churn rate analysis,
- relationship analysis between features and churn.

EDA allows us to identify:
- important churn drivers,
- class imbalance,
- outliers and data quality issues,
- meaningful patterns for modeling.

---

## 5. Unsupervised Learning: Customer Segmentation

### 5.1 Objective

The goal of the unsupervised analysis is **not to predict churn**, but to answer:

> **What types of customers does the company have?**

Customer segmentation helps the business understand:
- different behavior profiles,
- value differences between customers,
- which segments require specific strategies.

---

### 5.2 Variables Used

Only **behavioral, usage, and value-related variables** are used.

Examples:
- Tenure Months  
- Monthly Charges  
- Total Charges  
- Number of subscribed services (engineered feature)  
- Contract Type  
- Payment Method  
- CLTV  

All churn-related variables are **excluded** to avoid bias.

---

### 5.3 Methods

- Data scaling (standardization)
- Dimensionality reduction (PCA) for visualization
- Clustering algorithms (e.g., K-Means)

---

### 5.4 Expected Outcomes

The clustering process may reveal segments such as:
- long-term loyal customers,
- high-value but dissatisfied customers,
- low-usage, high-risk customers,
- new customers with uncertain behavior.

---

### 5.5 Business Value of Segmentation

Customer segmentation allows the company to:
- design targeted retention strategies,
- prioritize high-value customers,
- allocate marketing and support resources efficiently,
- avoid one-size-fits-all retention campaigns.

---

## 6. Supervised Learning: Churn Prediction

### 6.1 Objective

The supervised learning task aims to answer:

> **Which customers are likely to churn in the near future?**

This enables proactive intervention before the customer leaves.

---

### 6.2 Features Used

Only variables **available before churn occurs** are used to avoid data leakage.

Categories of features:
- customer profile (age, family status),
- contract characteristics,
- service usage,
- billing and payment behavior.

Excluded variables:
- Churn Reason,
- Churn Score,
- Customer ID.

---

### 6.3 Modeling Approach

- Train-test split
- Models such as:
  - Logistic Regression
  - Random Forest
- Evaluation using:
  - Accuracy
  - Recall (important to detect churners)
  - ROC-AUC

---

### 6.4 Model Output

The model produces:
- a churn prediction (yes / no),
- or a churn probability score for each customer.

---

## 7. Business Implications

The results of this project can be directly translated into business actions:

- proactive retention campaigns for high-risk customers,
- personalized offers based on customer segment,
- optimized customer support prioritization,
- reduction of unnecessary discounts to low-risk customers.

Ultimately, this leads to:
- lower churn rate,
- higher customer lifetime value,
- improved profitability.

---

## 8. Project Value and Conclusion

This project demonstrates a **complete data science workflow**:
- business understanding,
- data exploration,
- unsupervised learning for insight generation,
- supervised learning for prediction,
- business-oriented interpretation.

It reflects a **real-world use case** commonly encountered in Telecom and SaaS companies and shows how data science can support strategic decision-making.

---

## 9. Limitations and Future Improvements

- The dataset is not time-series based, limiting temporal churn prediction.
- Future work could include:
  - survival analysis,
  - cost-sensitive modeling,
  - integration of customer interaction logs.

---

## 10. Final Summary

> This project uses customer data to segment users, predict churn, and provide actionable insights that help a Telecom/SaaS company reduce revenue loss and improve customer retention through data-driven decisions.
