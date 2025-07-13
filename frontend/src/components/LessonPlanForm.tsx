import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Card,
  CardContent,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Paper,
} from '@mui/material';
import { School, Create, Send } from '@mui/icons-material';
import { LessonPlanRequest } from '../types/lessonPlan';

interface LessonPlanFormProps {
  onSubmit: (request: LessonPlanRequest) => void;
  loading: boolean;
}

const gradeLevels = [
  'Kindergarten',
  '1st Grade',
  '2nd Grade',
  '3rd Grade',
  '4th Grade',
  '5th Grade',
  '6th Grade',
  '7th Grade',
  '8th Grade',
  '9th Grade',
  '10th Grade',
  '11th Grade',
  '12th Grade',
];

export const LessonPlanForm: React.FC<LessonPlanFormProps> = ({ onSubmit, loading }) => {
  const [topic, setTopic] = useState('');
  const [gradeLevel, setGradeLevel] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!topic.trim()) {
      setError('Please enter a topic');
      return;
    }

    const request: LessonPlanRequest = {
      topic: topic.trim(),
      grade_level: gradeLevel || undefined,
    };

    onSubmit(request);
  };

  return (
    <Paper elevation={3} sx={{ p: 4, maxWidth: 600, mx: 'auto', mt: 4 }}>
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        <Box sx={{ textAlign: 'center', mb: 2 }}>
          <School sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
          <Typography variant="h4" component="h1" gutterBottom>
            Lesson Planner Bot
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Create comprehensive lesson plans with AI-powered content scraping
          </Typography>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <TextField
          label="Lesson Topic"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="e.g., Photosynthesis, Simple Machines, World War II"
          fullWidth
          required
          disabled={loading}
          sx={{ mb: 2 }}
        />

        <FormControl fullWidth disabled={loading}>
          <InputLabel>Grade Level (Optional)</InputLabel>
          <Select
            value={gradeLevel}
            label="Grade Level (Optional)"
            onChange={(e) => setGradeLevel(e.target.value)}
          >
            <MenuItem value="">
              <em>Any grade level</em>
            </MenuItem>
            {gradeLevels.map((grade) => (
              <MenuItem key={grade} value={grade}>
                {grade}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Button
          type="submit"
          variant="contained"
          size="large"
          disabled={loading || !topic.trim()}
          startIcon={loading ? <CircularProgress size={20} /> : <Create />}
          sx={{ mt: 2, py: 1.5 }}
        >
          {loading ? 'Creating Lesson Plan...' : 'Create Lesson Plan'}
        </Button>

        <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', mt: 2 }}>
          The AI will search for educational content and generate a complete lesson plan with objectives, materials, exercises, and assessments.
        </Typography>
      </Box>
    </Paper>
  );
}; 