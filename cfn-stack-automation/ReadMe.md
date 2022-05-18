## Requirement for this Lambda Function:

- The Infrastructure creation process was semi-automated. Although we had CFN templates to meet IaaC requirements, we had to manually upload `nestedstack` CFN template from the CFN Console and start the CFN Stack creation.
- This was a gap in our automation. I was tasked to come up with a solution to automate this gap. 
- I created a Lambda trigger for the S3 bucket so that whenever a `nestedstack.json` template is uploaded to the S3 bucket, a Lambda function would be triggered to create/update CFN stacks.


This python script is executed by a Lambda function to trigger CFN API calls.

The Lambda Function triggeres the CFN `Create_Stack` or `Update_Stack` API when a new `nestedstack.json` template is uploaded to the S3 Bucket. 

---

When this automation was implemented, the Lambda function was triggered everytime a `nestedstack.json` template was uploaded to the S3 bucket. 

The `handler.py` script checks if the Nested Stack tempate uploaded to the S3 bucket is creating a New CFN stack or updating an existing CFN Stack. 

The script also sends Email notifications to the team Email list and notifies about the CFN Stack creation or update. 

---

In order to avoid accidental CFN Stack creation or accidental CFN Stack update, the script creates a `Change Set` which needs to be reviewed and approved for the new stack creation or existing stack update to take effect. 



