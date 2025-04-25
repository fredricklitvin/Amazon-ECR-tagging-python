
import boto3
import questionary

client = boto3.client('ecr')
iam_client = boto3.client('iam')

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

def manage_repositories():

    def create_repositories(repository_name = "", scan_image = False ):
        print("hi")
    manage_menu = questionary.select(
        "Choose action:",
        choices=['Create a repository ', 'Delete a repository', 'Exit']
    ).ask()
    if manage_menu == 'Create a repository ':
        repository_name = input("Please write your repository name: \n (The repository name must start with a letter and can only contain lowercase letters, numbers, hyphens, underscores, and forward slashes.) \n")







    elif manage_menu == 'Delete a repository':
        print("hi")
    else:
        return
# chosen_repo = questionary.select(
#     "Choose a repository:",
#     choices=ecr_repositories
# ).ask()
#
# image_tag = questionary.text("Enter the image tag (e.g. latest):").ask()
#
# region = questionary.select(
#     "Choose AWS region:",
#     choices=["us-east-1", "us-west-2"]
# ).ask()
#
# print(f"You selected: {repo}, tag: {image_tag}, region: {region}")


exit_menu = False
while not exit_menu:
    response_user = iam_client.get_user()
    print(response_user)

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