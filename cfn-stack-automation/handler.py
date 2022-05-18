import json
import random
import boto3
import botocore

## --- Variables for SDK calls  
client = boto3.client('cloudformation')
email = boto3.client('ses',region_name='us-west-2')
s3 = boto3.client('s3')

## --- Function to create New Stack
def cf_new_stack(stack_name,template):

    ## --- Try block to create New Stack with DBPassword parameter.
    try:
        ## --- Code snippet to generate random password for RDS
        s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#%^*()?"
        passlen = 20
        DBPassword =  "".join(random.sample(s,passlen))

        ## --- SDK API call to create change set for New Stack. If Stack already exists, ChangeSetType CREATE will fail and throw exception.
        response = client.create_change_set(
        StackName=stack_name,
        TemplateURL='https://<bucket_name>.s3-us-west-1.amazonaws.com/Environments/'+stack_name+'/'+template,
        Parameters=[
        {
            'ParameterKey': 'DBPassword',
            'ParameterValue': DBPassword
        },],            
        Capabilities=
        [
            'CAPABILITY_IAM',
        ],
        ChangeSetName=stack_name,
        ChangeSetType='CREATE')
        print("New Stack Will be Created")

        ## --- Push RDS password to S3 bucket.
        s3.put_object(Bucket='cwdskeys', Key='rds-password/'+stack_name+'-RDS_Password.txt', Body=DBPassword)
        print("Password generated and sent to s3")

        ## --- call email function with set_type = NEW.
        cf_email_notify('NEW',stack_name)

    ## --- Code for templates that do not need DBPassword parameter to be set.
    except botocore.exceptions.ClientError as ex:
        print(ex)

        ## --- Check for errors in Template
        if 'Template error' in str(ex):
            print(ex)
            cf_email_notify(str(ex),stack_name)
            exit(0)
                
        ## --- SDK API call to create change set for New Stack
        response = client.create_change_set(
        StackName=stack_name,
        TemplateURL='https://<bucket_name>.s3-us-west-1.amazonaws.com/Environments/'+stack_name+'/'+template,            
        Capabilities=
        [
            'CAPABILITY_IAM',
        ],
        ChangeSetName=stack_name,
        ChangeSetType='CREATE')
        print("Stack does not need Parameters\nNew Stack will be created: "+stack_name)

        ## --- call email function with set_type = NEW_nonDB.
        cf_email_notify('NEW_nonDB',stack_name)        

    return response

## --- Function to update Existing Stack.
def cf_old_stack(stack_name, template):

    ## Try block for updates to Existing Stack with old parameter values
    try:
        response = client.create_change_set(
        StackName=stack_name,
        TemplateURL='https://<bucket_name>.s3-us-west-1.amazonaws.com/Environments/'+stack_name+'/'+template,
        Parameters=[
        {
            'ParameterKey': 'DBPassword',
            'UsePreviousValue': True
        },],
        Capabilities=
        [
            'CAPABILITY_IAM',
        ],
        ChangeSetName=stack_name,
        ChangeSetType='UPDATE')

        ## --- call email function with set_type = OLD.
        cf_email_notify('OLD',stack_name)

    ## --- Code for templates that do not need RDS password to be set.
    except botocore.exceptions.ClientError as ex:
        print(ex)

        ## --- Check for errors in Template
        if 'Template error' in str(ex):
            print(ex)
            cf_email_notify(str(ex),stack_name)
            exit(0)
                
        response = client.create_change_set(
        StackName=stack_name,
        TemplateURL='https://<bucket_name>.s3-us-west-1.amazonaws.com/Environments/'+stack_name+'/'+template,
        Capabilities=
        [
            'CAPABILITY_IAM',
        ],
        ChangeSetName=stack_name,
        ChangeSetType='UPDATE')

        ## --- call email function with set_type = OLD.
        cf_email_notify('OLD',stack_name)        

    return response

## --- Function to send Email Notifications about Stack Status
def cf_email_notify(set_type, stack_name):
    if set_type == 'NEW':
        
        ## --- Get temporary pre-signed URL to the RDS password file.
        url = s3.generate_presigned_url('get_object',
        Params={'Bucket': '<bucket_name>','Key': 'rds-password/'+stack_name+'-RDS_Password.txt'},
        ExpiresIn=600)

        ## --- API call to send Email notification for change set created for New Stack
        notify = email.send_email(
        Destination=
        {
            'ToAddresses': ["CWDSDevOpsEngineering@osi.ca.gov"]
        },
        Message=
        {
            'Body': 
            {
                'Html': 
                {
                    'Charset': 'UTF-8',
                    'Data': '<h3>Change set created for <font color="red">New Stack</font> '+stack_name+'</h3><hr>RDS Password file in S3: <a href='+url+'>'+stack_name+'-RDS Password</a><br>This link will be invalid after 10 minutes'
                },
            },
            'Subject': 
            {
                'Charset': 'UTF-8',
                'Data': 'Lambda CF Notification',
            },
        },
        Source='<email_list>')
        print("RDS Password sent to CWDS DevOps Email list")

    elif set_type == 'NEW_nonDB':
        ## --- API call to send Email notification for change set created for New Stack without DBPassword Parameter
        notify = email.send_email(
        Destination=
        {
            'ToAddresses': ["<email_list>"]
        },
        Message=
        {
            'Body': 
            {
                'Html': 
                {
                    'Charset': 'UTF-8',
                    'Data': '<h3>Change set created for <font color="red">New Stack</font> '+stack_name+'</h3><hr>This Stack does not need DBPassword Parameter.'
                },
            },
            'Subject': 
            {
                'Charset': 'UTF-8',
                'Data': 'Lambda CF Notification',
            },
        },
        Source='<email_list>')    

    elif set_type == 'OLD':
        ## --- API call to send Email notification for change set created for Existing Stack        
        notify = email.send_email(
        Destination=
        {
            'ToAddresses': ["<email_list>"]
        },
        Message=
        {
            'Body': 
            {
                'Html': 
                {
                    'Charset': 'UTF-8',
                    'Data': '<h3>Change set created for <font color="red">Existing Stack</font> '+stack_name+'</h3>'
                },
            },
            'Subject': 
            {
                'Charset': 'UTF-8',
                'Data': 'Lambda CF Notification',
            },
        },
        Source='<email_list>')

    else:
        ## --- API call to send Email notification for errors in Template
        notify = email.send_email(
        Destination=
        {
            'ToAddresses': ["<email_list>"]
        },
        Message=
        {
            'Body': 
            {
                'Html': 
                {
                    'Charset': 'UTF-8',
                    'Data': '<h3>Error in Template uploaded for <font color="red">Stack Name: </font> '+stack_name+'</h3><hr>Error: '+set_type
                },
            },
            'Subject': 
            {
                'Charset': 'UTF-8',
                'Data': 'Lambda CF Notification',
            },
        },
        Source='<email_list>')

    return notify

## --- Actual Lambda function to invoke on template uploads to cwds-cloudformation s3 bucket.
def lambda_cf(event, context):

    print("S3 Generated Event:")
    print(event)

    ## --- Parse the s3 event to get stack-name and CF-template name
    stack_name = event["Records"][0]["s3"]["object"]["key"].split('/')[1]
    template = event["Records"][0]["s3"]["object"]["key"].split('/')[2]

    ## -- Verify if the template is a Nestedstack template    
    if 'nestedstack' in template:
        path = event["Records"][0]["s3"]["object"]["key"]
        print("Nestedstack Detected")
        print("Nestedstack Path: ", path, "\nStack Name: ",stack_name, "\nTemplate to use: ", template)

        try:
            print("Calling New Stack Create Function")
            cf_new_stack(stack_name,template)

        ## --- catch exceptions block:
        except botocore.exceptions.ClientError as ex:
            print(ex)
            print("Calling Existing Stack Update Function")
            cf_old_stack(stack_name,template)
            print("Existing Stack will be updated")
            print("Nestedstack Path: ", path)

    else:
        print("Template uploaded is not a NestedStack template. Cannot proceed.")
                


