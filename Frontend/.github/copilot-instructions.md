# AI Coding Guidelines for Frontend_Antena

## Project Overview
This is a React frontend application built with Vite, currently using the default template structure. The app is named "frontend-antena" and appears to be in early development stages.

## Architecture
- **Framework**: React 19 with functional components and hooks
- **Build Tool**: Vite 7 for fast development and building
- **Styling**: CSS with Tailwind CSS 4 installed (not yet utilized in components)
- **Linting**: ESLint with React-specific rules

## Key Files and Structure
- `src/App.jsx`: Main application component (currently displays Vite + React template)
- `src/main.jsx`: React 18 entry point with StrictMode
- `src/index.css`: Global styles (dark theme by default)
- `vite.config.js`: Minimal Vite configuration with React plugin
- `eslint.config.js`: ESLint config with custom unused vars rule (ignores uppercase vars like components)

## Development Workflows
- **Start dev server**: `npm run dev` (Vite with HMR)
- **Build for production**: `npm run build`
- **Lint code**: `npm run lint`
- **Preview build**: `npm run preview`

## Coding Conventions
- Use functional React components with hooks (e.g., `useState` in App.jsx)
- ESLint rule: `no-unused-vars` ignores vars starting with uppercase (for unused component imports)
- CSS classes for styling (Tailwind available but not applied yet)
- Import assets from `./assets/` or `/` (public folder)

## Dependencies
- React 19.2.0 (latest)
- Vite 7.2.4
- Tailwind CSS 4.1.18 (ready to use with `@tailwind` directives in CSS)

## Patterns to Follow
- Component structure: Export default function components
- State management: Local state with `useState` (no global state yet)
- Example from codebase: Counter component in App.jsx using `useState`