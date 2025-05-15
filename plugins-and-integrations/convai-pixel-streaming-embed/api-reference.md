---
icon: webhook
---

# API Reference

Props (`PixelStreamComponent`)

| Prop          | Type            | Required | Description                        |
| ------------- | --------------- | -------- | ---------------------------------- |
| expId         | string          | ✅        | Your experiment ID                 |
| InitialScreen | React.ReactNode | ❌        | Custom loading screen              |
| serviceUrls   | object          | ❌        | Override backend service endpoints |

#### Options (`PixelStreamClient`)

| Option        | Type        | Required | Description                 |
| ------------- | ----------- | -------- | --------------------------- |
| container     | HTMLElement | ✅        | The video container element |
| expId         | string      | ✅        | Experiment ID               |
| InitialScreen | HTMLElement | ❌        | Custom loading element      |
