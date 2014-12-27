read -p "Enter commit message for CALLIOPE changes:" calliope_commit_msg
git add .
git commit -m "$calliope_commit_msg"
git pull --rebase
git push