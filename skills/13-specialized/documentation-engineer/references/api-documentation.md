# API Documentation

### OpenAPI/Swagger

- **Spec as Source of Truth**: `openapi.yaml` lives in the repo. All changes to the API start with changes to the spec.
- **CI Validation**:
  ```yaml
  - name: Validate OpenAPI Spec
    run: npx @stoplight/spectral-cli lint openapi.yaml
  - name: Check Breaking Changes
    run: npx @apideck/openapi-diff openapi-v1.yaml openapi-v2.yaml
  ```
- **Reference Generation**: `docusaurus-plugin-openapi-docs` renders OpenAPI specs as Docusaurus doc pages. Alternative: Redoc standalone HTML, Scalar API reference.
- **Supplemental Hand-Written Guides**: Authentication, pagination, error handling, webhooks, rate limiting -- these are better explained in prose than auto-generated.

### GraphQL

- **Schema SDL as Source of Truth**: GraphQL schema files in the repo. Annotate with triple-quote description comments.
- **Auto-Generated Docs**: GraphDoc, SpectaQL, or Magidoc read the schema SDL and generate a full reference site.
- **Interactive Explorer**: GraphiQL or Apollo Studio Sandbox embedded for query experimentation.

### gRPC / Protobuf

- **`.proto` as Source of Truth**: Proto definitions in the repo.
- **Auto-Generated Docs**: `protoc-gen-doc` generates Markdown or HTML from `.proto` files.
  ```bash
  protoc --doc_out=./docs/api --doc_opt=markdown,api.md proto/*.proto
  ```
- **Service Documentation**: Each RPC method, message type, and field defined in the proto becomes documented.

### Interactive API Explorer

- **Try-It-Out Functionality**: Swagger UI, Scalar, or Mintlify's embedded API playground -- let users send real requests from the docs.
- **Auth Configuration**: Support API key, Bearer token, OAuth2. Store example tokens securely.
- **Example Requests**: Pre-populated curl, Python, JavaScript, Go examples for each endpoint.

### SDK Documentation

- **TypeDoc (TypeScript)**: `npx typedoc --out docs/api src/index.ts`
- **Javadoc (Java)**: `mvn javadoc:javadoc` outputs to `target/site/apidocs/`
- **Sphinx (Python)**: `sphinx-apidoc -o docs/api src/` followed by `make html`
- **CI Integration**: SDK docs are auto-generated on merge and published to the docs site.
