# Prepare
## Register an account
It is suggested to register a new account (using your friends name, and family members name and creating a empty ds160.) One reason is if it get banned temporarily, it does not affect your real account. Another reason is the script needs the account to be in the "Pay fee mode", so **if you have an account that has already paid the fee, you cannot use it**.

You need to put your email address and password in line 20 and line 21.

## Slack message
By default, running this script will send a notification to my slack, so that this script can help more people in the wechat group. You can disable it by comment out line 126 in find_visa_spot_.py.

## Register twilio account
With a twilio account, you can get a phone call to yourself when there is a good spot. You dont need to pay anything because the trial account is enough.

You'll have to setup a [Twilio](www.twilio.com) account [here](https://www.twilio.com/try-twilio). You'll need to get (a) a phone number, (b) your [account SID](https://www.twilio.com/docs/glossary/what-is-a-sid) and (c) your [authentification token](https://www.twilio.com/docs/iam/access-tokens). Some detail [here](https://www.twilio.com/docs/iam/api/account).

After getting setup the account and get the sid and token, you can fill in the blanks in the function at line 109.

Note that, when you get a phone call, don't answer it. If you answer, you will use your trial credit.

## Change sleeping time.
The current setup is to sleep for ranodmly between 15 mins to 25 mins. 

# Run it.

## Run a chromedriver with docker.
(There is probably other way, but this is very simple.)
```
docker run -d -p 4444:4444 --shm-size="2g" --name chrome selenium/standalone-chrome:4.1.3-20220405
```


This is used to simulate you logging into the account.

## Run the spot finder.

```
python find_visa_spot_.py
```

If you see something like:
```
[['Toronto', (2023, 5, 18)], ['Vancouver', (2023, 6, 28)], ['Calgary', (0, 0, 0)], ['Halifax', (0, 0, 0)], ['Montreal', (0, 0, 0)], ['Ottawa', (0, 0, 0)], ['Quebec City', (0, 0, 0)]]. %2022-05-13 01:18:55
```

Then it should be right.

If you stuck at "Choose Node", then the chromedriver has some problem. You may need to restart the docker container:

```
docker stop chrome;docker rm chrome;docker run -d -p 4444:4444 --shm-size="2g" --name chrome selenium/standalone-chrome:4.1.3-20220405
```

