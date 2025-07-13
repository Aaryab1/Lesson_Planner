import React, { useState } from 'react';
import { ThemeProvider, createTheme, CssBaseline, Container, Alert, Snackbar } from '@mui/material';
import { LessonPlanForm } from './components/LessonPlanForm';
import { LessonPlanDisplay } from './components/LessonPlanDisplay';
import { lessonPlanApi } from './services/api';
import { LessonPlan, LessonPlanRequest } from './types/lessonPlan';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
});

function App() {
  const [loading, setLoading] = useState(false);
  const [lessonPlan, setLessonPlan] = useState<LessonPlan | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleCreateLessonPlan = async (request: LessonPlanRequest) => {
    setLoading(true);
    setError(null);

    try {
      const response = await lessonPlanApi.createLessonPlan(request);
      
      if (response.success && response.lesson_plan) {
        setLessonPlan(response.lesson_plan);
      } else {
        setError(response.error || 'Failed to create lesson plan');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setLessonPlan(null);
    setError(null);
  };

  const handleCloseError = () => {
    setError(null);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="xl" sx={{ py: 2 }}>
        {lessonPlan ? (
          <LessonPlanDisplay lessonPlan={lessonPlan} onBack={handleBack} />
        ) : (
          <LessonPlanForm onSubmit={handleCreateLessonPlan} loading={loading} />
        )}
        
        <Snackbar
          open={!!error}
          autoHideDuration={6000}
          onClose={handleCloseError}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        >
          <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
            {error}
          </Alert>
        </Snackbar>
      </Container>
    </ThemeProvider>
  );
}

export default App;
