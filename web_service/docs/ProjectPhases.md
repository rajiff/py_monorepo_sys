# Project Phases
- No cannot be built overnight, it evolves in iterations
- This document defines scope for planned iterations 
- specifies which iteration is currently in focus for AI agents to focus on

Current Focus - **Iteration-001**

## Iteration-001
- Bootstrap the project and set up the project structure for backend development
- Develop FastAPI based backend with connectivity to PostgreSQL database using SQLAlchemy ORM or as relevant to FastAPI
- API request processing is done in multi-tenant capable way
    - i.e., Per tenant a specific database connection, user authentication is done before processing the API request and tenant specific data is fetched for processing and response is returned
- User requests across tenants or client connections is handled by the system, i.e., concurrent requests are spread across multiple tenants


### Deliverables
- Working code is securely available in Git repo
- Relevant markdown file like "HowToRun.md" has documented and steps from it is veriable and found to run the app 

### Scope

### Done criteria of Iteration-001
- [ ] Deliverables are available to verify
- [ ] Scoped functionality is working, verifiable by test cases
- [ ] Functionality is reviewed and review comments are addressed, improvements for next iteration noted
- [ ] Code is committed, repository is tagged for the phase