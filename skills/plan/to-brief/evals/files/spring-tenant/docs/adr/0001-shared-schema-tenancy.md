# 1. Shared schema with tenant_id column

Status: accepted

All tenants share one schema; every business table carries `tenant_id`. Isolation is enforced in the service layer, not by separate databases.
