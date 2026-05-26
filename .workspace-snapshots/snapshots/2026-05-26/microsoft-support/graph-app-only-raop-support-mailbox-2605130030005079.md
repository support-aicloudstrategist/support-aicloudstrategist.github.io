# Microsoft Support Request: Graph app-only access blocked by RAOP AppOnly AccessPolicy for one mailbox

- **Ticket #:** 2605130030005079
- **Status at submission:** Open; support agent being assigned
- **Severity:** Sev C
- **Created:** 2026-05-13 14:06 IST
- **Created by:** Rajiv Gupta
- **Contact method:** Email/service request (contact details shown in Microsoft admin center; not repeated here)

## Title

Graph app-only access blocked by RAOP AppOnly AccessPolicy for one mailbox

## Description submitted

Tenant/org: Digiscience Techsol Private Limited / aicloudstrategist.com

Issue summary:
Microsoft Graph app-only mailbox access is failing only for support@aicloudstrategist.com with HTTP 403 ErrorAccessDenied. The same Entra app and Exchange Application Access Policy configuration works for contact@aicloudstrategist.com. Delegated Graph access for support@ works, so the mailbox itself is reachable; the permanent requirement is app-only access.

Graph app:
- Display name: AICloudStrategist Mail Automation
- Application (client) ID: 8eb00610-7406-49ae-9dde-c223fb18107e
- Application permissions/admin-consented: Mail.ReadWrite, Mail.Send, User.Read.All

Exchange Application Access Policy:
- Policy restricts app access via mail-enabled security group: aics-mail-automation-allowed@aicloudstrategist.com
- Intended allowed mailboxes: support@aicloudstrategist.com and contact@aicloudstrategist.com
- Test-ApplicationAccessPolicy previously showed Granted for both support@aicloudstrategist.com and contact@aicloudstrategist.com

Observed behavior:
- App-only Graph read/send works for contact@aicloudstrategist.com
- App-only Graph for support@aicloudstrategist.com fails with:
  403 ErrorAccessDenied: Access to OData is disabled: [RAOP] : Blocked by tenant configured AppOnly AccessPolicy settings.
- Delegated Graph fallback for support@aicloudstrategist.com works, confirming operations are not blocked, but app-only remains broken.

Request:
Please investigate why the Exchange/Graph AppOnly AccessPolicy/RAOP evaluation blocks support@aicloudstrategist.com despite Test-ApplicationAccessPolicy showing Granted and the same policy allowing contact@aicloudstrategist.com. Please confirm whether there is backend policy cache/propagation issue, mailbox-level flag, group membership resolution issue, or policy corruption, and provide remediation.

## Confirmation shown by Microsoft admin center

Service request opened. A support agent is being assigned to your request.
