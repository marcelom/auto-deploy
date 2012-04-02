settings = (
    {
        'repo_name': 'aaa.github.com',
        'repo_url': 'git@github.com:aaa/aaa.github.com.git',

        'deploy_type': 's3',

        'aws_key_id': 'your aws key id',
        'aws_key': 'your aws key content',
        's3_bucket': 'your s3 bucket name',
    },

    {
        'repo_name': 'bbb',
        'repo_url': 'git@github.com:bbb/bbb.git',

        'deploy_type': 'ssh',

        'ssh_address': 'bbb.domainname.com',
        'ssh_username': 'username',
        'ssh_password': 'password',
        'base_folder': 'public_html',
    }
)
