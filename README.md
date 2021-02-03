## Getting Started
These instructions will get you a copy of the project up and running on your Local Environment 
```
git clone www.github.com/kashishshah881/ipam
```

### Prerequisites

- Python3.7
- AWS Account
- AWS Cli setup
- Terraform v0.14
- Python virtualenv

### Setup

1. cd into the project directory
2. Run ``` pip install -r requirements.txt ```
3. Run ``` terraform init ```
4. Run ``` terraform apply --auto-approve```
5. Goto AWS Management Console and Setup Secrets Manager for DB credentials and copy the ARN. 
6. Paste the Fifo ARN and Secrets Manager arn in index.py at Line 16 and 17 and in input.py at Line 9
7. Run ``` python3 input.py ``` 
8. Run ``` streamlit run index.py ```

