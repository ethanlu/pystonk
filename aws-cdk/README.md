Navigate to the `aws-cdk` directory.

```
$ cd aws-cdk
```

Create the virtualenv.

```
$ python3 -m venv .venv
```

Activate the virtualenv.

```
$ source .venv/bin/activate
```

Install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

Configure the AWS profile.

```
$ aws configure --profile [profile-name]
```

Update environment variables in `aws-cdk/pystonk-stack.py`.

To deploy the stack, run the following command.

```
$ cdk --profile [profile-name] deploy
```
