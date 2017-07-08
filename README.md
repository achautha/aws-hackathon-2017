# SplitSmartBot - Chat, Split and Enjoy

## What is SplitSmartBot
SplitSmartBot is a conversationsational chatbot based on [SplitWise](https://www.splitwise.com/) application. Splitwise is a free tool for friends and roommates to track bills and other shared expenses, so that everyone gets paid back. Bot is deployed on Facebook messenger.

## Features and use cases
SplitSmartBot chatbot is based on [AWS Lex](https://aws.amazon.com/lex) service. It supports following use cases.

1. Create an expense group and add friends
    - e.g. Create expense group called 'Vegas Trip' with friends Bob and Alice
2. Add a new expense to the  group
    - e.g 500 INR for Accommodation by Alice
3. Show pending expenses with a Friend
    - E.g. Alice owes you INR 100,  You owe Bob INR 50
4. Show pending expenses for a Group
    - E.g. In VegasTrip group,  Alice owes Bob INR 100, Rita owes Alice INR 200


## How to install

Bot is deployed on Facebook messenger. All you need is a Facebook messenger. No additional installtion steps are required.
You can use the bot from broswer, phone ( android, IOS) and tablets. ( Thanks to awesome integration support by AWS Lex support for Facebook platform)

## How to use

> **Note**: Currently SplitSmartBot is not publicly available. You have to use **Test Facebook account** mentioned below.

#### Test accounts
```
1. Facebook
    - username : user1.splitsmartbot@yahoo.com
    - password : awslex2017

2. SplitWise
    - username : user1.splitsmartbot@yahoo.com
    - password : awslex2017
```

> **IMPORTANT**:  If you are using the bot for the **first time**, You need to authorize it to access your splitwise account or test SplitWise account metntioned above.

#### Access SplitSmartBot

1. From browser:
    - Go to link : [https://m.me/splitsmartbot](https://m.me/splitsmartbot)
    - login using test Facebook account

2. From Facebook messenger application on mobile or table
    - Open Facebook messenger
    - In Search Tab,  type @splitsmartbot and press enter


## Architecture

SplitSmartBot is built using following AWS, python and Serverless Framework.

A] AWS Services
   1. Lex
   2. Lambda
   3. Dynamodb
   4. API Gateway
   5. Cloud Watch monitoring and logs

B] Programming Language:  Python 2.7

C] Tools/Frameworks: [Serverless Framework](https://serverless.com/)

D] Architecture Diagram:

![splitbot architecture](https://s3.amazonaws.com/splitsmartbot-2017/splitsmart-diag.png)


## Short Demos

### 1. First time login and Greetings

![](https://s3.amazonaws.com/splitsmartbot-2017/get-expenses.mov)

### 2. Get all my pending expenses
=======
![splitbot architecture](/demo/splitsmart-diag.png)
