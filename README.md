# Attendance

The bot follows a slightly different paradigm than most discord bots due to the constraints of AWS Lambda. This video here is a greater starter to this concept https://www.youtube.com/watch?v=BmtMr6Nmz9k

# Setup

Install Dependencies
`pip install -r requirements.txt`
`pip install -r requirements-dev.txt`

Create a Discord bot and note down its Public Key, Token and App ID. You can do this by going to the Discord Developer Portal and creating a new application.

Create `.env` file

```
APP_NAME=<The name of your Cloudformation App Stack. Make sure this is unique>

ID=<Discord App ID>
DISCORD_TOKEN=<Refresh the Discord Token in the Developer portal to obtain one>
DISCORD_PUBLIC_KEY=<The Public Key of the Discord app, can also be found in the portal>
```

# Registering and Deleting Commands

You can define a command in the `discord_commands.yaml` file

```
- name: Command Name
  description: Command Description
  options:
    - name: Parameter 1
      description: Parameter 2 Description
      type: 3 # string
      required: true
    - name: Parameter 2
      description: Parameter 2 Description
      type: 3 # string
      required: true
```

Add commands to the discord through the following command. Previous commands that were registered before but are not in the file anymore will be deleted.
`python commands/register_commands.py`

# Actually making the commands work

See the comments in the `src/app/main.py` file. 
You can define a command via adding extra cases to the match case statement.

# Deployment

You only need to run this command once
`cdk bootstrap`

After that you can just run this to deploy.
`cdk deploy`

After you run `cdk deploy` a Docker Container will be built out of the contents of the `src` directory. There is a `Dockerfile` there and a `requirements.txt` that you should modify to include any dependencies you need. The container will be built and uploaded to AWS ECR. The Lambda function will then be updated to use this container.

After running cdk deploy, you should see something similar to the following output
  
```
Outputs:
AttendanceBot.API{your APP_NAME}Endpoint254F1E81 = https://42ah7jjudh.execute-api.us-east-1.amazonaws.com/prod/
```

Set the URL as the interactions endpoint in the Discord Developer Portal.

When you look in the AWS Console, you should look for two things

1. A Lambda function with the name of your `APP_NAME` env variable
2. A DynamoDB table with the name `Table{APP_NAME}`

# CDK Basic Documentation

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
