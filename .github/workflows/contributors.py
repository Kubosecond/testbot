name: Check New Contributors

on: pull_request:
    issues:
      types: [opened, reopened]

jobs:
  welcome:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v5
        with:
          script: |
            // Get a list of all issues created by the PR opener
            // See: https://octokit.github.io/rest.js/#pagination
            const creator = context.payload.sender.login
            const opts = github.rest.issues.listForRepo.endpoint.merge({
              ...context.issue,
              creator,
              state: 'all'
            })
            const issues = await github.paginate(opts)

            for (const issue of issues) {
              if (issue.number === context.issue.number) {
                continue
              }

              if (issue.pull_request) {
                return // Creator is already a contributor.
              }
            }

            await github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: 'Welcome, new contributor!'
            })
