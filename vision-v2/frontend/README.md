# NOC Vision Frontend

Vue 3 + Vite + Tailwind CSS frontend for NOC Vision - Network Operations Center Platform.

## Features

- Vue 3 Composition API with `<script setup>`
- Vue Router for navigation
- Pinia for state management
- Tailwind CSS with shadcn-admin inspired theme
- Light/Dark/System theme switching
- Responsive design with mobile sidebar
- JWT authentication

## Project Structure

```
frontend/
├── public/
│   └── logo.png              # NOC Vision logo
├── src/
│   ├── assets/
│   │   └── css/
│   │       └── main.css      # Tailwind imports + custom styles
│   ├── components/
│   │   ├── ui/               # UI components (Button, Card, Input, etc.)
│   │   └── layout/           # Layout components (Sidebar, SidebarItem)
│   ├── layouts/
│   │   └── DashboardLayout.vue
│   ├── lib/
│   │   └── utils.js          # Utility functions (cn, formatDate)
│   ├── router/
│   │   └── index.js          # Vue Router configuration
│   ├── stores/
│   │   ├── auth.js           # Authentication store
│   │   └── theme.js          # Theme store
│   ├── views/
│   │   ├── auth/             # SignIn, SignUp, ForgotPassword
│   │   ├── dashboard/        # Dashboard
│   │   ├── plugins/          # Plugins
│   │   ├── inventory/        # Inventory Manager
│   │   ├── performance/      # Performance Manager
│   │   ├── configuration/    # Configuration Manager
│   │   ├── accounting/       # Accounting Manager
│   │   ├── incidents/        # Incident Manager
│   │   ├── security/         # Security Manager
│   │   ├── users/            # Users
│   │   ├── settings/         # Settings, Profile, Account, Notifications, Display
│   │   ├── help/             # Help
│   │   └── errors/           # NotFound
│   ├── App.vue
│   └── main.js
├── index.html
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── vite.config.js
```

## Installation

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run development server:
```bash
npm run dev
```

The app will be available at http://localhost:3000

## Default Credentials

- **Username:** admin
- **Password:** admin

## Build for Production

```bash
npm run build
```

## Theme

The project uses a shadcn-admin inspired color palette:
- CSS variables for Light/Dark themes
- Card, muted, accent colors
- Smooth transitions between themes
- System preference detection

## Navigation Structure

### General
- Dashboard
- Plugins
- Inventory Manager
- Performance Manager
- Configuration Manager
- Accounting Manager
- Incident Manager
- Security Manager

### Pages
- Users
- Auth (Sign In, Sign Up, Forgot Password)

### Other
- Settings (Profile, Account, Notifications, Display)
- Help
