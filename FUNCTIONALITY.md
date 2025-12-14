# Product Functionality Document

 ## Overview
 This document explains how the AI Lead Generation Platform actually works, from identifying a lead to launching a live ad campaign.

 ---

 ## 1. Lead Generation
 **Goal:** Identify potential customers based on business criteria.

 1.  **User Input:** The user enters an "Industry" (e.g., *Logistics*) and "Location" (e.g., *Miami*) on the Dashboard.
 2.  **Data Provider:** The system sends this query to the configured Data Provider.
     *   **Apollo.io / People Data Labs (Real):** The system uses your API Key to search these external B2B databases and returns verified contact info (Email, Phone, LinkedIn).
     *   **Mock (Demo):** Uses a built-in generator to create realistic dummy data for testing.
 3.  **Storage:** The results are saved to the local database (`Lead` table) so the user can access them anytime in the "History" panel.

 ---

 ## 2. Messaging
 **Goal:** Contact the generated leads directly.

 1.  **Selection:** The user clicks "Message" on a specific lead in the results table.
 2.  **Channel:** The user selects Email or SMS.
 3.  **Delivery (Simulation):**
     *   Currently, the system logs the message to the database (`MessageLog`) and returns a "Sent" status.
     *   **Future Production:** This service would connect to **SendGrid** (for Email) or **Twilio** (for SMS) using API keys to actually deliver the message.

 ---

 ## 3. Ad Campaign Management
 **Goal:** Retarget these leads or similar audiences on major ad platforms.

 ### A. Connecting Accounts (Integrations)
 Before launching ads, the system must have permission to manage the user's ad accounts.

 1.  **Integrations Page:** The user navigates to the "Integrations" tab.
 2.  **OAuth Flow:** The user clicks "Connect" on a platform (e.g., Google Ads).
 3.  **Authorization:**
     *   **Real World:** The user is redirected to Google's login page, grants permission, and Google returns an `access_token` to our system.
     *   **Current MVP:** We simulate this handshake. Clicking connect securely stores a "mock" token in our database (`AdAccount` table) to represent a successful link.

 ### B. Launching a Campaign
 1.  **Campaign Setup:** On the Dashboard, the user fills out the Campaign form (Name, Budget, Target).
 2.  **Validation:** The `AdService` checks if the user has a valid `AdAccount` for the selected platform. If not, the launch is blocked.
 3.  **API Execution:**
     *   **Real World:** The system uses the stored `access_token` to make an authenticated POST request to the Ad Platform's API (e.g., `google-ads-api`) to create a new Campaign entity with the specified budget.
     *   **Current MVP:** The system records the Campaign in our local database and sets the status to "Active".

 ---

 ## 4. Analytics
 **Goal:** Track performance.

 1.  **Data Retrieval:** When the user views "Stats", the `AnalyticsService` is called.
 2.  **Real World:** The service would query the Ad Platform's Reporting API (e.g., Facebook Insights API) for the latest `impressions`, `clicks`, and `cost`.
 3.  **Current MVP:** The system generates realistic performance curves based on the campaign's budget and duration to simulate a live campaign.
