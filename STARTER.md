# Portman case - starter package (remote)

1. Install Docker Desktop and Python 3.11 or newer. For Part D you also need k3d or kind, kubectl and helm;
   for Part E Node.js 20+ and Terraform.
2. Load the vendor image once: `docker load -i vendor/mock-lseg-image.tar`
3. In this folder run `docker compose up -d`. This starts:
   - TimescaleDB on localhost:5432 (database `portman`, user/password `portman_admin`, local test values only)
   - the mock vendor API on http://localhost:8080 (app key `portman-case-key`)
4. Check the vendor: `curl http://localhost:8080/v1/usage`

The case description (PDF) explains the assignment, the data and the vendor API. All data is synthetic.
Treat the vendor as an external service: use only its HTTP API.

Include in your submission the output of `GET /v1/usage` and the vendor's call log after one clean backfill
(`docker compose cp vendor:/state/calls.log .`).
