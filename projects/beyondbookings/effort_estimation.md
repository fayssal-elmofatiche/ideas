# BeyondBookings - Invoice Payment Automation
## Effort & Cost Estimation

### Client Context
- **Company**: BeyondBookings (hospitality fintech, ~10-12 people)
- **Problem**: Manual processing of supplier invoices received via a dedicated Outlook mailbox
- **Volume**: ~1,000 invoices/year (up from 500 last year), ~20-40/week at peak
- **Invoice types**: Mix of digitally generated and scanned PDFs
- **Vendors**: Handful today, should scale to hundreds
- **Current stack**: HubSpot (CRM), Lexoffice (bookkeeping), manual bank transfers, local Access database (CFO financial consolidation)
- **Approval**: Single approver
- **Timeline**: A few months
- **Additional need**: Replace the local Access database where the CFO manually consolidates financials (customer data from HubSpot, invoice/payment data) with an automated, cloud-based solution

---

## Recommended Approach: Modular Delivery

### Core: Invoice Processing MVP (4-6 weeks)

Core extraction + approval workflow. Get value fast, validate accuracy before automating payments. This component is always included and serves as the foundation for all variants.

| Task | Description | Effort (PD) | Hours |
|------|-------------|-------------|-------|
| **Email Ingestion** | Microsoft Graph API integration to monitor the Outlook mailbox, extract PDF attachments, queue for processing | 2-3 PD | 16-24h |
| **PDF Processing Pipeline** | Digital PDF text extraction + OCR for scanned docs (Azure Document Intelligence or AWS Textract) | 3-4 PD | 24-32h |
| **AI Data Extraction** | LLM-based field extraction (vendor, invoice #, date, due date, amount, VAT, IBAN, line items) with confidence scoring | 4-5 PD | 32-40h |
| **Approval Dashboard** | Simple web UI: list of pending invoices, side-by-side PDF viewer + extracted data, approve/reject/edit, notifications via email | 3-4 PD | 24-32h |
| **Lexoffice Integration** | Push approved invoice data into Lexoffice via API | 2-3 PD | 16-24h |
| **Infrastructure & Auth** | Hosting, authentication, basic monitoring, environment setup | 2-3 PD | 16-24h |
| **Testing & QA** | End-to-end testing with real invoices, edge case handling, accuracy tuning | 3-4 PD | 24-32h |

**Core Total: ~19-26 PD (152-208h)**

#### Core Deliverables
- Invoices automatically read from Outlook and parsed
- Extracted data presented for review in a dashboard
- Approver can review, correct, approve/reject
- Approved invoices pushed to Lexoffice
- Payment still triggered manually (but all data is pre-filled)

---

### Variant A: Full Payment Automation (3-4 weeks after Core)

Add payment automation and operational improvements based on Core learnings.

| Task | Description | Effort (PD) | Hours |
|------|-------------|-------------|-------|
| **Payment Automation** | Banking API integration (e.g. finAPI) or Lexoffice payment triggering for approved invoices | 5-6 PD | 40-48h |
| **Duplicate Detection** | Invoice deduplication, vendor matching against known database | 3-4 PD | 24-32h |
| **Accuracy Feedback Loop** | Use approver corrections to improve extraction over time | 3-4 PD | 24-32h |
| **Notifications & Alerts** | Reminders for pending approvals, payment confirmations, failure alerts | 2-3 PD | 16-24h |
| **Reporting** | Basic dashboard: processed/pending/rejected counts, monthly spend overview | 2-3 PD | 16-24h |
| **Hardening** | Error handling, retry logic, GDPR data handling review, audit logging | 3-4 PD | 24-32h |

**Variant A Total: ~18-24 PD (144-192h)**

---

### Variant B: CFO Financial Consolidation (replaces Access database)

Replace the local Access database with a cloud-based financial consolidation layer. Can be executed in parallel with Core or sequentially after it. Benefits from shared infrastructure with the invoice automation.

#### Discovery & Data Migration (1-2 weeks)

| Task | Description | Effort (PD) | Hours |
| ---- | ----------- | ----------- | ----- |
| **Access DB Analysis** | Reverse-engineer the existing Access database: tables, relationships, queries, reports. Understand what the CFO actually uses vs. legacy clutter | 3-4 PD | 24-32h |
| **Data Model Design** | Design a clean, normalized data model that covers the CFO's consolidation needs (customers, revenue, invoices, payments, cash flow) | 2-3 PD | 16-24h |
| **Data Migration** | Migrate historical data from Access into the new system. Validate completeness with the CFO | 2-3 PD | 16-24h |

#### Automated Data Integrations (2-3 weeks)

| Task | Description | Effort (PD) | Hours |
| ---- | ----------- | ----------- | ----- |
| **HubSpot Integration** | Automated sync of customer data, deals, and revenue via HubSpot API. Replace the manual copy-paste workflow. Scheduled sync + webhook for real-time updates | 4-5 PD | 32-40h |
| **Lexoffice Integration** | Pull bookkeeping data (expenses, revenue, tax) from Lexoffice API. Complement the invoice data already flowing from Phase 1 | 3-4 PD | 24-32h |
| **Invoice Pipeline Integration** | Connect the invoice automation pipeline (Core) so approved/paid invoices flow directly into the CFO view | 2-3 PD | 16-24h |
| **Data Reconciliation** | Automated cross-checks between sources (HubSpot revenue vs Lexoffice bookings vs invoice payments) with discrepancy flagging | 3-4 PD | 24-32h |

#### CFO Dashboard (2-3 weeks)

| Task | Description | Effort (PD) | Hours |
| ---- | ----------- | ----------- | ----- |
| **Financial Overview** | Consolidated dashboard: revenue, expenses, cash flow, outstanding invoices, accounts payable/receivable | 4-5 PD | 32-40h |
| **Customer Financial View** | Per-customer P&L view combining HubSpot deal data with invoice/payment history | 3-4 PD | 24-32h |
| **Reporting & Export** | Monthly/quarterly financial reports, CSV/PDF export for accountant or tax advisor | 2-3 PD | 16-24h |
| **Filters & Drill-Down** | Filter by period, customer, vendor, category. Drill down from summary to individual transactions | 2-3 PD | 16-24h |
| **Testing & CFO Validation** | Validate numbers against Access database, iterate on views based on CFO feedback | 3-4 PD | 24-32h |

**Variant B Total: ~28-38 PD (224-304h)**

#### Variant B Deliverables

- Local Access database fully replaced by cloud-based solution
- HubSpot customer/revenue data synced automatically (no more manual pulls)
- Lexoffice bookkeeping data integrated automatically
- Invoice pipeline data flows in from Core automation
- CFO dashboard with consolidated financial overview, per-customer views, and exportable reports
- Discrepancy detection between data sources

#### Technical Approach Options

| Option | Pros | Cons | Fit |
| ------ | ---- | ---- | --- |
| **Custom dashboard** (React + PostgreSQL) | Full control, integrates seamlessly with Phase 1 app | More dev effort, needs maintenance | Best if Phase 1 is already custom-built |
| **Metabase / Superset + PostgreSQL** | Fast to build reports, SQL-native, open source | Less flexibility on custom workflows | Good balance of speed and capability |
| **Retool / Appsmith** | Very fast to build, low-code, good for internal tools | Vendor lock-in, per-seat pricing | Fastest to deliver, fine for small team |

*Recommendation: If the approval dashboard from Core is built as a custom web app, extend it with the CFO views. If Core uses a low-code tool (Retool), build the CFO dashboard there too for consistency.*

---

### Variant C: Client Invoice Portal (replaces Outlook inbox)

Replace the dedicated Outlook mailbox with a branded client-facing portal where suppliers upload invoices directly, track processing status in real-time, and receive feedback. Improves client experience and data quality (structured uploads vs. free-form emails).

*Note: This variant assumes Core is already built. The portal replaces the email ingestion layer and adds a client-facing frontend on top of the existing processing pipeline.*

#### Portal Core (3-4 weeks)

| Task | Description | Effort (PD) | Hours |
| ---- | ----------- | ----------- | ----- |
| **Client Authentication** | Client accounts with secure login (email/password or SSO). Invitation-based onboarding by BeyondBookings. Role management (e.g. multiple users per supplier) | 4-5 PD | 32-40h |
| **Invoice Upload** | Drag-and-drop upload interface. Support for single/bulk PDF upload. File validation (format, size). Optional structured fields at upload (invoice #, amount, PO reference) to improve extraction accuracy | 4-5 PD | 32-40h |
| **Status Tracking Dashboard** | Real-time invoice status for clients: Uploaded → Processing → Under Review → Approved → Paid. Timeline view per invoice with timestamps | 4-5 PD | 32-40h |
| **Feedback & Communication** | Per-invoice comment thread between BeyondBookings and the supplier. Rejection reasons with resubmission workflow. Request for clarification or missing documents | 3-4 PD | 24-32h |
| **Email Notifications** | Automated notifications to clients on status changes (received, approved, rejected, paid). Configurable notification preferences | 2-3 PD | 16-24h |

#### Integration & Migration (1-2 weeks)

| Task | Description | Effort (PD) | Hours |
| ---- | ----------- | ----------- | ----- |
| **Pipeline Integration** | Connect portal uploads to the existing PDF processing pipeline from Core. Portal becomes an alternative ingestion source alongside email (dual-mode during transition) | 3-4 PD | 24-32h |
| **Approval Dashboard Updates** | Extend the internal approval dashboard (Core) with client feedback capabilities, link to portal communication thread, show client-provided metadata | 2-3 PD | 16-24h |
| **Client Onboarding Flow** | Admin interface for BeyondBookings to invite clients, manage accounts, and monitor portal usage | 2-3 PD | 16-24h |

#### Branding & Polish (1 week)

| Task | Description | Effort (PD) | Hours |
| ---- | ----------- | ----------- | ----- |
| **UI/UX Design** | Clean, branded interface aligned with BeyondBookings identity. Mobile-responsive for suppliers uploading from phone | 3-4 PD | 24-32h |
| **Multi-language Support** | German and English at minimum (supplier base may be international in hospitality) | 1-2 PD | 8-16h |
| **Testing & QA** | End-to-end testing from client upload through processing to status update. Cross-browser, mobile testing | 3-4 PD | 24-32h |

**Variant C Total: ~28-38 PD (224-304h)**

#### Variant C Deliverables

- Branded client portal with secure login for suppliers
- Drag-and-drop invoice upload (single and bulk)
- Real-time status tracking for every submitted invoice
- Per-invoice feedback and communication thread
- Automated email notifications on status changes
- Dual-mode ingestion: portal + Outlook (for transition period, then phase out email)
- Admin interface for client account management

#### Key Consideration: Build vs. Core Dependency

The portal **requires Core** to be functional first — it feeds into the same processing pipeline. However, the UI/UX design and authentication layer can start in parallel with Core development. Recommended sequencing:

1. Weeks 1-4: Core development + portal UI/UX design (parallel)
2. Weeks 5-8: Core completion + portal development
3. Weeks 9-10: Integration, testing, client onboarding

---

## Cost Estimation

### Technology Costs (Monthly)

| Service | Estimated Cost |
|---------|---------------|
| OCR service (Azure DI, AWS Textract, or Google Document AI) | ~€50-100/mo (at 1,000 invoices/year) |
| LLM API (GPT-4o / Claude) | ~€30-80/mo |
| Hosting (cloud functions + small app) | ~€30-60/mo |
| Email API (Microsoft Graph) | Included in M365 license |
| Lexoffice API | Included in Lexoffice subscription |
| Banking API (Variant A) | Depends on provider, ~€50-150/mo |
| Database hosting (Variant B) | ~€20-50/mo (managed PostgreSQL) |
| Dashboard tool license (if Retool/Metabase Cloud) | ~€0-100/mo |
| Client portal hosting (Variant C) | ~€30-60/mo (included if shared with Core infra) |
| Auth provider (Variant C) | ~€0-25/mo (Auth0 free tier or similar) |
| Transactional email (Variant C) | ~€0-20/mo (SendGrid/Resend at this volume) |

**Estimated infra cost: ~€200-550/month** (all phases combined)

### Development Costs

#### Rate Structure

Rates are tiered based on total engagement volume, rewarding larger commitments with a reduced daily rate:

| Engagement Volume | Daily Rate | Hourly Rate |
|-------------------|------------|-------------|
| Up to 40 PD | €1,200/day | €150/h |
| 41-80 PD | €1,050/day | €130/h |
| 81-120 PD | €950/day | €120/h |
| 120+ PD | €880/day | €110/h |

#### Per-Component Effort

| Component | Effort (PD) | Hours |
|-----------|-------------|-------|
| Core (Invoice Processing MVP) | 19-26 PD | 152-208h |
| Variant A (Full Payment Automation) | 18-24 PD | 144-192h |
| Variant B (CFO Consolidation) | 28-38 PD | 224-304h |
| Variant C (Client Portal) | 28-38 PD | 224-304h |

#### Packaging Options

| Package | Scope | Effort (PD) | Hours | Rate | Cost |
| ------- | ----- | ----------- | ----- | ---- | ---- |
| **A: Core only** | Core | 19-26 PD | 152-208h | €1,200/day | €22,800 - €31,200 |
| **B: Core + CFO** | Core + Var. B | 47-64 PD | 376-512h | €1,050/day | €49,350 - €67,200 |
| **C: Core + Portal** | Core + Var. C | 47-64 PD | 376-512h | €1,050/day | €49,350 - €67,200 |
| **D: Core + CFO + Portal** | Core + Var. B + C | 75-102 PD | 600-816h | €950/day | €71,250 - €96,900 |
| **E: Everything** | Core + Var. A + B + C | 93-126 PD | 744-1008h | €880/day | €81,840 - €110,880 |

#### Savings at Scale

| Package | vs. Package A rate | Saving per PD | Total Saving |
| ------- | ------------------ | ------------- | ------------ |
| **A** | baseline | - | - |
| **B / C** | -12.5% | €150/day | €7,050 - €9,600 |
| **D** | -20.8% | €250/day | €18,750 - €25,500 |
| **E** | -26.7% | €320/day | €29,760 - €40,320 |

*Package D offers the best value-to-scope ratio: 20% lower rate than a standalone engagement, while delivering Core automation plus both the CFO dashboard and client portal.*

---

## Key Technical Decisions

### Recommended Architecture

```
Outlook Mailbox                          HubSpot CRM
    → Microsoft Graph API                    → HubSpot API (scheduled sync)
    → PDF Processing Service                 ↓
        → Digital PDF: text extraction   Customer & Revenue Data ──┐
        → Scanned PDF: OCR (Azure DI)                             │
    → LLM Extraction (confidence scores)                          │
    → Approval Dashboard ◄────────────────────────────────────────►│
    → Lexoffice API (bookkeeping sync) ──→ Bookkeeping Data ──────┤
    → Banking API (payment - Variant A)                              │
                                                                   ↓
                                                          ┌────────────────┐
                                                          │  PostgreSQL DB  │
                                                          │  (central data) │
                                                          └───────┬────────┘
                                                                  ↓
                                                          CFO Dashboard
                                                          (financial consolidation)
```

### Technology Choices to Decide
1. **OCR Provider**: Azure Document Intelligence vs AWS Textract vs Google Document AI
2. **LLM**: GPT-4o vs Claude — both strong at structured extraction
3. **Frontend**: Simple React app vs low-code (Retool/Appsmith) for the dashboard
4. **Hosting**: Azure (natural fit with Outlook) vs AWS vs Vercel + serverless
5. **Payment API**: finAPI, Klarna Kosma, or direct bank API (Variant A)

---

## Risks & Considerations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Low OCR accuracy on scanned invoices | High | Budget extra tuning time, use confidence scoring to flag uncertain extractions |
| Diverse invoice layouts from new vendors | Medium | LLM-based extraction handles variety well, feedback loop improves over time |
| Banking API complexity / bank onboarding | Medium | Start with Lexoffice-triggered payments before full bank API integration |
| GDPR / data handling | Medium | Flag to client for legal review, ensure no invoice data stored beyond necessary retention |
| GoBD compliance (German tax archiving) | Low-Medium | Client should verify with their tax advisor; may need compliant archiving added |
| Access DB migration data quality | Medium | Legacy Access data may be inconsistent; budget time for cleanup and CFO validation |
| HubSpot data model complexity | Low-Medium | Need to map HubSpot custom properties to financial model; requires discovery session |
| CFO adoption | Medium | Involve CFO early in dashboard design; iterative feedback sessions to match their workflow |
| Client portal adoption | Medium | Suppliers need a reason to switch from email; clear UX advantage and status tracking are key incentives |
| Dual ingestion during transition | Low-Medium | Support both email and portal simultaneously; plan a clear sunset timeline for email-based submissions |

---

## Recommendation

Start with **Package D (Core + Variant B + Variant C)** as the recommended engagement:

1. **Core** proves out the invoice extraction accuracy with real data (weeks 1-8)
2. **Variant B** runs in parallel to replace the Access database and give the CFO immediate value from automated HubSpot/Lexoffice data consolidation (weeks 3-10)
3. **Variant C** starts UI/UX design in parallel with Core, then builds the client portal once the processing pipeline is stable (weeks 4-12)
4. **Variant A** (payment automation) follows as an add-on once extraction accuracy is validated and the client is confident in the system

This approach delivers tangible value to three stakeholders simultaneously:
- **Invoice processor**: automated extraction and approval workflow
- **CFO**: real-time financial consolidation replacing manual Access work
- **Suppliers/clients**: self-service portal with transparency on invoice status

If budget is a constraint, **Package B (Core + Variant B)** is the minimum viable engagement that addresses the two most painful manual workflows. The client portal (Variant C) can then follow as a separate engagement.
