# shadcn/ui Integration

This project has been configured to use shadcn/ui components with a vanilla JavaScript setup.

## Project Structure

```
.
├── components/
│   ├── ui/              # shadcn/ui components
│   │   └── button.jsx   # Example button component
│   └── SearchExample.jsx # Example of using shadcn/ui components
├── lib/
│   └── utils.js         # Utility functions (cn helper)
├── styles/
│   └── globals.css      # Tailwind CSS and theme variables
├── components.json      # shadcn/ui configuration
└── tailwind.config.js   # Tailwind CSS configuration
```

## How to Add More Components

You can add more shadcn/ui components using the CLI:

```bash
npx shadcn@latest add <component-name>
```

For example:
```bash
npx shadcn@latest add card
npx shadcn@latest add dialog
```

## How to Use Components

1. Import the component in your React component:
```jsx
import { Button } from "@/components/ui/button";
```

2. Use it in your JSX:
```jsx
<Button variant="default">Click me</Button>
```

## Available Components

- Button (`@/components/ui/button`)

## Customization

You can customize the theme by modifying the CSS variables in `styles/globals.css`.
The theme follows the shadcn/ui default theme with light and dark modes.