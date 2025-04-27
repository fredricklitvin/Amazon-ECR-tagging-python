
#used to work with aws
import boto3
#used to have a more interactive application
import questionary
from botocore.exceptions import ClientError

client = boto3.client('ecr')
iam_client = boto3.client('iam')

#list all the repositories
def list_repositories(print_repositories = False):
    i = 0
    ecr_repositories = []
    ecr_responses = client.describe_repositories()
    while i < len(ecr_responses['repositories']):
        # print(ecr_responses['repositories'][i]['repositoryName'])
        ecr_repositories.append(ecr_responses['repositories'][i]['repositoryName'])
        i +=1
    if not print_repositories:
        return ecr_repositories
    else:
        for ecr_repository in ecr_repositories:
            print(ecr_repository)

#choose whether to create a new repository or delete an existing one
def manage_repositories():
    manage_menu = questionary.select(
        "Choose action:",
        choices=['Create a repository ', 'Delete a repository', 'Exit']
    ).ask()
    if manage_menu == 'Create a repository ':
        create_repositories()
    elif manage_menu == 'Delete a repository':
        delete_repositories()
    else:
        return

#create a new repository
def create_repositories():
    try:
        #get the needed vars from the user
        repository_name = input("Please write your repository name: \n (The repository name must start with a letter and can only contain lowercase letters, numbers, hyphens, underscores, and forward slashes.) \n")
        scan_image = questionary.select(
            "Please choose whether to scan the images you upload:",
            choices=['Yes', 'No']
        ).ask()
        scan_image = True if scan_image == 'Yes' else False

        #create the new repository
        response_create_repository = client.create_repository(
        repositoryName = repository_name,
        tags = [
            {
                'Key': 'Owner',
                'Value': user_name
            }],
            imageScanningConfiguration = {
            'scanOnPush': scan_image})
        print("New repository was created:",response_create_repository['repository']['repositoryName'] )

    except client.exceptions.RepositoryAlreadyExistsException:
        print(" Error: A repository with that name already exists.")

    except client.exceptions.InvalidParameterException:
        print(" Error: Invalid parameters provided. Please double-check the repository name or other settings.")

    except ClientError as e:
        print(f" ClientError: {e.response['Error']['Message']}")

    except Exception as e:
        print(f" An unexpected error occurred: {str(e)}")

#delete a repository
def delete_repositories():
    try:
        repositories_list = list_repositories(print_repositories = False)
        repository_deletion = questionary.select(
            "Choose a repository for deletion:",
            choices=repositories_list
        ).ask()
        response_deleted_repository = client.delete_repository(
            repositoryName=repository_deletion,
            force=False
        )
        print("Repository was deleted successfully: ",response_deleted_repository['repository']['repositoryName'])

    except client.exceptions.RepositoryNotEmptyException:
        force_delete = questionary.select(
            "Repository is not empty, do you want to force delete?:",
            choices=['Yes', 'No']
        ).ask()
        scan_image = True if force_delete == 'Yes' else False
        if scan_image:
            response_deleted_repository = client.delete_repository(
                repositoryName=repository_deletion,
                force=True
            )
        else:
            print("No repository was deleted because it is not empty")

    except ClientError as e:
        print(f" ClientError: {e.response['Error']['Message']}")

    except Exception as e:
        print(f" An unexpected error occurred: {str(e)}")

#makes sure the program doesn't stop until being told
exit_menu = False

# get the username for tagging
response_user = iam_client.get_user()
user_name_split = response_user['User']['Arn'].split(':')
user_name = user_name_split[-1]

# the main menu where you decide what action to use
while not exit_menu:
    starting_menu = questionary.select(
        "Choose action:",
        choices=['List repositories','Manage repositories','Upload images','Exit']
    ).ask()

    if starting_menu == 'List repositories':
        list_repositories(True)
    elif starting_menu == 'Manage repositories':
        manage_repositories()
    else:
        print("Thanks for your time, have a nice day!")
        exit_menu = True