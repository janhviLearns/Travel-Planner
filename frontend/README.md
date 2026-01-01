# Travel Planner - React + TypeScript Frontend

A modern, minimal React + TypeScript application for the AI Travel Planner with natural language interface.

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Fast build tool and dev server
- **CSS Modules** - Component-scoped styling

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
# Install dependencies
npm install
```

### Development

```bash
# Start development server (with proxy to backend)
npm run dev
```

The app will be available at `http://localhost:5173` with hot module replacement.

The dev server proxies API requests to `http://localhost:8000` (make sure the backend is running).

### Build for Production

```bash
# Build for production
npm run build
```

This builds the app to `../static/` directory which the FastAPI backend serves.

### Preview Production Build

```bash
# Preview production build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/         # React components
│   │   ├── Header.tsx
│   │   ├── ChatInterface.tsx
│   │   ├── ChatMessage.tsx
│   │   ├── TypingIndicator.tsx
│   │   └── InfoPanel.tsx
│   ├── types.ts           # TypeScript interfaces
│   ├── api.ts             # API service
│   ├── App.tsx            # Main app component
│   ├── App.css
│   ├── index.css          # Global styles
│   └── main.tsx           # Entry point
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## Components

### Header
- Logo and branding
- API badge

### ChatInterface
- Main chat UI
- Message list
- Input area with suggestions
- Typing indicator

### ChatMessage
- Individual message bubble
- User/AI avatar
- Timestamp

### InfoPanel
- Features list
- Example queries
- Tech stack info

## Features

- ✨ Type-safe development with TypeScript
- 🎨 Modern, responsive design
- ⚡ Fast HMR with Vite
- 🔄 Real-time chat interface
- 📱 Mobile-friendly layout
- 🎯 Clean component architecture
- 🚀 Optimized production builds

## Development Tips

- Components are written in TypeScript with full type safety
- CSS is component-scoped for better maintainability
- API calls are centralized in `src/api.ts`
- Types are defined in `src/types.ts` for reusability

## Deployment

The production build outputs to `../static/` which is served by the FastAPI backend at the `/ui` route.

After building:
1. Run `npm run build`
2. Start the FastAPI server
3. Visit `http://localhost:8000/ui`

## Environment Variables

The app uses `import.meta.env.PROD` to determine the API base URL:
- Development: proxies to `http://localhost:8000`
- Production: uses relative URLs (same origin)

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## License

Part of the AI Travel Planner project.

