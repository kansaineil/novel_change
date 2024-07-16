Clone repo

	git clone -v --recurse-submodules --progress "https://github.com/kansaineil/novel_change" 

Fetch all

	git.exe -c fetch.parallel=0 -c submodule.fetchJobs=0 fetch --progress "--all"

List local and remotes branches 

	git branch -a

Checkout  remote branch

	git.exe checkout -B "user/dev" "origin/user/dev"