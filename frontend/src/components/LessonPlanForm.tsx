import React, { useState, useEffect } from 'react';
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
  LinearProgress,
  Fade,
  Slide,
  Card as MuiCard,
} from '@mui/material';
import { School, Create, Send, Search, Psychology, Assignment, CheckCircle, Lightbulb, TrendingUp, EmojiEvents, AutoAwesome } from '@mui/icons-material';
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

const funFacts = [
  {
    fact: "Did you know? The average teacher creates 150+ lesson plans per year! 📚",
    icon: TrendingUp,
    color: "#4CAF50"
  },
  {
    fact: "Fun fact: AI can analyze thousands of educational resources in seconds! ⚡",
    icon: AutoAwesome,
    color: "#2196F3"
  },
  {
    fact: "Interesting: The first lesson plan was created in 1892 by John Dewey! 🎓",
    icon: School,
    color: "#FF9800"
  },
  {
    fact: "Amazing: Your lesson plan will include activities for different learning styles! 🧠",
    icon: Psychology,
    color: "#9C27B0"
  },
  {
    fact: "Pro tip: Include hands-on activities for better student engagement! 🎯",
    icon: Assignment,
    color: "#F44336"
  },
  {
    fact: "Did you know? Visual learners make up 65% of students! 👁️",
    icon: Lightbulb,
    color: "#00BCD4"
  },
  {
    fact: "Fun fact: Students retain 90% when they teach others! 🤝",
    icon: EmojiEvents,
    color: "#FFC107"
  },
  {
    fact: "Amazing: The best lessons connect to real-world applications! 🌍",
    icon: AutoAwesome,
    color: "#4CAF50"
  }
];

const robotPoses = [
  { emoji: "🤖", animation: "thinking" },
  { emoji: "🤔", animation: "searching" },
  { emoji: "💡", animation: "idea" },
  { emoji: "✍️", animation: "writing" },
  { emoji: "🎯", animation: "targeting" },
  { emoji: "✨", animation: "sparkle" },
  { emoji: "🚀", animation: "launching" },
  { emoji: "🎉", animation: "celebrating" }
];

export const LessonPlanForm: React.FC<LessonPlanFormProps> = ({ onSubmit, loading }) => {
  const [topic, setTopic] = useState('');
  const [gradeLevel, setGradeLevel] = useState('');
  const [error, setError] = useState('');
  const [currentFactIndex, setCurrentFactIndex] = useState(0);
  const [currentPoseIndex, setCurrentPoseIndex] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (loading) {
      // Animate progress bar
      const progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 95) return prev;
          return prev + Math.random() * 15;
        });
      }, 1000);

      // Cycle through fun facts
      const factInterval = setInterval(() => {
        setCurrentFactIndex((prev) => (prev + 1) % funFacts.length);
      }, 3000);

      // Cycle through robot poses
      const poseInterval = setInterval(() => {
        setCurrentPoseIndex((prev) => (prev + 1) % robotPoses.length);
      }, 1500);

      return () => {
        clearInterval(progressInterval);
        clearInterval(factInterval);
        clearInterval(poseInterval);
      };
    } else {
      setProgress(0);
      setCurrentFactIndex(0);
      setCurrentPoseIndex(0);
    }
  }, [loading]);

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

  const currentFact = funFacts[currentFactIndex];
  const currentPose = robotPoses[currentPoseIndex];
  const IconComponent = currentFact.icon;

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

        {!loading ? (
          <>
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
              startIcon={<Create />}
              sx={{ mt: 2, py: 1.5 }}
            >
              Create Lesson Plan
            </Button>

            <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', mt: 2 }}>
              The AI will search for educational content and generate a complete lesson plan with objectives, materials, exercises, and assessments.
            </Typography>
          </>
        ) : (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
              Creating your lesson plan...
            </Typography>
            
            {/* Animated Robot Character */}
            <Box sx={{ mb: 4 }}>
              <Typography 
                variant="h1" 
                sx={{ 
                  fontSize: '4rem',
                  animation: `${currentPose.animation} 2s ease-in-out infinite`,
                  '@keyframes thinking': {
                    '0%, 100%': { transform: 'rotate(-5deg)' },
                    '50%': { transform: 'rotate(5deg)' }
                  },
                  '@keyframes searching': {
                    '0%, 100%': { transform: 'translateX(-10px)' },
                    '50%': { transform: 'translateX(10px)' }
                  },
                  '@keyframes idea': {
                    '0%, 100%': { transform: 'scale(1)' },
                    '50%': { transform: 'scale(1.1)' }
                  },
                  '@keyframes writing': {
                    '0%, 100%': { transform: 'rotateY(0deg)' },
                    '50%': { transform: 'rotateY(180deg)' }
                  },
                  '@keyframes targeting': {
                    '0%, 100%': { transform: 'translateY(0px)' },
                    '50%': { transform: 'translateY(-10px)' }
                  },
                  '@keyframes sparkle': {
                    '0%, 100%': { transform: 'rotate(0deg) scale(1)' },
                    '25%': { transform: 'rotate(90deg) scale(1.1)' },
                    '50%': { transform: 'rotate(180deg) scale(1)' },
                    '75%': { transform: 'rotate(270deg) scale(1.1)' }
                  },
                  '@keyframes launching': {
                    '0%, 100%': { transform: 'translateY(0px) scale(1)' },
                    '50%': { transform: 'translateY(-20px) scale(1.2)' }
                  },
                  '@keyframes celebrating': {
                    '0%, 100%': { transform: 'rotate(0deg)' },
                    '25%': { transform: 'rotate(-10deg)' },
                    '75%': { transform: 'rotate(10deg)' }
                  }
                }}
              >
                {currentPose.emoji}
              </Typography>
            </Box>

            {/* Progress Bar */}
            <Box sx={{ mb: 4 }}>
              <LinearProgress 
                variant="determinate" 
                value={Math.min(progress, 95)}
                sx={{ 
                  height: 12, 
                  borderRadius: 6, 
                  mb: 2,
                  '& .MuiLinearProgress-bar': {
                    borderRadius: 6,
                    background: 'linear-gradient(90deg, #4CAF50, #2196F3, #9C27B0)',
                    animation: 'shimmer 2s ease-in-out infinite',
                    '@keyframes shimmer': {
                      '0%': { backgroundPosition: '-200px 0' },
                      '100%': { backgroundPosition: 'calc(200px + 100%) 0' }
                    }
                  }
                }}
              />
              <Typography variant="body2" color="text.secondary">
                {Math.round(Math.min(progress, 95))}% Complete
              </Typography>
            </Box>

            {/* Fun Fact Card */}
            <Fade in={true} timeout={500}>
              <MuiCard 
                sx={{ 
                  mb: 3, 
                  p: 3, 
                  background: `linear-gradient(135deg, ${currentFact.color}15, ${currentFact.color}25)`,
                  border: `2px solid ${currentFact.color}30`,
                  borderRadius: 3,
                  position: 'relative',
                  overflow: 'hidden',
                  '&::before': {
                    content: '""',
                    position: 'absolute',
                    top: 0,
                    left: '-100%',
                    width: '100%',
                    height: '100%',
                    background: `linear-gradient(90deg, transparent, ${currentFact.color}20, transparent)`,
                    animation: 'shimmer 3s infinite',
                    '@keyframes shimmer': {
                      '0%': { left: '-100%' },
                      '100%': { left: '100%' }
                    }
                  }
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <IconComponent 
                    sx={{ 
                      fontSize: 32, 
                      color: currentFact.color,
                      animation: 'pulse 2s ease-in-out infinite',
                      '@keyframes pulse': {
                        '0%, 100%': { transform: 'scale(1)' },
                        '50%': { transform: 'scale(1.1)' }
                      }
                    }} 
                  />
                  <Typography 
                    variant="body1" 
                    sx={{ 
                      fontWeight: 500,
                      color: 'text.primary',
                      lineHeight: 1.6
                    }}
                  >
                    {currentFact.fact}
                  </Typography>
                </Box>
              </MuiCard>
            </Fade>

            {/* Status Messages */}
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, alignItems: 'center' }}>
              <Typography variant="body2" color="text.secondary">
                🤖 AI Assistant is working hard...
              </Typography>
              <Typography variant="body2" color="text.secondary">
                ⏱️ This usually takes 10-15 seconds
              </Typography>
              <Typography variant="body2" color="text.secondary">
                💡 Learning something new while you wait!
              </Typography>
            </Box>
          </Box>
        )}
      </Box>
    </Paper>
  );
}; 