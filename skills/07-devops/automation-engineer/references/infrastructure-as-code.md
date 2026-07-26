# infrastructure-as-code

Reference documentation for the automation-engineer skill — Terraform, OpenTofu, Pulumi, AWS CDK, CDKTF, Bicep, Crossplane, state management, drift detection, cost estimation, policy as code, multi-cloud patterns, CI integration, and module publishing.

## Terraform

### Project structure

```
infra/
├── environments/
│   ├── production/
│   │   ├── main.tf          # provider + backend config
│   │   ├── variables.tf     # input variable declarations
│   │   ├── terraform.tfvars # concrete values for this environment
│   │   └── outputs.tf       # output declarations
│   └── staging/
│       ├── main.tf
│       ├── variables.tf
│       └── terraform.tfvars
├── modules/
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── versions.tf
│   ├── compute/
│   └── database/
└── global/                   # shared resources (DNS, CDN, IAM)
    ├── main.tf
    └── terraform.tfvars
```

### Remote state backends

**AWS S3 + DynamoDB (state locking):**
```hcl
# backend.tf in each environment
terraform {
  backend "s3" {
    bucket         = "myorg-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
    kms_key_id     = "alias/terraform-state"
  }
}
```
```hcl
# The DynamoDB table must exist beforehand — create once via bootstrap
resource "aws_dynamodb_table" "terraform_lock" {
  name         = "terraform-state-lock"
  hash_key     = "LockID"
  billing_mode = "PAY_PER_REQUEST"
  attribute { name = "LockID"; type = "S" }
}
```

**GCS (Google Cloud Storage):**
```hcl
terraform {
  backend "gcs" {
    bucket = "myorg-tf-state"
    prefix = "production"
  }
}
```

**AzureRM (Azure Storage Account):**
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "myorgtfstate"
    container_name       = "tfstate"
    key                  = "production.terraform.tfstate"
  }
}
```

**Terraform Cloud (HCP Terraform — managed):**
```hcl
terraform {
  cloud {
    organization = "myorg"
    workspaces {
      name = "production-aws"
    }
  }
}
```

### Workspaces vs directories

| Approach | Pros | Cons |
|----------|------|------|
| **Separate directories** (recommended) | Full isolation, different backends, independent state | More copy-paste, DRY violations if not modularized |
| **Terraform workspaces** (`terraform workspace`) | Single config, shared module code | Same backend, same credentials — risk of cross-env blast radius |

**Workspaces pattern (for small teams, same cloud account):**
```bash
terraform workspace new production
terraform workspace new staging
terraform workspace select production
terraform apply -var-file=production.tfvars
```

### Module design

```hcl
# modules/networking/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = merge(var.tags, { Name = "${var.name}-vpc" })
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnets[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]
}

output "vpc_id" { value = aws_vpc.main.id }
output "private_subnet_ids" { value = aws_subnet.private[*].id }
```

**Usage:**
```hcl
module "networking" {
  source          = "../../modules/networking"
  name            = "production"
  cidr_block      = "10.0.0.0/16"
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  tags            = { Environment = "production" }
}
```

### Provider configuration

```hcl
terraform {
  required_version = ">= 1.8.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.60"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  assume_role {
    role_arn = "arn:aws:iam::123456789012:role/TerraformDeploy"
  }
  default_tags { tags = { ManagedBy = "terraform" } }
}
```

## OpenTofu

**Key differences from Terraform:**
- Drop-in replacement: `tofu init`, `tofu plan`, `tofu apply` — same CLI surface
- No BSL restrictions; fully open-source under MPL 2.0
- State format fully compatible with Terraform
- Provider registry at `registry.opentofu.org` (mirrors HashiCorp registry)
- `tofu test` built-in (no plugin needed)

```bash
# Installation
brew install opentofu

# Migration from Terraform
tofu init -upgrade
tofu plan

# Compatibility note: providers published to registry.opentofu.org,
# but can use Terraform registry providers with:
# provider_installation { direct {} } in ~/.tofurc
```

## Pulumi

### TypeScript
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

const vpc = new awsx.ec2.Vpc("main", {
  cidrBlock: "10.0.0.0/16",
  numberOfAvailabilityZones: 2,
  enableDnsHostnames: true,
  tags: { Environment: pulumi.getStack() },
});

const cluster = new aws.ecs.Cluster("app", {});
const service = new awsx.ecs.FargateService("api", {
  cluster: cluster.arn,
  taskDefinitionArgs: {
    container: {
      image: "nginx:latest",
      cpu: 256,
      memory: 512,
      portMappings: [{ containerPort: 80 }],
    },
  },
  desiredCount: 2,
});

export const url = service.url;
```

### Python
```python
import pulumi
import pulumi_aws as aws

vpc = aws.ec2.Vpc("main", cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    tags={"Environment": pulumi.get_stack()})

pulumi.export("vpc_id", vpc.id)
```

### Stack management
```bash
pulumi stack init production          # create stack
pulumi stack select production        # switch
pulumi config set aws:region us-east-1
pulumi config set --secret db_password "s3cret!"  # encrypted at rest

pulumi preview                        # plan
pulumi up --yes                       # apply (auto-approve)
pulumi destroy                        # teardown

# CI integration
pulumi up --yes --suppress-outputs    # quiet for CI logs
```

### Pulumi Cloud backend
```bash
# Pulumi Cloud (SaaS) — default, stores state + secrets
pulumi login                         # opens browser

# Self-managed S3 backend
pulumi login "s3://my-pulumi-state-bucket"

# Azure blob
pulumi login "azblob://mycontainer"
```

### GitHub Actions CI
```yaml
- uses: pulumi/actions@v5
  with:
    command: up
    stack-name: myorg/production
    cloud-url: s3://my-pulumi-state
  env:
    PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

## AWS CDK

### TypeScript
```typescript
import * as cdk from "aws-cdk-lib";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import { Construct } from "constructs";

export class MyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, "MainVpc", {
      maxAzs: 2,
      natGateways: 1,
      subnetConfiguration: [
        { name: "public", subnetType: ec2.SubnetType.PUBLIC },
        { name: "private", subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
      ],
    });

    new cdk.CfnOutput(this, "VpcId", { value: vpc.vpcId });
  }
}

const app = new cdk.App();
new MyStack(app, "ProductionStack", {
  env: { account: "123456789012", region: "us-east-1" },
});
```

### Bootstrapping
```bash
# One-time per account/region — creates CDK toolkit resources
cdk bootstrap aws://123456789012/us-east-1

# With specific permissions boundary
cdk bootstrap aws://123456789012/us-east-1 \
  --cloudformation-execution-policies "arn:aws:iam::aws:policy/AdministratorAccess"

# Multi-account trust
cdk bootstrap aws://123456789012/us-east-1 \
  --trust 111111111111 --trust-for-lookups 111111111111
```

### GitHub Actions CI
```yaml
- run: |
    npm ci
    npx cdk synth
    npx cdk diff
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsDeploy
    aws-region: us-east-1
- run: npx cdk deploy --all --require-approval never
```

## CDKTF (CDK for Terraform)

### TypeScript
```typescript
import { Construct } from "constructs";
import { App, TerraformStack, TerraformOutput } from "cdktf";
import { AwsProvider, Vpc, Subnet } from "@cdktf/provider-aws";

class MyStack extends TerraformStack {
  constructor(scope: Construct, name: string) {
    super(scope, name);

    new AwsProvider(this, "AWS", { region: "us-east-1" });

    const vpc = new Vpc(this, "main", {
      cidrBlock: "10.0.0.0/16",
      enableDnsHostnames: true,
    });

    new TerraformOutput(this, "vpcId", { value: vpc.id });
  }
}

const app = new App();
new MyStack(app, "production");
app.synth(); // produces cdktf.out/ — Terraform JSON
```

### Workflow
```bash
npm install -g cdktf-cli
cdktf init --template=typescript --local
cdktf synth                           # generates Terraform JSON
cdktf diff                            # plan diff
cdktf deploy --auto-approve           # terraform apply
cdktf destroy
```

**When to choose CDKTF vs Pulumi:** CDKTF outputs Terraform JSON and uses Terraform CLI under the hood — best when the org is already Terraform-centric. Pulumi uses its own engine with real programming-language constructs — best for greenfield or when you want true programming-language expressiveness (loops, conditions, async).

## Bicep (Azure)

### Module design
```bicep
// main.bicep
param location string = resourceGroup().location
param environment string

@secure()
param adminPassword string

module networking './modules/networking.bicep' = {
  name: 'networking'
  params: {
    location: location
    vnetAddressPrefix: '10.0.0.0/16'
    environment: environment
  }
}

resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: 'asp-${environment}'
  location: location
  sku: { name: 'S1', tier: 'Standard' }
}
```

### Deployment stacks
```bash
# Deploy with subscription scope
az deployment sub create \
  --location eastus \
  --template-file main.bicep \
  --parameters environment=production

# What-if (preview changes)
az deployment group what-if \
  --resource-group myapp-rg \
  --template-file main.bicep \
  --parameters environment=production
```

### GitHub Actions CI
```yaml
- uses: azure/login@v2
  with: { creds: "${{ secrets.AZURE_CREDENTIALS }}" }
- run: |
    az deployment sub validate --location eastus --template-file main.bicep
    az deployment sub create --location eastus --template-file main.bicep \
      --parameters environment=${{ github.ref_name }}
```

## Crossplane (Kubernetes-native)

### Composite resource definition
```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: xpostgresqlinstances.database.example.org
spec:
  compositeTypeRef:
    apiVersion: database.example.org/v1alpha1
    kind: XPostgreSQLInstance
  resources:
    - name: rds-instance
      base:
        apiVersion: rds.aws.upbound.io/v1beta1
        kind: Instance
        spec:
          forProvider:
            region: us-east-1
            engine: postgres
            engineVersion: "16.3"
            instanceClass: db.t3.micro
            allocatedStorage: 20
            publiclyAccessible: false
          writeConnectionSecretToRef:
            namespace: crossplane-system
```

### Provider setup
```yaml
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws-rds
spec:
  package: xpkg.upbound.io/upbound/provider-aws-rds:v1.5.0
---
apiVersion: aws.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: default
spec:
  credentials:
    source: IRSA  # IAM Roles for Service Accounts
```

## State Management Patterns

### State migration (refactoring resource addresses)
```bash
# Move resource between modules
terraform state mv module.old.aws_instance.app module.new.aws_instance.app

# Remove dangling resource (destroyed outside Terraform)
terraform state rm aws_s3_bucket.deleted_manually

# Import existing resource
terraform import aws_instance.existing i-0a1b2c3d4e5f67890

# List all resources in state
terraform state list
```

### State surgery (corrupted state recovery)
```bash
# Pull and examine state
terraform state pull > state.json
# Edit state.json (remove corrupted resource), then:
terraform state push state.json

# Alternative: targeted state removal
terraform state rm -dry-run aws_iam_role.broken
terraform state rm aws_iam_role.broken
# Then re-import
terraform import aws_iam_role.broken MyRoleName
```

### Remote backend config migration
```bash
# Migrate from local to S3 backend
terraform init -migrate-state -backend-config=backend.hcl

# backend.hcl
bucket         = "myorg-tf-state"
key            = "production/terraform.tfstate"
region         = "us-east-1"
dynamodb_table = "terraform-state-lock"
encrypt        = true
```

## Drift Detection

### Daily plan cron (GitHub Actions)
```yaml
name: Drift Detection
on:
  schedule:
    - cron: "0 6 * * *"   # daily at 06:00 UTC
jobs:
  drift-check:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        workspace: [production, staging]
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: |
          cd environments/${{ matrix.workspace }}
          terraform init
          terraform plan -detailed-exitcode -out=tfplan
          EXIT=$?
          if [ $EXIT -eq 2 ]; then
            echo "DRIFT_DETECTED=true" >> $GITHUB_ENV
          fi
      - name: Notify on drift
        if: env.DRIFT_DETECTED == 'true'
        uses: slackapi/slack-github-action@v1
        with:
          payload: '{"text":"Drift detected in ${{ matrix.workspace }} — resources are out of sync with Terraform state"}'
```

### PR plan comments (Atlantis / Terraform Cloud)
```yaml
# With hashicorp/setup-terraform + sticky comment action
- id: plan
  run: |
    cd environments/production
    terraform init
    terraform plan -no-color -out=tfplan 2>&1 | tee plan.txt
- uses: marocchino/sticky-pull-request-comment@v2
  with:
    header: terraform-plan
    message: |
      <details><summary>Terraform Plan</summary>

      ```
      ${{ steps.plan.outputs.stdout }}
      ```
      </details>
```

### Drift reconciliation
```bash
# Apply to reconcile drift
terraform apply -auto-approve

# Import specific drifted resources individually
terraform import aws_s3_bucket.drifted_bucket my-bucket-name
# Then plan again to see remaining drift
terraform plan
```

## Cost Estimation

### Infracost CI integration
```yaml
- uses: infracost/actions/setup@v3
  with: { api-key: "${{ secrets.INFRACOST_API_KEY }}" }
- run: infracost breakdown --path . --format json --out-file infracost.json
- run: infracost comment github --path infracost.json --repo $GITHUB_REPOSITORY --pull-request ${{ github.event.number }}
```

### Blocking on cost threshold
```yaml
- run: |
    MONTHLY=$(infracost breakdown --path . --format json | jq '.totalMonthlyCost | tonumber')
    if (( $(echo "$MONTHLY > 5000" | bc -l) )); then
      echo "Monthly cost $MONTHLY exceeds $5000 threshold — blocking deploy"
      exit 1
    fi
```

### Terraform Cloud cost estimates
```hcl
# TFC automatically provides cost estimates for supported resources
# Enable in workspace Settings → Cost Estimation
# Cost estimates appear inline on PRs when VCS integration is configured
```

## Policy as Code

### Open Policy Agent / Rego (Terraform validation)
```rego
# policy/deny_public_s3.rego
package terraform

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  resource.change.after.acl == "public-read"
  msg = sprintf("S3 bucket %s has public-read ACL — deny", [resource.address])
}

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_security_group_rule"
  resource.change.after.cidr_blocks[_] == "0.0.0.0/0"
  msg = sprintf("Security group rule %s opens to 0.0.0.0/0", [resource.address])
}
```

```bash
terraform plan -out=tfplan
terraform show -json tfplan > plan.json
opa eval --input plan.json --data policy/ "data.terraform.deny"
```

### Checkov
```yaml
- uses: bridgecrewio/checkov-action@v12
  with:
    directory: .
    framework: terraform
    soft_fail: false    # true = warn only, false = fail pipeline
    output_format: sarif
```

### tfsec
```bash
tfsec . --format sarif --out tfsec-results.sarif
# Exit code 0 = no issues, 1 = warnings, 2+ = errors
```

### Terrascan
```bash
terrascan scan -d . -i terraform -o sarif > terrascan.sarif
```

### Sentinel (Terraform Cloud only)
```sentinel
# sentinel.hcl
import "tfplan/v2" as tfplan

main = rule {
    all tfplan.resource_changes as _, rc {
        rc.type is "aws_s3_bucket" and
        rc.change.after.acl is "public-read"
    } is false
}
```

## Multi-Cloud Patterns

### Provider aliasing
```hcl
provider "aws" {
  alias  = "us_east"
  region = "us-east-1"
}
provider "aws" {
  alias  = "eu_west"
  region = "eu-west-1"
}
provider "azurerm" {
  features {}
}

# Usage
resource "aws_s3_bucket" "primary" {
  provider = aws.us_east
  bucket   = "my-primary-bucket"
}
resource "aws_s3_bucket" "replica" {
  provider = aws.eu_west
  bucket   = "my-replica-bucket"
}
resource "azurerm_resource_group" "main" {
  name     = "multicloud-rg"
  location = "East US"
}
```

### Cross-cloud state references (terraform_remote_state)
```hcl
# In AWS config, reference GCP outputs
data "terraform_remote_state" "gcp" {
  backend = "gcs"
  config = {
    bucket = "myorg-gcp-tf-state"
    prefix = "production"
  }
}

resource "aws_route53_zone" "main" {
  name = data.terraform_remote_state.gcp.outputs.dns_zone_name
}
```

### Unified variables (Terragrunt / TFC variable sets)
```hcl
# variables.tf — shared across clouds
variable "environment" { type = string }
variable "region" {
  type    = map(string)
  default = { aws = "us-east-1", gcp = "us-central1", azure = "eastus" }
}
```

## CI Integration

### Plan on PR, apply on merge (GitHub Actions)
```yaml
name: Terraform
on:
  pull_request: { branches: [main] }
  push: { branches: [main] }
jobs:
  terraform:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - name: Terraform Plan
        if: github.event_name == 'pull_request'
        run: |
          cd environments/production
          terraform init
          terraform plan -no-color | tee /tmp/plan.txt
      - name: Post Plan Comment
        if: github.event_name == 'pull_request'
        uses: thollander/actions-comment-pull-request@v2
        with:
          filePath: /tmp/plan.txt
          comment_tag: terraform-plan
      - name: Terraform Apply
        if: github.event_name == 'push'
        run: |
          cd environments/production
          terraform init
          terraform apply -auto-approve
```

### Approval gates
```yaml
deploy-production:
  needs: [terraform-plan]
  environment: production         # GitHub Environments with required reviewers
  runs-on: ubuntu-latest
  steps:
    - run: |
        cd environments/production
        terraform init
        terraform apply -auto-approve
```

## Module Versioning and Registry Publishing

### Module versioning
```hcl
# Tag modules with semver in git
git tag v1.0.0
git push origin v1.0.0

# Consumers pin versions
module "vpc" {
  source  = "git::https://github.com/myorg/terraform-aws-vpc?ref=v1.0.0"
  # ...
}
```

### Private registry (Terraform Cloud / HCP)
```hcl
module "vpc" {
  source  = "app.terraform.io/myorg/vpc/aws"
  version = "~> 1.0"
}
```

### GitHub-based module source
```hcl
# Tagged version
module "networking" {
  source = "github.com/myorg/terraform-aws-networking?ref=v2.1.0"
}

# Specific commit
module "networking" {
  source = "github.com/myorg/terraform-aws-networking?ref=abc1234"
}

# Subdirectory within a monorepo
module "database" {
  source = "git::https://github.com/myorg/infra-modules.git//modules/rds?ref=v1.5.0"
}
```

### Terraform Registry publishing requirements
```hcl
# Required: GitHub repo named terraform-<PROVIDER>-<NAME>
# Example: terraform-aws-vpc → registry publishes as myorg/vpc/aws
# Required files: main.tf, variables.tf, outputs.tf, README.md, LICENSE

# Optional but recommended: examples/ directory with consumable examples
# examples/complete/main.tf — full featured usage
```

### Release automation (GitHub Actions)
```yaml
name: Release Module
on:
  push:
    tags: ["v*"]
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create GitHub Release
        run: |
          gh release create "${{ github.ref_name }}" \
            --title "${{ github.ref_name }}" \
            --generate-notes
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Pulumi provider publishing
```bash
# Pulumi packages follow <name>@<version> convention
cd sdk/nodejs
npm publish

cd sdk/python
python -m build && twine upload dist/*
```
