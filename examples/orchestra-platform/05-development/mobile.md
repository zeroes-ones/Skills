# Mobile App Architecture

## Technology Stack

React Native 0.74 with Expo SDK 51, managed workflow. TypeScript 5.5 for type safety. React Navigation 6 for stack and tab navigation. TanStack React Query for API data fetching (same query keys as the web app, shared hooks extracted to `packages/shared-hooks`). Zustand for local UI state and offline queue management. Expo EAS Build for CI/CD (development builds, preview, production).

## Scope — Read-Only Operational View

The mobile app is intentionally read-only in v1.0. It provides operational visibility for on-call engineers and team leads. Write operations (creating services, running templates, configuring plugins) remain web-only for the initial release. This scoping decision reduces mobile QA surface by 60% and aligns with user research showing that 78% of mobile sessions are health checks and alert responses.

## Key Screens

**Service Health Dashboard**: Scrollable list of services grouped by team. Each row shows service name, health indicator (colored dot), last deployment time, and incident count. Pull-to-refresh triggers a full health recheck. Tapping a service opens a detail view with metrics (CPU, memory, request rate), recent deployments, and active alerts.

**On-Call Alerts**: Chronological feed of PagerDuty alerts with severity badge, acknowledging/snoozing via swipe actions. Each alert shows affected service, trigger condition, and time since firing. Deep links open the web app's incident detail page.

**Template Execution Monitor**: Running and recent template executions with progress bars and status. Supports filtering by status (running, success, failed) and search by service name.

## Push Notifications

Firebase Cloud Messaging (FCM) delivers push notifications for: P1 alerts (bypasses Do Not Disturb), deployment failures, and template execution completion. Notification payload includes a `deepLink` field that navigates directly to the relevant screen. User preferences for notification channels are synced with the backend and configurable per alert severity.

## Offline Support

Cached health data persists via React Query's `persistQueryClient` with an AsyncStorage adapter (7-day TTL). When offline, the dashboard shows the last-known state with a banner ("Offline — data from July 15, 14:32 UTC"). Write actions (alert acknowledge, snooze) queue locally and replay when connectivity returns, with conflict resolution preferring server state.
