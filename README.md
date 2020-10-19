# !!! Use of git
!!! TIP: ${} is a placeholder (replace it with your input)
1. create in local (your computer) your own branch from a reference branch (ex. main)
    git checkout -b ${NAME OF THE NEW BRANCH}
2. every time before starting to working on the code, pull the lastest changes of the project in Github
    git pull origin main
3. work on the code
4. once finished, stage your modifications (so that they are ready to be committed)
    git add -A
5. commit your modifications
    git commit -m "${the commit message}"
6. push the modifications to your own remote branch (the branch with the same name but in Github)
    git push origin ${NAME OF THE BRANCH}
7. after step 6, normally you will be asked if you want to do a pull request (i.e. merge request)
you can choose to merge your remote branch with the branch 'main' so that others can pull your changes.
Otherwise you can continue to work on the code, make commits, and make a pull request later.

!!! TIP: push your modifications frequently to your remote branch, so that it will be eaiser to be recovered in the case of a computer failure

# AFDA
AFDA (Airline Flight Data Analysis) is a tool for high-volume flight data analysis 
This tool is part of the student project "Machine Learning to explore the the flight data ADS-B" at ISAE-SUPAERO.
baptiste just modified the file
