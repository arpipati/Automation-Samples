### JSON Config updates

As part of the process to onboard internal teams to AWS Organizations, the on-call engineers had to add a number of accounts to the JSON Config. 

This process was not automated, because the tools we were using to onboard the teams was developed and managed by another team. Automation was a low priority for them.

Our team was spending time consuming and tedious manual effort for well over a year, and could not focus on a native automation solution due to capacity restrains and prioritization issues. 

### Semi-Auomation Approach

As I got comfortable and up-to-speed with the team responsibities, I began to feel bogged down by the amount of manual effort I had to spend to just update accounts to the JSON config. 

I started to think of possible automation solutions and began to explore JSON parsing approach. As I explored deeper, I could see a workable stop-gap arrangement that could work well for our use-case. It would reduce a number of manuel steps in the onboarding process. 

Eventually, I created a command line utility script that takes values for critical fields in the JSON as arguments and then generates a new JSON config with the requested account numbers updated in appropriate locations. 

This new JSON config is now ready to deploy.

### Working:

The following command uses the `--accounts` flag, which can be used if there are a handful of account numbers that need to be updated to the JSON Config:

```
ruby auto-create-sdc-json.rb --service-principal oranges.url.internal --filename test.json --accounts 838523055275,602292946641,206547593965 --service-access --ticket https://corp.ticket-queue.com/V879555748
```

The following command uses the `--accounts-file` flag, which should be used if there are a large number of account that need to be updated to the JSON Config:

```
ruby auto-create-sdc-json.rb --service-principal beta.url.internal --filename test.json --accounts-file accounts.txt --service-access --ticket https://issues.ticket-queue.com/issues/xyxz-11111
```

### Examples:

* The repository has a sample JSON Config file `test.json` which resembles the actual config. 
* The Ruby script `auto-create-sdc-json.rb` is the main file which contains the logic for the command and the usage. This script will parse the JSON and generate a new one.
* The `output.json` file is the sample output JSON file which is generated upon parsing the original JSON. This file will contain the new accounts that were requested to be updated in the appropriate location.

