# SplitSmartBot - Chat, Split and Enjoy

## What is SplitSmartBot
SplitSmartBot is a conversational chatbot based on [SplitWise](https://www.splitwise.com/) application. Splitwise is a free tool for friends and roommates to track bills and other shared expenses, so that everyone gets paid back. Bot built using AWS Lex and other services and is deployed on Facebook messenger.

## Features and use cases
SplitSmartBot chatbot is based on [AWS Lex](https://aws.amazon.com/lex) service. It supports following use cases.

1. Invite Friend to your account.
2. Create a group and add friends
    - e.g. Create expense group called 'Vegas Trip' with friends Bob and Alice
3. Add a new expense to the  group
    - e.g 500 INR for Accommodation by Alice
4. Show balance with a Friend
    - E.g. Alice owes you INR 100,  You owe Bob INR 50
5. Show balances for a group
    - E.g. In VegasTrip group,  Alice owes Bob INR 100, Rita owes Alice INR 200


## How to install

Bot is deployed on Facebook messenger. All you need is a Facebook messenger. No additional installtion steps are required.
You can use the bot from broswer, phone ( android, IOS) and tablets. ( Thanks to awesome integration support by AWS Lex for Facebook platform)

## Testing instructions

> **Note**: Currently SplitSmartBot is not publicly available. As per Hackathon guidelines, we have given tester role to Facebook ID: stef.devpost.1

You also need SplitWise account. Please use following account. 

#### SplitWise test account
```
2. SplitWise: 
    - username : user1.splitsmartbot@yahoo.com
    - password : awslex2017
```

> **IMPORTANT**:  If you are using the bot for the **first time**, You need to authorize the bot to access your splitwise account.

#### Access SplitSmartBot

1. From browser:
    - Go to link : [https://m.me/splitsmartbot](https://m.me/splitsmartbot)
    - login using test Facebook account

2. From Facebook messenger application on mobile or table
    - Open Facebook messenger
    - In Search Tab,  type @splitsmartbot and press enter

3. Visit this Facebook page:  https://www.facebook.com/splitsmartbot/  


## Architecture

SplitSmartBot is built using following AWS, python and Serverless Framework.

A] AWS Services
   1. Lex
   2. Lambda
   3. Dynamodb
   4. API Gateway
   5. Cloud Watch monitoring and logs
   6. S3 for hosting lambda code.

B] SplitWise API : [API](http://dev.splitwise.com/)     

C] Programming Language:  Python 2.7

D] Tools/Frameworks: [Serverless Framework](https://serverless.com/)

E] Architecture Diagram:

![splitbot architecture](https://s3.amazonaws.com/splitsmartbot-2017/splitsmart-diag.png)
