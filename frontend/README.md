# Lesson Planner Bot - Frontend

A modern React frontend for the AI-powered lesson planning assistant.

## Features

- 🎨 **Modern UI**: Built with Material-UI for a clean, professional look
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- ⚡ **Real-time Feedback**: Loading states and error handling
- 📚 **Comprehensive Display**: Beautiful presentation of lesson plans with all components
- 🔗 **Source Links**: Direct access to educational resources

## Tech Stack

- **React 18** with TypeScript
- **Material-UI (MUI)** for components and theming
- **Axios** for API communication
- **React Router** for navigation (if needed)

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend server running on `http://localhost:8000`

### Installation

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

4. **Open your browser** and go to `http://localhost:3000`

## Usage

### Creating a Lesson Plan

1. **Enter a topic** in the main input field (e.g., "Photosynthesis", "Simple Machines")
2. **Select a grade level** (optional) from the dropdown
3. **Click "Create Lesson Plan"** to generate the plan
4. **Wait for the AI** to scrape content and generate the lesson plan
5. **Review the complete lesson plan** with all components

### Lesson Plan Components

The generated lesson plan includes:

- **Learning Objectives**: Clear goals for student achievement
- **Materials Needed**: List of required supplies and resources
- **Lesson Overview**: Detailed breakdown of lesson segments with timing
- **Classroom Exercises**: Hands-on activities for students
- **Assessment Questions**: Evaluation questions to test understanding
- **Source Materials**: Links to educational resources used

### Navigation

- **Create New Lesson Plan**: Click the button to return to the form
- **Source Links**: Click on source chips to open educational resources
- **Accordion Sections**: Expand/collapse lesson overview segments

## Development

### Project Structure

```
src/
├── components/
│   ├── LessonPlanForm.tsx      # Main form for creating lesson plans
│   └── LessonPlanDisplay.tsx   # Display component for lesson plans
├── services/
│   └── api.ts                  # API communication layer
├── types/
│   └── lessonPlan.ts           # TypeScript interfaces
└── App.tsx                     # Main application component
```

### Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

### Customization

#### Theme

The app uses a custom Material-UI theme. You can modify colors and typography in `App.tsx`:

```typescript
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2', // Change primary color
    },
    secondary: {
      main: '#dc004e', // Change secondary color
    },
  },
  // ... other theme options
});
```

#### API Configuration

Update the API base URL in `src/services/api.ts`:

```typescript
const API_BASE_URL = 'http://localhost:8000'; // Change to your backend URL
```

## Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Ensure the backend server is running on port 8000
   - Check that CORS is properly configured on the backend

2. **Build Errors**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check TypeScript errors in the console

3. **Styling Issues**
   - Ensure all Material-UI dependencies are installed
   - Check browser console for CSS conflicts

### Development Tips

- Use the browser's developer tools to inspect the API requests
- Check the Network tab to see communication with the backend
- Use React Developer Tools for component debugging

## Deployment

### Production Build

1. **Create a production build**:
   ```bash
   npm run build
   ```

2. **Serve the build folder** using a static server:
   ```bash
   npx serve -s build
   ```

### Environment Variables

Create a `.env` file in the frontend directory for environment-specific configuration:

```
REACT_APP_API_URL=http://localhost:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Lesson Planner Bot application.
