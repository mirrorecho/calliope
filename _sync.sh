# change directory to calliope directory (directory containint the sync script)
cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

read -p "Enter commit message for CALLIOPE changes:" calliope_commit_msg
git add --all .
git commit -m "$calliope_commit_msg"
git pull --rebase
git push